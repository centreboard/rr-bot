import requests

import xml.etree.ElementTree as ET

from RowGeneration.PlaceNotationGenerator import PlaceNotationGenerator


class MethodPlaceNotationGenerator(PlaceNotationGenerator):
    def __init__(self, method_title: str, auto_start=True, logger=print):
        method_pn, stage = self._load_method(method_title)
        if stage % 2:
            stage += 1
        super(MethodPlaceNotationGenerator, self).__init__(stage, method_pn, auto_start=auto_start, logger=logger)

    @staticmethod
    def _load_method(method_title: str):
        params = {'title': method_title, 'fields': 'pn|stage'}
        source = requests.get('http://methods.ringing.org/cgi-bin/simple.pl', params=params)

        root = ET.fromstring(source.text)
        methodxml = root
        xmlns = '{http://methods.ringing.org/NS/method}'
        symblock = methodxml.findall(xmlns + 'method/' + xmlns + 'pn/' + xmlns + 'symblock')
        block = methodxml.findall(xmlns + 'method/' + xmlns + 'pn/' + xmlns + 'block')
        stage = int(methodxml.find(xmlns + 'method/' + xmlns + 'stage').text)

        if len(symblock) != 0:
            notation = "&" + symblock[0].text
            le = symblock[1].text
            return f"&{notation}, {le}", stage
        elif len(block) != 0:
            notation = block[0].text
            return notation, stage
        else:
            raise Exception("Place notation not found")
