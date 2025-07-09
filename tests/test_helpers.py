from unittest import TestCase

from refinedoc.helpers import (
    generate_weights,
    neutralize_arabic_numerals,
    neutralize_roman_numerals,
    unify_list_len,
)


class Test(TestCase):
    def test_unify_list_len(self):
        to_len_unified = [["a", "b", "c"], ["d", "e"], ["f"]]
        unify_list_len(to_len_unified)
        self.assertEqual(
            to_len_unified, [["a", "b", "c"], ["d", "e", ""], ["f", "", ""]]
        )

        to_len_unified = [["a", "b", "c"], ["d", "e"], ["f"]]
        unify_list_len(to_len_unified, at_top=True)
        self.assertEqual(
            to_len_unified, [["a", "b", "c"], ["", "d", "e"], ["", "", "f"]]
        )

    def test_generate_weights(self):
        weights = list(generate_weights(5))
        self.assertEqual(weights, [1.0, 0.75, 0.5, 0.5, 0.5])

        weights = list(generate_weights(2))
        self.assertEqual(weights, [1.0, 0.75])

        weights = list(generate_weights(1))
        self.assertEqual(weights, [1.0])

        weights = list(generate_weights(0))
        self.assertEqual(weights, [None])

    def test_neutralize_arabic_numerals(self):
        self.assertEqual(neutralize_arabic_numerals("abc 1234"), "abc @@@@")
        self.assertEqual(
            neutralize_arabic_numerals("abc 1234", neutral_representation="*"),
            "abc ****",
        )

        self.assertEqual(neutralize_arabic_numerals("abc 1 2 3 4"), "abc @ @ @ @")

    def test_neutralize_roman_numerals(self):
        self.assertEqual(neutralize_roman_numerals("BMC IV"), "BMC @")
        self.assertEqual(neutralize_roman_numerals("abc iv"), "abc @")
        self.assertEqual(neutralize_roman_numerals("abc iV"), "abc @")
        self.assertEqual(neutralize_roman_numerals("vrai i v"), "vrai @ @")

        self.assertEqual(
            neutralize_roman_numerals("abc IV", neutral_representation="*"), "abc *"
        )
        self.assertEqual(
            neutralize_roman_numerals("abc i v", neutral_representation="*"),
            "abc * *",
        )
