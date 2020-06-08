import unittest
from unittest import TestCase

from RowGeneration.PlaceNotationGenerator import PlaceNotationGenerator
from RowGeneration.PlainHuntGenerator import PlainHuntGenerator
from test.GeneratorTestBase import GeneratorTestBase


class PlaceNotationGeneratorTests(GeneratorTestBase):

    def test_plain_bob_minimus(self):
        stage = 4

        generator = PlaceNotationGenerator(stage, "&x1x1,2", auto_start=True)

        self.initial_rounds(generator, stage)
        rows = self.gen_rows(generator, 8)
        self.assertEqual([[2, 1, 4, 3],
                          [2, 4, 1, 3],
                          [4, 2, 3, 1],
                          [4, 3, 2, 1],
                          [3, 4, 1, 2],
                          [3, 1, 4, 2],
                          [1, 3, 2, 4],
                          [1, 3, 4, 2]],
                         rows)

    def test_plain_bob_minimus_bob(self):
        stage = 4

        generator = PlaceNotationGenerator(stage, "&x1x1,2", auto_start=True)

        self.initial_rounds(generator, stage)
        rows = self.gen_rows(generator, 6)
        generator.bob()
        for row in self.gen_rows(generator, 2):
            rows.append(row)

        self.assertEqual([[2, 1, 4, 3],
                          [2, 4, 1, 3],
                          [4, 2, 3, 1],
                          [4, 3, 2, 1],
                          [3, 4, 1, 2],
                          [3, 1, 4, 2],
                          [1, 3, 2, 4],
                          [1, 2, 3, 4]],
                         rows)

    def test_plain_bob_minimus_single(self):
        stage = 4

        generator = PlaceNotationGenerator(stage, "&x1x1,2", auto_start=True)

        self.initial_rounds(generator, stage)
        rows = self.gen_rows(generator, 6)
        generator.single()
        for row in self.gen_rows(generator, 2):
            rows.append(row)

        self.assertEqual([[2, 1, 4, 3],
                          [2, 4, 1, 3],
                          [4, 2, 3, 1],
                          [4, 3, 2, 1],
                          [3, 4, 1, 2],
                          [3, 1, 4, 2],
                          [1, 3, 2, 4],
                          [1, 3, 2, 4]],
                         rows)

    def test_plain_bob_doubles_plain(self):
        stage = 5

        generator = PlaceNotationGenerator(stage, "&5.1.5.1.5,2", auto_start=True)

        self.initial_rounds(generator, stage)
        rows = self.gen_rows(generator, 10)

        self.assertEqual([[2, 1, 4, 3, 5, 6],
                          [2, 4, 1, 5, 3, 6],
                          [4, 2, 5, 1, 3, 6],
                          [4, 5, 2, 3, 1, 6],
                          [5, 4, 3, 2, 1, 6],
                          [5, 3, 4, 1, 2, 6],
                          [3, 5, 1, 4, 2, 6],
                          [3, 1, 5, 2, 4, 6],
                          [1, 3, 2, 5, 4, 6],
                          [1, 3, 5, 2, 4, 6]],
                         rows)

    def test_plain_bob_doubles_two_bobs(self):
        stage = 5

        generator = PlaceNotationGenerator(stage, "&5.1.5.1.5,2", auto_start=True)

        self.initial_rounds(generator, stage)
        self.gen_rows(generator, 8)
        generator.bob()
        first_lead_end = self.gen_rows(generator, 2)
        # 4ths made at bob
        self.assertEqual([[1, 3, 2, 5, 4, 6], [1, 2, 3, 5, 4, 6]], first_lead_end)

        self.gen_rows(generator, 8)
        generator.bob()
        second_lead_end = self.gen_rows(generator, 2)
        # 4ths made at bob
        self.assertEqual([[1, 3, 2, 4, 5, 6], [1, 2, 3, 4, 5, 6]], second_lead_end)

    def test_resets_call_after_bob(self):
        stage = 5

        generator = PlaceNotationGenerator(stage, "&5.1.5.1.5,2", auto_start=True)

        self.initial_rounds(generator, stage)
        self.gen_rows(generator, 8)
        generator.bob()
        first_lead_end = self.gen_rows(generator, 2)
        # 4ths made at bob
        self.assertEqual([[1, 3, 2, 5, 4, 6], [1, 2, 3, 5, 4, 6]], first_lead_end)

        self.gen_rows(generator, 8)
        second_lead_end = self.gen_rows(generator, 2)
        # 2nds made at plain lead
        self.assertEqual([[1, 3, 2, 4, 5, 6], [1, 3, 4, 2, 5, 6]], second_lead_end)

    def test_stedman_doubles_plain(self):
        stage = 5

        generator = PlaceNotationGenerator.stedman_doubles()

        self.initial_rounds(generator, stage)
        rows = self.gen_rows(generator, 12)

        self.assertEqual([[2, 1, 3, 5, 4, 6],
                          [2, 3, 1, 4, 5, 6],
                          [3, 2, 4, 1, 5, 6],
                          [2, 3, 4, 5, 1, 6],
                          [2, 4, 3, 1, 5, 6],
                          [4, 2, 3, 5, 1, 6],
                          [4, 3, 2, 1, 5, 6],
                          [3, 4, 2, 5, 1, 6],
                          [4, 3, 5, 2, 1, 6],
                          [4, 5, 3, 1, 2, 6],
                          [5, 4, 3, 2, 1, 6],
                          [5, 3, 4, 1, 2, 6]],
                         rows)

    def test_stedman_doubles_first_single(self):
        stage = 5

        generator = PlaceNotationGenerator.stedman_doubles()

        self.initial_rounds(generator, stage)
        initial_rows = self.gen_rows(generator, 4)
        generator.single()
        single_rows = self.gen_rows(generator, 2)
        after_rows = self.gen_rows(generator, 6)


        self.assertEqual([[2, 1, 3, 5, 4, 6],
                          [2, 3, 1, 4, 5, 6],
                          [3, 2, 4, 1, 5, 6],
                          [2, 3, 4, 5, 1, 6]],
                         initial_rows)
        self.assertEqual([[2, 4, 3, 1, 5, 6],
                          [4, 2, 3, 1, 5, 6]],
                         single_rows)
        self.assertEqual([[4, 3, 2, 5, 1, 6],
                          [3, 4, 2, 1, 5, 6],
                          [4, 3, 1, 2, 5, 6],
                          [4, 1, 3, 5, 2, 6],
                          [1, 4, 3, 2, 5, 6],
                          [1, 3, 4, 5, 2, 6]],
                         after_rows)

    def test_stedman_doubles_second_single(self):
        stage = 5

        generator = PlaceNotationGenerator.stedman_doubles()

        self.initial_rounds(generator, stage)
        self.gen_rows(generator, 10)
        generator.single()
        single_rows = self.gen_rows(generator, 2)

        self.assertEqual([[5, 4, 3, 2, 1, 6],
                          [5, 3, 4, 2, 1, 6]],
                         single_rows)


if __name__ == '__main__':
    unittest.main()