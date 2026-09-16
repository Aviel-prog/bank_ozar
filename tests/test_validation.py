"""Logics._validate_amount and Logics._validate_date."""

import unittest

from src.exceptions import InvalidAmountError, InvalidDateError
from src.logics.logics import Logics


class ValidateAmountTests(unittest.TestCase):
    def test_accepts_whole_numbers_in_any_form(self):
        for given, expected in (("100", 100), (100, 100), ("  50  ", 50), ("1", 1)):
            with self.subTest(given=given):
                self.assertEqual(Logics._validate_amount(given), expected)

    def test_rejects_zero_and_negatives(self):
        for given in ("0", 0, "-5", -1):
            with self.subTest(given=given):
                with self.assertRaises(InvalidAmountError):
                    Logics._validate_amount(given)

    def test_rejects_anything_that_is_not_a_whole_number(self):
        for given in ("abc", "10.5", "", None, "1e3", "١٠٠٠٠٠"[0:0] or "  "):
            with self.subTest(given=given):
                with self.assertRaises(InvalidAmountError):
                    Logics._validate_amount(given)

    def test_error_names_the_offending_value(self):
        with self.assertRaises(InvalidAmountError) as raised:
            Logics._validate_amount("abc")
        self.assertIn("abc", str(raised.exception))


class ValidateDateTests(unittest.TestCase):
    def test_accepts_a_real_date_in_the_expected_format(self):
        self.assertEqual(Logics._validate_date("25-12-2027"), "25-12-2027")

    def test_rejects_the_wrong_field_order(self):
        with self.assertRaises(InvalidDateError):
            Logics._validate_date("2027-12-25")

    def test_rejects_dates_that_do_not_exist(self):
        for given in ("32-01-2027", "29-02-2027", "00-01-2027", "01-13-2027"):
            with self.subTest(given=given):
                with self.assertRaises(InvalidDateError):
                    Logics._validate_date(given)

    def test_rejects_non_dates(self):
        for given in ("tomorrow", "", None):
            with self.subTest(given=given):
                with self.assertRaises(InvalidDateError):
                    Logics._validate_date(given)

    def test_accepts_a_leap_day_in_a_leap_year(self):
        self.assertEqual(Logics._validate_date("29-02-2028"), "29-02-2028")


if __name__ == "__main__":
    unittest.main()
