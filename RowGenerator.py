from abc import abstractmethod, ABC


class RowGenerator(ABC):
    def __init__(self, stage: int, auto_start=True, logger=print):
        self.stage = stage
        self.logger = logger

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
        return self._row

    def go(self):
        self._has_go = True

    def bob(self):
        self._has_bob = True

    def single(self):
        self._has_single = True

    def thats_all(self):
        self._index = 0
        self._has_go = False
        self._row = self._rounds()

    def _rounds(self):
        return [i for i in range(1, self.stage + 1)]

    @abstractmethod
    def _gen_row(self, previous_row: [int], is_handstroke: bool, index: int) -> [int]:
        pass

    def permute(self, row: [int], places: [int]) -> [int]:
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


class PlainHuntGenerator(RowGenerator):
    def _gen_row(self, previous_row: [int], is_handstroke: bool, index: int) -> [int]:
        if is_handstroke:
            return self.permute(previous_row, [])
        else:
            return self.permute(previous_row, [1, self.stage])


class PlaceNotationGenerator(RowGenerator):
    def __init__(self, stage: int, method: str, plain: str, bob: str = '14', single: str = '1234', auto_start=True,
                 logger=print):
        super(PlaceNotationGenerator, self).__init__(stage, auto_start, logger)
        self.method_pn = self._convert_pn(method)
        self.plain_pn = self._convert_pn(plain)
        self.bob_pn = self._convert_pn(bob)
        self.single_pn = self._convert_pn(single)

        assert len(self.plain_pn) == len(self.bob_pn)
        assert len(self.plain_pn) == len(self.single_pn)
        self._mod_index = len(self.method_pn) + len(self.plain_pn)

    def _gen_row(self, previous_row: [int], is_handstroke: bool, index: int) -> [int]:
        lead_index = index % self._mod_index

        if lead_index < len(self.method_pn):
            return self.permute(previous_row, self.method_pn[lead_index])
        lead_end_index = lead_index - len(self.method_pn)
        if self._has_bob:
            return self.permute(previous_row, self.bob_pn[lead_end_index])
        if self._has_single:
            return self.permute(previous_row, self.single_pn[lead_end_index])
        return self.permute(previous_row, self.plain_pn[lead_end_index])

    @staticmethod
    def _convert_pn(pn_str: str):
        cross_pn = []

        symmetric = pn_str.startswith('&')

        cleaned = pn_str.replace('x', '-').replace('-', '.-.').strip('.& ').split('.')

        converted = [[int(y) for y in place] if place != '-' else cross_pn for place in cleaned]
        if symmetric:
            return converted + list(reversed(converted[:-1]))
        else:
            return converted
