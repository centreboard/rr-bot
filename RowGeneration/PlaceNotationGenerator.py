from typing import List

from RowGeneration.Helpers import Helpers
from RowGeneration.RowGenerator import RowGenerator


class PlaceNotationGenerator(RowGenerator):
    def __init__(self, stage: int, method: str, plain: str, bob: str = '14', single: str = '1234', auto_start=True,
                 logger=print):
        super(PlaceNotationGenerator, self).__init__(stage, auto_start, logger)
        self.method_pn = Helpers.convert_pn(method)
        self.plain_pn = Helpers.convert_pn(plain)
        self.bob_pn = Helpers.convert_pn(bob)
        self.single_pn = Helpers.convert_pn(single)

        assert len(self.plain_pn) == len(self.bob_pn)
        assert len(self.plain_pn) == len(self.single_pn)
        self._mod_index = len(self.method_pn) + len(self.plain_pn)

    def _gen_row(self, previous_row: List[int], is_handstroke: bool, index: int) -> List[int]:
        lead_index = index % self._mod_index

        if lead_index < len(self.method_pn):
            place_notation = self.method_pn[lead_index]
        else:
            lead_end_index = lead_index - len(self.method_pn)

            if self._has_bob:
                place_notation = self.bob_pn[lead_end_index]
            elif self._has_single:
                place_notation = self.single_pn[lead_end_index]
            else:
                place_notation = self.plain_pn[lead_end_index]
            if lead_end_index + 1 == len(self.bob_pn):
                self.reset_calls()

        return self.permute(previous_row, place_notation)

    @staticmethod
    def grandsire(stage: int):
        assert stage % 2

        stage_bell = Helpers.convert_to_bell_string(stage)

        main_body = [stage_bell if i % 2 else "1" for i in range(1, 2 * stage - 1)]
        main_body[0] = "3"
        notation = ".".join(main_body)
        return PlaceNotationGenerator(stage + 1, notation, f"{stage_bell}.1", "3.1", "3.123")

    # @staticmethod
    # def stedman(stage: int):
    #     assert stage % 2
    #
    #     if stage == 5:
    #         return PlaceNotationGenerator.stedman_doubles()
    #
    #     stage_bell = Helpers.convert_to_bell_string(stage)
    #     stage_bell_1 = Helpers.convert_to_bell_string(stage - 1)
    #     stage_bell_2 = Helpers.convert_to_bell_string(stage - 2)
    #
    #     # Note only supporting calls at end of slow sixes
    #     main_body = [stage_bell if i % 2 else "1" for i in range(1, 2 * stage - 1)]
    #     main_body[0] = "3"
    #     notation = f"3.1.{stage_bell}.3.1.3.1.3"
    #     return PlaceNotationGenerator(stage + 1, notation, f"{stage_bell}.1.3.1", f"{stage_bell_2}.1.3.1",
    #                                   f"{stage_bell_2}{stage_bell_1}{stage_bell}.1.3.1")
    #
    # @staticmethod
    # def stedman_doubles():
    #     # Note only supporting singles in quick sixes
    #     notation = "&3.1.5.3.1.3"
    #     return PlaceNotationGenerator(6, notation, "1", "1", "145")
