"""Each colour's registration criteria, tested without touching storage."""

import unittest

from src.logics.base_rules import AccountRules
from src.logics.blue_rules import BlueAccountRules
from src.logics.green_rules import GreenAccountRules
from src.logics.red_rules import RedAccountRules
from src.logics.yellow_rules import YellowAccountRules
from tests.support import BLUE_PERSON, GREEN_PERSON, RED_PERSON, YELLOW_PERSON, person


class BaseRulesTests(unittest.TestCase):
    def test_the_default_claims_nobody(self):
        self.assertFalse(AccountRules.qualifies(person()))

    def test_the_default_onboarding_does_nothing(self):
        self.assertIsNone(AccountRules.on_register(object(), person()))

    def test_the_default_opening_balance_is_zero(self):
        self.assertEqual(AccountRules.INITIAL_BALANCE, 0)


class BlueQualifiesTests(unittest.TestCase):
    def test_permanent_service_with_three_and_five_in_the_phone(self):
        self.assertTrue(BlueAccountRules.qualifies(BLUE_PERSON))

    def test_rejects_non_permanent_service(self):
        self.assertFalse(BlueAccountRules.qualifies(
            person(serviceType="חובה", phone="03-5551234")))

    def test_needs_both_digits(self):
        for phone in ("0300000", "0500000", "0000000"):
            with self.subTest(phone=phone):
                self.assertFalse(BlueAccountRules.qualifies(
                    person(serviceType="קבע", phone=phone)))

    def test_opening_balance(self):
        self.assertEqual(BlueAccountRules.INITIAL_BALANCE, 1700)


class RedQualifiesTests(unittest.TestCase):
    def test_final_nun_in_family_name_and_a_listed_department(self):
        self.assertTrue(RedAccountRules.qualifies(RED_PERSON))
        self.assertTrue(RedAccountRules.qualifies(
            person(lastName="לוין", department="אלנקטרוניקה")))

    def test_rejects_an_unlisted_department(self):
        self.assertFalse(RedAccountRules.qualifies(
            person(lastName="לוין", department="אחר")))

    def test_rejects_a_family_name_without_the_final_nun(self):
        self.assertFalse(RedAccountRules.qualifies(
            person(lastName="כהן"[0:2], department="פסיפס")))

    def test_opening_balance(self):
        self.assertEqual(RedAccountRules.INITIAL_BALANCE, 30000)


class GreenQualifiesTests(unittest.TestCase):
    def test_a_qualifying_rank_and_a_yod_in_the_first_name(self):
        for rank in ("סמל", "סמר", "רבט"):
            with self.subTest(rank=rank):
                self.assertTrue(GreenAccountRules.qualifies(
                    person(rank=rank, firstName="יוסי")))

    def test_rejects_an_unlisted_rank(self):
        self.assertFalse(GreenAccountRules.qualifies(
            person(rank="טוראי", firstName="יוסי")))

    def test_rejects_a_first_name_without_a_yod(self):
        self.assertFalse(GreenAccountRules.qualifies(
            person(rank="סמל", firstName="דן")))

    def test_opening_balance(self):
        self.assertEqual(GreenAccountRules.INITIAL_BALANCE, 0)


class YellowQualifiesTests(unittest.TestCase):
    def test_a_nickname_is_enough_on_its_own(self):
        self.assertTrue(YellowAccountRules.qualifies(YELLOW_PERSON))

    def test_male_in_a_tav_organization_is_the_other_way_in(self):
        self.assertTrue(YellowAccountRules.qualifies(
            person(gender="M", organization="תקשוב")))

    def test_needs_both_halves_of_the_second_route(self):
        self.assertFalse(YellowAccountRules.qualifies(
            person(gender="F", organization="תקשוב")))
        self.assertFalse(YellowAccountRules.qualifies(
            person(gender="M", organization="אחר")))

    def test_rejects_someone_with_neither(self):
        self.assertFalse(YellowAccountRules.qualifies(person()))

    def test_opening_balance(self):
        self.assertEqual(YellowAccountRules.INITIAL_BALANCE, 0)


class CriteriaAreDistinctTests(unittest.TestCase):
    """The design assumes a person lands in exactly one colour."""

    def test_each_sample_person_matches_only_their_own_colour(self):
        rules = {
            "blue": (BlueAccountRules, BLUE_PERSON),
            "red": (RedAccountRules, RED_PERSON),
            "green": (GreenAccountRules, GREEN_PERSON),
            "yellow": (YellowAccountRules, YELLOW_PERSON),
        }
        for name, (_, record) in rules.items():
            matched = [other for other, (klass, _) in rules.items()
                       if klass.qualifies(record)]
            with self.subTest(person=name):
                self.assertEqual(matched, [name])


if __name__ == "__main__":
    unittest.main()
