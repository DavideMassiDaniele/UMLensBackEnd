from typing import List, Tuple
from PIL import Image, ImageDraw, ImageFont
from .model import Connector, Shape
import math
from .model import Background, Diagram
import base64
from io import BytesIO

class Generator:

    def __init__(self, diagram: Diagram) -> None:
        self.diagram = diagram

    def generate_image(self):
        img = self._draw_background(self.diagram.background)
        if len(self.diagram.shapes) != 0:
            img = self._draw_shapes(img, self.diagram.shapes)
        if len(self.diagram.connectors) != 0:
            img = self._draw_connectors(img, self.diagram.connectors)
        return img

    # richiama funzioni per disegnare background, shapes e connectors
    # attualmente img.show() mostra a schermo il diagramma risultante
    def draw_diagram(self):
        img = self.generate_image()
        img.show()

    def get_diagram(self):
        img = self.generate_image()
        buffered = BytesIO()
        img.save(buffered, format="PNG")
        return base64.b64encode(buffered.getvalue())

    # crea lo sfondo del diagramma da un background
    def _draw_background(self, bg_info: Background) -> Image:
        size = (bg_info.width, bg_info.height)
        bg = Image.new('RGBA', size, bg_info.background_color)
        return bg
    

    # crea connectors da una lista di connectors
    def _draw_connectors(self, base_img: Image, connectors: List[Connector]) -> Image:
        img = ImageDraw.Draw(base_img)

        for connector in connectors:

            if connector.tag == 'Generalization':
                self._draw_generalization(connector, img)
            elif connector.tag == 'Composition':
                self._draw_composition(connector, img)
            elif connector.tag == 'Realization':
                self._draw_realization(connector, img)
            elif connector.tag == 'Dependency':
                self._draw_dependency(connector, img)
            elif connector.tag == 'Association':
                self._draw_association(connector, img)
            elif connector.tag == 'Aggregation':
                self._draw_aggregation(connector, img)
            elif connector.tag == 'Instantiation':
                self._draw_connector_with_caption(connector, img, "<<instantiate>>")
            elif connector.tag == 'Usage':
                self._draw_connector_with_caption(connector, img, "<<use>>")
            elif connector.tag == 'Abstraction':
                self._draw_connector_with_caption(connector, img, "<<abstraction>>")
            elif connector.tag == 'BindingDependency':
                self._draw_connector_with_caption(connector, img, "<<bind>>")
            elif connector.tag == 'Import':
                self._draw_connector_with_caption(connector, img, "<<import>>")
            elif connector.tag == 'Substitution':
                self._draw_connector_with_caption(connector, img, "<<substitute>>")
            elif connector.tag == 'Permission':
                self._draw_connector_with_caption(connector, img, "<<permit>>")
            elif connector.tag == 'Derive':
                self._draw_connector_with_caption(connector, img, "<<derive>>")
            elif connector.tag == 'Merge':
                self._draw_connector_with_caption(connector, img, "<<merge>>")
            elif connector.tag == 'Access':
                self._draw_connector_with_caption(connector, img, "<<access>>")
            elif connector.tag == 'Refine':
                self._draw_connector_with_caption(connector, img, "<<refine>>")
            elif connector.tag == 'Trace':
                self._draw_connector_with_caption(connector, img, "<<trace>>")
            elif connector.tag == _:
                self._draw_association(connector, img)
  
        return base_img



    # metodi che disegnano i vari tipi di frecce in un diagramma

    def _draw_realization(self, connector: Connector, img: ImageDraw):
        for index, coordinates in enumerate(connector.coordinates):
            if index + 1 < len(connector.coordinates):
                if index!= 0:
                    self._dashed_line(img, coordinates[0], coordinates[1], connector.coordinates[index+1][0], connector.coordinates[index+1][1], color = connector.color)
                else:
                    self._dashed_line(img, coordinates[0], coordinates[1], connector.coordinates[index+1][0], connector.coordinates[index+1][1], color = connector.color)

                    self._triangle(img,(connector.coordinates[index+1][0], connector.coordinates[index+1][1]), (coordinates[0], coordinates[1]), connector.bg_color, connector.color)



    def _draw_connector_with_caption(self, connector: Connector, img: ImageDraw, caption: str):

        connector.coordinates.reverse()

        for index, coordinates in enumerate(connector.coordinates):
            if index + 1 < len(connector.coordinates):
                if index!= 0:
                    self._dashed_line(img, coordinates[0], coordinates[1], connector.coordinates[index+1][0], connector.coordinates[index+1][1], color = connector.color)
                else:
                    font = ImageFont.truetype("app/extensions/class_diagram/diagram_viewer/assets/fonts/arial.ttf",  10)
                    img.text([connector.caption_x, connector.caption_y], caption, 'black', font, anchor='lm')
                    self._dashed_line(img, coordinates[0], coordinates[1], connector.coordinates[index+1][0], connector.coordinates[index+1][1], color = connector.color)
                    self._empty_triangle(img,(connector.coordinates[index+1][0], connector.coordinates[index+1][1]), (coordinates[0], coordinates[1]), connector.color)


    def _draw_dependency(self, connector: Connector, img: ImageDraw):

        connector.coordinates.reverse()

        for index, coordinates in enumerate(connector.coordinates):
            if index + 1 < len(connector.coordinates):
                self._dashed_line(img, coordinates[0], coordinates[1], connector.coordinates[index+1][0], connector.coordinates[index+1][1], color = connector.color)
                if index == 0:
                    self._empty_triangle(img,(connector.coordinates[index+1][0], connector.coordinates[index+1][1]), (coordinates[0], coordinates[1]), connector.color)
                    
                    

    def _draw_composition(self, connector: Connector, img: ImageDraw):
        for index, coordinates in enumerate(connector.coordinates):
            if index + 1 < len(connector.coordinates):
                img.line([(coordinates[0], coordinates[1]), (connector.coordinates[index+1][0],
                        connector.coordinates[index+1][1])], fill=connector.color, width = connector.weight)
                if index == 0:
                    self._rhombus(img,(connector.coordinates[index+1][0], connector.coordinates[index+1][1]), (coordinates[0], coordinates[1]), 'black', connector.color)


    def _draw_association(self, connector: Connector, img: ImageDraw):
        for index, coordinates in enumerate(connector.coordinates):
            if index + 1 < len(connector.coordinates):
                img.line([(coordinates[0], coordinates[1]), (connector.coordinates[index+1][0],
                        connector.coordinates[index+1][1])], fill=connector.color, width = connector.weight)
                if index == 0:
                    if connector.aggregation_kind == 'Shared':
                        self._rhombus(img,(connector.coordinates[index+1][0], connector.coordinates[index+1][1]), (coordinates[0], coordinates[1]), 'white', connector.color)
                    elif connector.aggregation_kind == 'Composited':
                        self._rhombus(img,(connector.coordinates[index+1][0], connector.coordinates[index+1][1]), (coordinates[0], coordinates[1]), 'black', connector.color)
                    
                

    def _draw_aggregation(self, connector: Connector, img: ImageDraw):
        for index, coordinates in enumerate(connector.coordinates):
            if index + 1 < len(connector.coordinates):
                img.line([(coordinates[0], coordinates[1]), (connector.coordinates[index+1][0],
                        connector.coordinates[index+1][1])], fill=connector.color, width = connector.weight)
                if index == 0:
                    self._rhombus(img,(connector.coordinates[index+1][0], connector.coordinates[index+1][1]), (coordinates[0], coordinates[1]), 'white', connector.color)


    def _draw_generalization(self, connector: Connector, img: ImageDraw):
        for index, coordinates in enumerate(connector.coordinates):
            if index + 1 < len(connector.coordinates):
                img.line([(coordinates[0], coordinates[1]), (connector.coordinates[index+1][0],
                        connector.coordinates[index+1][1])], fill=connector.color, width = connector.weight)
                if index == 0:
                    self._triangle(img,(connector.coordinates[index+1][0], connector.coordinates[index+1][1]), (coordinates[0], coordinates[1]), 'white', connector.color)
                    


    # metodi che disegnano le punte delle frecce

    def _triangle(self,  img: ImageDraw, ptA: Tuple, ptB: Tuple, color: str, outline: str):
    
        vertici = self._find_arrowhead_points(ptA, ptB)

        img.polygon([vertici[0], vertici[1], ptB], fill=color, outline=outline)


    def _empty_triangle(self, img: ImageDraw, ptA: Tuple, ptB: Tuple, outline: str):

        vertici = self._find_arrowhead_points(ptA, ptB)

        img.line([ptB,vertici[0]], outline)
        img.line([ptB,vertici[1]], outline)


    def _rhombus(self,  img: ImageDraw, ptA: Tuple, ptB: Tuple, color: str, outline: str):

        vertici = self._find_arrowhead_points(ptA, ptB)

        deltax = vertici[2]-ptB[0]
        deltay = vertici[3]-ptB[1]

        rx = vertici[2] + deltax
        ry = vertici[3] + deltay
        r = (rx, ry)

        img.polygon([vertici[0], r, vertici[1], ptB], fill=color, outline=outline)




    # metodo che trova i vertici per costruire le punte delle frecce
    def _find_arrowhead_points(self, ptA: Tuple, ptB: Tuple) -> Tuple:

        #coordinate punti inizio ultima linea
        x0, y0 = ptA
        #coorinate punta freccia
        x1, y1 = ptB

        #coordinate dell'intersezione linea - base della punta
        xb = 0.80*(x1-x0)+x0
        yb = 0.80*(y1-y0)+y0

        #controlla se la linea è verticale o orizzontale
        if x0==x1:
           vtx0 = (xb-5, yb)
           vtx1 = (xb+5, yb)
        elif y0==y1:
           vtx0 = (xb, yb+5)
           vtx1 = (xb, yb-5)
        else:
           alpha = math.atan2(y1-y0,x1-x0) - 90*math.pi/180
           a = 6*math.cos(alpha)
           b = 6*math.sin(alpha)
           vtx0 = (xb+a, yb+b)
           vtx1 = (xb-a, yb-b)

        return vtx0, vtx1, xb, yb



    

    # metodo che disegna linea tratteggiata
    def _dashed_line(self, base_img: ImageDraw, x0, y0, x1, y1, color='black', dashlen=5, ratio=2): 
        
        dx=x1-x0 # delta x
        dy=y1-y0 # delta y
        # calcolo lunghezza segmento
        if dy==0:
            len=abs(dx)
        elif dx==0:
            len=abs(dy)
        else:
            len=math.sqrt(dx*dx+dy*dy)

        xa=dx/len
        ya=dy/len

        step=dashlen*ratio # lunghezza spazio tra trattini
        
        a0=0
        while a0<len:
            a1=a0+dashlen
            if a1>len:
                a1=len
            base_img.line((x0+xa*a0, y0+ya*a0, x0+xa*a1, y0+ya*a1), fill = color, width = 1)
            a0+=step


    # da implementare
    #def rgba_2_rgb(self, rgba_string: str) -> str:
    #    pattern = re.compile('^(rgba)')
    #    if pattern.search(rgba_string):
    #        rgb_string = re.sub(   , ')', rgba_string)


    # crea connectors da una lista di connectors
    def _draw_shapes(self, base_img: Image, shapes: List[Shape]) -> Image:
        img = ImageDraw.Draw(base_img)

        for shape in shapes:
            # aggiungere altre shapes (triangolo, ottagono, esagono, trapezio, rombo)
            if shape.primitive_shape_type == '0':   # disegna rettangolo
                img.rectangle([(shape.x, shape.y), (shape.x+shape.width, shape.y+shape.height)], fill = shape.bgcolor, outline = shape.outline_color, width = shape.outline_weight)
            elif shape.primitive_shape_type == '2':   # disegna rettangolo arrotondato
                img.rounded_rectangle([(shape.x, shape.y), (shape.x+shape.width, shape.y+shape.height)], radius = 4, fill = shape.bgcolor, outline = shape.outline_color, width = shape.outline_weight)
            elif shape.primitive_shape_type == '3':   # disegna ellisse
                img.ellipse([(shape.x, shape.y), (shape.x+shape.width, shape.y+shape.height)], fill = shape.bgcolor, outline = shape.outline_color, width = shape.outline_weight)
            elif shape.primitive_shape_type == _:
                img.rectangle([(shape.x, shape.y), (shape.x+shape.width, shape.y+shape.height)], fill = shape.bgcolor, outline = shape.outline_color, width = shape.outline_weight)

            font = ImageFont.truetype("app/extensions/class_diagram/diagram_viewer/assets/fonts/arial.ttf",  shape.font_size)

            w, h = img.textsize(shape.name)
            img.text([shape.x+ (shape.width-w)/2, shape.y], shape.name, fill=shape.text_color, font=font)
            #self.rgba_2_rgb(shape.outline_color)
            img.line([shape.x, shape.y+h, shape.x+shape.width, shape.y+h], fill = shape.outline_color)

            if shape.stereotypes:
                for stereotype in shape.stereotypes:
                    w, h = img.textsize(stereotype)
                    img.text([shape.x+ (shape.width-w)/2, shape.y-h], "<<"+stereotype+">>", fill=shape.text_color, font=font)

            a=0

            if shape.attributes:
                for attribute in shape.attributes:
                    w, h = img.textsize(attribute.name)
                    img.text([shape.x, shape.y+h+a], attribute.visibility+' '+attribute.name, fill=shape.text_color, font=font, anchor='lt')
                    a+=h+1
                img.line([shape.x, shape.y+h+a, shape.x+shape.width, shape.y+h+a], fill = shape.outline_color)

            if shape.operations:
                for operation in shape.operations:
                    w, h = img.textsize(operation.name)
                    img.text([shape.x, shape.y+h+a], operation.visibility+' '+operation.name, fill=shape.text_color, font=font, anchor='lt')
                    a+=h+1

        return base_img
