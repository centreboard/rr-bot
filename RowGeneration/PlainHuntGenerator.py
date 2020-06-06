from RowGeneration.RowGenerator import RowGenerator


class PlainHuntGenerator(RowGenerator):
    def _gen_row(self, previous_row: [int], is_handstroke: bool, index: int) -> [int]:
        if is_handstroke:
            return self.permute(previous_row, [])
        else:
            return self.permute(previous_row, [1, self.stage])
