from abc import ABC, abstractmethod
from typing import List

from RowGeneration.Helpers import Helpers


class RowGenerator(ABC):
    def __init__(self, stage: int, auto_start=True, logger=print):
        self.stage = stage
        self._logger = logger

        self._has_go = auto_start
        self._has_bob = False
        self._has_single = False
        self._index = -1
        self._row = self._rounds()

    def next_row(self, is_handstroke: bool):
        if not self._has_go or self._index < 0 or (self._index == 0 and not is_handstroke):
            if self._index < 0:
                self._index += 1
            return self._rounds()
        self._row = self._gen_row(self._row, is_handstroke, self._index)
        self._index += 1

        self.log(" ".join([Helpers.convert_to_bell_string(bell) for bell in self._row]))

        return self._row

    def go(self):
        self._has_go = True

    def bob(self):
        self._has_bob = True

    def single(self):
        self._has_single = True

    def reset(self):
        self.log("Reset")
        self._index = 0
        self._has_go = False
        self._row = self._rounds()
        self.reset_calls()

    def reset_calls(self):
        self.log("Reset calls")
        self._has_bob = False
        self._has_single = False

    def _rounds(self):
        return [i for i in range(1, self.stage + 1)]

    def log(self, message: str):
        self._logger(f"ROWGEN: {message}")

    @abstractmethod
    def _gen_row(self, previous_row: List[int], is_handstroke: bool, index: int) -> List[int]:
        pass

    def permute(self, row: List[int], places: List[int]) -> List[int]:
        new_row = list(row)
        i = 1
        if places and places[0] % 2 == 0:
            # Skip 1 for implicit Lead
            i += 1

        while i < self.stage:
            if i in places:
                i += 1
                continue
            else:
                # If not in place, must swap, index is 1 less than place
                new_row[i - 1], new_row[i] = new_row[i], new_row[i - 1]
                i += 2

        return new_row
