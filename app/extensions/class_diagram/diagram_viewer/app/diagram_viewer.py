from .generator import Generator
from .dv_parser import Parser


def get_diagram(xml_path):

    parser = Parser()

    # il metodo parse() è da parametrizzare con l'indirizzo del file xml che invia l'utente
    parsed_data = parser.parse(xml_path)

    gen = Generator(parsed_data)

    # il metodo mostra il diagramma a schermo con .show()
    return gen.get_diagram()

