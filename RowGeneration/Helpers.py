from typing import List


class Helpers:
    @staticmethod
    def convert_pn(pn_str: str) -> List[List[int]]:
        cross_pn = []

        symmetric = pn_str.startswith('&')

        cleaned = pn_str.replace('x', '-').replace('-', '.-.').strip('.& ').split('.')

        converted = [[Helpers.convert_bell_string(y) for y in place] if place != '-' else cross_pn for place in cleaned]
        if symmetric:
            return converted + list(reversed(converted[:-1]))
        else:
            return converted

    _lookup = ["Intentionally Left Blank", "1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "E", "T"]

    @staticmethod
    def convert_bell_string(bell: str) -> int:
        return Helpers._lookup.index(bell)

    @staticmethod
    def convert_to_bell_string(bell: int) -> str:
        return Helpers._lookup[bell]
