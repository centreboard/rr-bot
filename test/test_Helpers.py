import unittest

from RowGeneration.Helpers import Helpers


class HelpersBellStringTests(unittest.TestCase):
    def test_convert_bell_string(self):
        self.assertEqual(1, Helpers.convert_bell_string("1"))
        self.assertEqual(9, Helpers.convert_bell_string("9"))

        self.assertEqual(10, Helpers.convert_bell_string("0"))
        self.assertEqual(11, Helpers.convert_bell_string("E"))
        self.assertEqual(12, Helpers.convert_bell_string("T"))

    def test_convert_bell_string_not_found(self):
        with self.assertRaisesRegex(ValueError, "'A' is not known bell symbol"):
            Helpers.convert_bell_string("A")

    def test_convert_to_bell_string(self):
        self.assertEqual("1", Helpers.convert_to_bell_string(1))
        self.assertEqual("9", Helpers.convert_to_bell_string(9))

        self.assertEqual("0", Helpers.convert_to_bell_string(10))
        self.assertEqual("E", Helpers.convert_to_bell_string(11))
        self.assertEqual("T", Helpers.convert_to_bell_string(12))

    def test_convert_to_bell_string_not_found(self):
        with self.assertRaisesRegex(ValueError, "'0' is not known bell number"):
            Helpers.convert_to_bell_string(0)

        with self.assertRaisesRegex(ValueError, "'13' is not known bell number"):
            Helpers.convert_to_bell_string(13)


class HelpersPlaceNotationTests(unittest.TestCase):
    def test_convert_pn_unknown_bell(self):
        with self.assertRaisesRegex(ValueError, "'A' is not known bell symbol"):
            place_notation = "&-A"
            Helpers.convert_pn(place_notation)

    def test_convert_pn_symmetric(self):
        place_notation = "&-1"
        result = Helpers.convert_pn(place_notation)
        self.assertEqual([Helpers.cross_pn, [1], Helpers.cross_pn], result)

    def test_convert_pn_asymmetric(self):
        place_notation = "-1"
        result = Helpers.convert_pn(place_notation)
        self.assertEqual([Helpers.cross_pn, [1]], result)

    def test_convert_pn_multiple_bells(self):
        place_notation = "-123-4"
        result = Helpers.convert_pn(place_notation)
        self.assertEqual([Helpers.cross_pn, [1, 2, 3], Helpers.cross_pn, [4]], result)

    def test_convert_pn_x(self):
        place_notation = "x1"
        result = Helpers.convert_pn(place_notation)
        self.assertEqual([Helpers.cross_pn, [1]], result)

    def test_convert_pn_dot(self):
        place_notation = "x.1.-."
        result = Helpers.convert_pn(place_notation)
        self.assertEqual([Helpers.cross_pn, [1], Helpers.cross_pn], result)

    def test_convert_pn_multiple_bells_and_dots(self):
        place_notation = "12.3-123"
        result = Helpers.convert_pn(place_notation)
        self.assertEqual([[1, 2], [3], Helpers.cross_pn, [1, 2, 3]], result)

    def test_convert_pn_multiple_sections_both_symmetric(self):
        place_notation = "&-1,&2.3"
        result = Helpers.convert_pn(place_notation)
        self.assertEqual([Helpers.cross_pn, [1], Helpers.cross_pn, [2], [3], [2]], result)

    def test_convert_pn_multiple_sections_first_symmetric(self):
        place_notation = "&-1,2.3"
        result = Helpers.convert_pn(place_notation)
        self.assertEqual([Helpers.cross_pn, [1], Helpers.cross_pn, [2], [3]], result)

    def test_convert_pn_multiple_sections_second_symmetric(self):
        place_notation = "-1,&2.3"
        result = Helpers.convert_pn(place_notation)
        self.assertEqual([Helpers.cross_pn, [1], [2], [3], [2]], result)

    def test_convert_pn_multiple_sections_neither_symmetric(self):
        place_notation = "-1,2.3"
        result = Helpers.convert_pn(place_notation)
        self.assertEqual([Helpers.cross_pn, [1], [2], [3]], result)

    def test_convert_pn_multiple_sections_3(self):
        place_notation = "-1,2.3,4"
        result = Helpers.convert_pn(place_notation)
        self.assertEqual([Helpers.cross_pn, [1], [2], [3], [4]], result)


if __name__ == '__main__':
    unittest.main()
