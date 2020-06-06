from RowGeneration.RowGenerator import RowGenerator


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

    def _convert_pn(self, pn_str: str):
        cross_pn = []

        symmetric = pn_str.startswith('&')

        cleaned = pn_str.replace('x', '-').replace('-', '.-.').strip('.& ').split('.')

        converted = [[self.convert_bell_string(y) for y in place] if place != '-' else cross_pn for place in cleaned]
        if symmetric:
            return converted + list(reversed(converted[:-1]))
        else:
            return converted
