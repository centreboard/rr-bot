from typing import List

import requests

from RowGeneration.Helpers import Helpers
from RowGeneration.RowGenerator import RowGenerator


class ComplibCompositionReader(RowGenerator):
    complib_url = "https://complib.org/composition/"

    def __init__(self, id: int, auto_start=True, logger=print):

        url = self.complib_url + str(id) + "/rows"
        request_rows = requests.get(url)
        request_rows.raise_for_status()

        # New line separated, skip the first line (rounds)
        split_rows = request_rows.text.splitlines(False)[1::]
        self.loaded_rows = [[Helpers.convert_bell_string(bell) for bell in row] for row in split_rows]

        stage = len(self.loaded_rows[0])
        if stage % 2:
            # Add cover
            stage += 1
            self.loaded_rows = [row.append(stage) for row in self.loaded_rows]
        super().__init__(stage, auto_start, logger)

    def _gen_row(self, previous_row: List[int], is_handstroke: bool, index: int) -> List[int]:
        if index < len(self.loaded_rows):
            return self.loaded_rows[index]
        return self._rounds()
