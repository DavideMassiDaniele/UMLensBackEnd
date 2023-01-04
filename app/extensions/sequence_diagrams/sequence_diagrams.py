from typing import Dict
import xml.etree.ElementTree as Et

from .models.xml_type import XmlType
from .models.xml_attribute import XmlAttribute


class SequenceDiagramParser:

    # inizializza l'albero relativo al path del file XML 
    def __init__(self, filepath):
        tree = Et.parse(filepath)
        root = tree.getroot()
        self.models = root.find(XmlType.MODELS)

    # restituisce un oggetto che comprende tutte le liste degli elementi del diagramma parsati
    def get_data(self):
        return {
            'messages': self._parse_messages(),
            'lifelines': self._parse_lifelines(),
            'actors': self._parse_actors(),
            'frames': self._parse_frames(),
            'classes': self._parse_classes(),
            'notes': self._parse_notes(),
            'combined_fragments': self._parse_combined_fragments()
        }

    # comprende tutte le metriche calcolate
    def get_metrics(self):
        data = self.get_data()
        data.setdefault('metrics', [
            {'number of total messages': len(data.get('messages'))}, # numero dei messaggi totali
            {'number of self messages': self._self_messages(data.get('messages'))}, # numero dei self messages
            {'number of lifelines': len(data.get('lifelines'))}, # numero delle lifeline
            {'number of combined fragments': len(data.get('combined_fragments'))}, # numero dei frammenti combinati
            {'height of sequence diagram': self._height(data.get('messages'), data.get('lifelines'))} # altezza del diagramma
        ])
        return data

    # metrica per il calcolo dei messaggi che un oggetto invia a se stesso
    def _self_messages(self, messages):
        n = 0
        types = ['Recursive Message', 'Self Message']
        for message in messages:
            if message.get('TYPE') in types:
                n = n + 1
        return n

    # metrica per il calcolo dell'altezza del diagramma (numero massimo di messaggi in entrata e uscita da ogni lifeline)
    def _height(self, messages, lifelines):
        N = []
        for lifeline in lifelines:
            n = self._ll_id_list(messages).count(lifeline.get('ID'))
            N.append(n)
        height = max(N)
        return height

    # restituisce la lista delle lifeline mittenti e destinatarie di ogni messaggio del diagramma
    def _ll_id_list(self, messages):
        z = []
        for message in messages:
            z.append(message.get('FROM_END'))
            z.append(message.get('TO END'))
        return z

    # individua tutti i messaggi presenti nel diagramma
    def _parse_messages(self):
        messages = []
        for message in self.models.iter(XmlType.MESSAGE):
            if message.get(XmlAttribute.ID) != None:
                _message = {}
                _message['ID'] = message.get(XmlAttribute.ID)
                _message['NAME'] = message.get(XmlAttribute.NAME)
                _message['FROM_END'] = message.get(XmlAttribute.FROM_END)
                _message['TO END'] = message.get(XmlAttribute.TO_END)
                _message['TYPE'] = message.get(XmlAttribute.TYPE)
                _message['SEQUENCE NUMBER'] = message.get(XmlAttribute.SEQUENCE_NUMBER)
                messages.append(_message)
        return messages

    # individua tutte le lifeline presenti nel diagramma
    def _parse_lifelines(self):
        lifelines = []
        for lifeline in self.models.iter(XmlType.LIFELINE):
            if lifeline.get(XmlAttribute.ID) != None:
                _lifeline = {}
                _lifeline['ID'] = lifeline.get(XmlAttribute.ID)
                _lifeline['NAME'] = lifeline.get(XmlAttribute.NAME)
                _lifeline['STOPPED'] = lifeline.get(XmlAttribute.STOPPED)
                lifelines.append(_lifeline)
        return lifelines

    # individua tutti gli attori presenti nel diagramma
    def _parse_actors(self):
        actors = []
        for actor in self.models.iter(XmlType.ACTOR):
            if actor.get(XmlAttribute.ID) != None:
                _actor = {}
                _actor['ID'] = actor.get(XmlAttribute.ID)
                _actor['NAME'] = actor.get(XmlAttribute.NAME)
                actors.append(_actor)
        return actors

    #individua tutti i frame presenti nel diagramma
    def _parse_frames(self):
        frames = []
        for frame in self.models.iter(XmlType.FRAME):
            if frame.get(XmlAttribute.ID) != None:
                _frame = {}
                _frame['ID'] = frame.get(XmlAttribute.ID)
                _frame['NAME'] = frame.get(XmlAttribute.NAME)
                _frame['TYPE'] = frame.get(XmlAttribute.TYPE)
                frames.append(_frame)
        return frames

    # individua le classi presenti nel diagramma
    def _parse_classes(self):
        classes = []
        for class_ in self.models.iter(XmlType.CLASS):
            if class_.get(XmlAttribute.ID) != None:
                _class = {}
                _class['ID'] = class_.get(XmlAttribute.ID)
                _class['NAME'] = class_.get(XmlAttribute.NAME)
                _class['VISIBILITY'] = class_.get(XmlAttribute.VISIBILITY)
                classes.append(_class)
        return classes

    # individua le note presenti nel diagramma
    def _parse_notes(self):
        notes = []
        for note in self.models.iter(XmlType.NOTE):
            if note.get(XmlAttribute.ID) != None:
                _note = {}
                _note['ID'] = note.get(XmlAttribute.ID)
                _note['DOCUMENTATION PLAN'] = note.get(XmlAttribute.DOCUMENTATION_PLAIN)
                notes.append(_note)
        return notes

    # individua i frammenti combinati del diagramma
    def _parse_combined_fragments(self):
        fragments = []
        for fragment in self.models.iter(XmlType.COMBINED_FRAGMENT):
            if fragment.get(XmlAttribute.ID) != None:
                _fragment = {}
                _fragment['ID'] = fragment.get(XmlAttribute.ID)
                _fragment['NAME'] = fragment.get(XmlAttribute.NAME)
                _fragment['OPERATOR_KIND'] = fragment.get(XmlAttribute.OPERATOR_KIND)
                fragments.append(_fragment)
        return fragments
