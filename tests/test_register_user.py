"""Logics.register_user - who gets an account, of which colour, and with what."""

import datetime
import unittest
from unittest import mock

from dateutil.relativedelta import relativedelta

from src.config import SUBSCRIPTION_DATE_FORMAT
from src.exceptions import (
    AccountAlreadyExistsError,
    NoQualifyingAccountTypeError,
    PersonNotFoundError,
    RegistrationError,
)
from src.logics.logics import Logics
from src.models import AccountType
from tests.support import (BLUE_PERSON, GREEN_PERSON, RED_PERSON, YELLOW_PERSON,
                           StorageTestCase, account, person)


class RegisterUserTestCase(StorageTestCase):
    """Base that points the directory at a fixed list of people."""

    directory: list = []

    def setUp(self):
        super().setUp()
        patcher = mock.patch("src.logics.services.get_people_list_from_web",
                             return_value=self.directory)
        patcher.start()
        self.addCleanup(patcher.stop)


class ColourAssignmentTests(RegisterUserTestCase):
    directory = [BLUE_PERSON, RED_PERSON, GREEN_PERSON, YELLOW_PERSON]

    def test_each_person_gets_their_colour_and_opening_balance(self):
        expected = {
            "p_blue": (AccountType.BLUE, 1700),
            "p_red": (AccountType.RED, 30000),
            "p_green": (AccountType.GREEN, 0),
            "p_yellow": (AccountType.YELLOW, 0),
        }
        for username, (account_type, balance) in expected.items():
            with self.subTest(username=username):
                created = Logics.register_user(username)
                self.assertEqual(created.account_type, account_type)
                self.assertEqual(created.balance, balance)
                self.assertEqual(created.username, username)

    def test_a_new_account_is_never_locked(self):
        self.assertFalse(Logics.register_user("p_blue").locked)

    def test_the_account_is_persisted(self):
        Logics.register_user("p_green")
        stored = self.storage.get_user_information("p_green")
        self.assertEqual(stored.account_type, AccountType.GREEN)


class PrecedenceTests(RegisterUserTestCase):
    """Red's rule reads "if blue does not match", which is the dict's order."""

    directory = [person("p_both", serviceType="קבע", phone="03-5551234",
                        lastName="לוין", department="פסיפס")]

    def test_blue_wins_over_red_when_a_person_matches_both(self):
        self.assertEqual(Logics.register_user("p_both").account_type, AccountType.BLUE)


class OnboardingTests(RegisterUserTestCase):
    directory = [BLUE_PERSON, RED_PERSON, GREEN_PERSON, YELLOW_PERSON]

    def test_red_opens_with_the_dudu_subscription(self):
        Logics.register_user("p_red")
        expected_end = (datetime.date.today()
                        + relativedelta(months=30)).strftime(SUBSCRIPTION_DATE_FORMAT)
        self.assertEqual(self.storage.get_subscriptions("p_red"),
                         [("Dudu", expected_end, -1000)])

    def test_yellow_opens_with_an_open_ended_subscription(self):
        Logics.register_user("p_yellow")
        (name, end_date, amount), = self.storage.get_subscriptions("p_yellow")
        self.assertEqual(name, "Yellow")
        self.assertEqual(end_date, "01-01-9999")
        self.assertTrue(-1500 <= amount <= -100, f"{amount} outside the drawn range")

    def test_blue_and_green_open_with_nothing(self):
        for username in ("p_blue", "p_green"):
            with self.subTest(username=username):
                Logics.register_user(username)
                self.assertEqual(self.storage.get_subscriptions(username), [])


class FailureTests(RegisterUserTestCase):
    directory = [BLUE_PERSON, person("p_none")]

    def test_a_username_the_directory_does_not_know(self):
        with self.assertRaises(PersonNotFoundError) as raised:
            Logics.register_user("ghost")
        self.assertIn("ghost", str(raised.exception))

    def test_someone_who_meets_no_criteria(self):
        with self.assertRaises(NoQualifyingAccountTypeError):
            Logics.register_user("p_none")

    def test_a_username_that_is_already_taken(self):
        Logics.register_user("p_blue")
        with self.assertRaises(AccountAlreadyExistsError):
            Logics.register_user("p_blue")

    def test_every_failure_is_one_family(self):
        for username in ("ghost", "p_none"):
            with self.subTest(username=username):
                with self.assertRaises(RegistrationError):
                    Logics.register_user(username)

    def test_nothing_is_written_when_registration_fails(self):
        with self.assertRaises(NoQualifyingAccountTypeError):
            Logics.register_user("p_none")
        self.assertEqual(self.storage.called("add_account"), [])


class ConnectUserTests(RegisterUserTestCase):
    directory = [BLUE_PERSON]
    accounts = {"t_known": account("t_known", 500, AccountType.GREEN)}

    def test_an_existing_customer_is_loaded_not_registered(self):
        loaded = Logics.connect_user("t_known")
        self.assertEqual(loaded.balance, 500)
        self.assertEqual(self.storage.called("add_account"), [])

    def test_an_unknown_customer_falls_through_to_registration(self):
        created = Logics.connect_user("p_blue")
        self.assertEqual(created.account_type, AccountType.BLUE)

    def test_a_stranger_raises_rather_than_returning_none(self):
        with self.assertRaises(PersonNotFoundError):
            Logics.connect_user("ghost")


if __name__ == "__main__":
    unittest.main()
