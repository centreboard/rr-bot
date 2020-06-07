from typing import List

import itertools
import re


class Helpers:
    cross_pn = []

    @staticmethod
    def convert_pn(pn_str: str) -> List[List[int]]:
        if "," in pn_str:
            return list(itertools.chain.from_iterable(Helpers.convert_pn(part) for part in pn_str.split(",")))

        symmetric = pn_str.startswith('&')

        cleaned = re.sub("[.]*[x-][.]*", ".-.", pn_str).strip('.& ').split('.')

        converted = [[Helpers.convert_bell_string(y) for y in place] if place != '-' else Helpers.cross_pn
                     for place in cleaned]
        if symmetric:
            return converted + list(reversed(converted[:-1]))
        else:
            return converted

    _lookup = ["Intentionally Left Blank", "1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "E", "T"]

    @staticmethod
    def convert_bell_string(bell: str) -> int:
        try:
            return Helpers._lookup.index(bell)
        except ValueError:
            raise ValueError(f"'{bell}' is not known bell symbol")

    @staticmethod
    def convert_to_bell_string(bell: int) -> str:
        if bell <= 0 or bell >= len(Helpers._lookup):
            raise ValueError(f"'{bell}' is not known bell number")
        return Helpers._lookup[bell]
