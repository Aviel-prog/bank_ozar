"""Balance, deposit, withdrawal, subscriptions and closing an account."""

import datetime
import unittest
from unittest import mock

from src.exceptions import InvalidAmountError, InvalidDateError
from src.logics import red_rules
from src.logics.base_rules import AccountRules
from src.logics.blue_rules import BlueAccountRules
from src.logics.green_rules import GreenAccountRules
from src.logics.logics import Logics
from src.logics.yellow_rules import YellowAccountRules
from src.models import AccountType
from tests.support import StorageTestCase, account


class LockedAccountTests(StorageTestCase):
    """A locked account is turned away before any rule is consulted."""

    def setUp(self):
        super().setUp()
        self.locked = self.given_account("t_locked", 1000, AccountType.RED, locked=True)

    def test_every_money_operation_reports_locked(self):
        self.assertEqual(Logics.get_balance(self.locked), "locked")
        self.assertEqual(Logics.add_money(self.locked, 50), "locked")
        self.assertEqual(Logics.get_money(self.locked, 50), "locked")
        self.assertEqual(
            Logics.add_subscription(self.locked, "Gym", "01-01-2030", 50), "locked")

    def test_a_locked_account_is_never_written_to(self):
        Logics.add_money(self.locked, 50)
        Logics.get_money(self.locked, 50)
        self.assertEqual(self.storage.called("update_balance"), [])


class DefaultRulesTests(StorageTestCase):
    def setUp(self):
        super().setUp()
        self.account = self.given_account("t_base", 500, AccountType.RED)

    def test_balance_is_reported_from_the_account(self):
        self.assertEqual(AccountRules.get_balance(self.account), "500 in your bank")

    def test_a_deposit_updates_the_object_and_storage(self):
        AccountRules.add_money(self.account, 250)
        self.assertEqual(self.account.balance, 750)
        self.assertEqual(self.storage.called("update_balance"),
                         [("update_balance", "t_base", 750)])

    def test_a_withdrawal_updates_the_object_and_storage(self):
        AccountRules.get_money(self.account, 200)
        self.assertEqual(self.account.balance, 300)
        self.assertEqual(self.storage.called("update_balance"),
                         [("update_balance", "t_base", 300)])

    def test_the_amount_is_validated_before_anything_moves(self):
        for bad in ("abc", "0", "-5"):
            with self.subTest(amount=bad):
                with self.assertRaises(InvalidAmountError):
                    Logics.add_money(self.account, bad)
        self.assertEqual(self.account.balance, 500)


class BlueRulesTests(StorageTestCase):
    def setUp(self):
        super().setUp()
        self.account = self.given_account("t_blue", 500, AccountType.BLUE)

    def test_a_withdrawal_over_the_cap_is_refused_and_changes_nothing(self):
        self.assertEqual(BlueAccountRules.get_money(self.account, 101),
                         "you cant get more than 100")
        self.assertEqual(self.account.balance, 500)
        self.assertEqual(self.storage.called("update_balance"), [])

    def test_a_withdrawal_at_the_cap_goes_through(self):
        BlueAccountRules.get_money(self.account, 100)
        self.assertEqual(self.account.balance, 400)


class RedRulesTests(StorageTestCase):
    def setUp(self):
        super().setUp()
        self.account = self.given_account("t_red", 500, AccountType.RED)

    def _on_day(self, day: int):
        """Pins today's date so the odd/even rule is not a coin toss."""
        frozen = mock.MagicMock()
        frozen.date.today.return_value = datetime.date(2026, 1, day)
        return mock.patch.object(red_rules, "datetime", frozen)

    def test_large_deposits_are_refused_on_an_odd_day(self):
        with self._on_day(3):
            self.assertEqual(red_rules.RedAccountRules.add_money(self.account, 301),
                             "no more than 300 on odd day")
        self.assertEqual(self.account.balance, 500)

    def test_the_same_deposit_is_allowed_on_an_even_day(self):
        with self._on_day(4):
            red_rules.RedAccountRules.add_money(self.account, 301)
        self.assertEqual(self.account.balance, 801)

    def test_a_small_deposit_is_fine_on_an_odd_day(self):
        with self._on_day(3):
            red_rules.RedAccountRules.add_money(self.account, 300)
        self.assertEqual(self.account.balance, 800)


class GreenRulesTests(StorageTestCase):
    def setUp(self):
        super().setUp()
        self.account = self.given_account("t_green", 10, AccountType.GREEN)

    def test_reading_the_balance_credits_two(self):
        self.assertEqual(GreenAccountRules.get_balance(self.account), "12 in your bank")
        self.assertEqual(self.account.balance, 12)

    def test_the_credit_is_persisted(self):
        GreenAccountRules.get_balance(self.account)
        self.assertEqual(self.storage.called("update_balance"),
                         [("update_balance", "t_green", 12)])


class YellowRulesTests(StorageTestCase):
    def setUp(self):
        super().setUp()
        self.account = self.given_account("t_yellow", 50, AccountType.YELLOW)

    def test_a_withdrawal_that_stays_positive_is_ordinary(self):
        self.assertEqual(YellowAccountRules.get_money(self.account, 30),
                         "got the money successfully")
        self.assertEqual(self.storage.called("update_lock"), [])

    def test_going_below_zero_locks_the_account_in_storage(self):
        message = YellowAccountRules.get_money(self.account, 80)
        self.assertEqual(message, "you have less than 0 in your account now")
        self.assertEqual(self.account.balance, -30)
        self.assertEqual(self.storage.called("update_lock"),
                         [("update_lock", "t_yellow", True)])

    def test_going_below_zero_also_locks_the_object_in_hand(self):
        """The lock has to reach the object the session keeps using.

        Writing it only to the database would leave this object reporting
        itself unlocked, and every later check would wave the customer
        through until they reconnected.
        """
        YellowAccountRules.get_money(self.account, 80)
        self.assertTrue(self.account.locked)

    def test_an_ordinary_withdrawal_leaves_the_account_unlocked(self):
        YellowAccountRules.get_money(self.account, 30)
        self.assertFalse(self.account.locked)


class SubscriptionTests(StorageTestCase):
    def setUp(self):
        super().setUp()
        self.account = self.given_account("t_sub", 500, AccountType.RED)

    def test_adding_one(self):
        self.assertEqual(Logics.add_subscription(self.account, "Gym", "01-06-2028", 50),
                         "the subscription Gym added successfully")
        self.assertEqual(self.storage.get_subscriptions("t_sub"),
                         [("Gym", "01-06-2028", 50)])

    def test_adding_the_same_one_twice(self):
        Logics.add_subscription(self.account, "Gym", "01-06-2028", 50)
        self.assertEqual(Logics.add_subscription(self.account, "Gym", "01-06-2028", 50),
                         "subscription Gym already exists")

    def test_a_bad_date_is_refused_before_it_reaches_storage(self):
        with self.assertRaises(InvalidDateError):
            Logics.add_subscription(self.account, "Gym", "2028-06-01", 50)
        self.assertEqual(self.storage.called("add_subscription"), [])

    def test_a_bad_amount_is_refused_before_it_reaches_storage(self):
        with self.assertRaises(InvalidAmountError):
            Logics.add_subscription(self.account, "Gym", "01-06-2028", "free")
        self.assertEqual(self.storage.called("add_subscription"), [])

    def test_removing_one(self):
        Logics.add_subscription(self.account, "Gym", "01-06-2028", 50)
        self.assertEqual(Logics.del_subscription(self.account, "Gym"),
                         "the subscription Gym deleted successfully")
        self.assertEqual(self.storage.get_subscriptions("t_sub"), [])

    def test_removing_one_that_was_never_there(self):
        self.assertEqual(Logics.del_subscription(self.account, "Gym"),
                         "No subscription found matching Gym.")

    def test_listing_them(self):
        Logics.add_subscription(self.account, "Gym", "01-06-2028", 50)
        self.assertEqual(Logics.subscription_list(self.account),
                         [("Gym", "01-06-2028", 50)])


class DeleteAccountTests(StorageTestCase):
    def setUp(self):
        super().setUp()
        self.account = self.given_account("t_gone", 500, AccountType.RED)
        self.given_account("t_stays", 10, AccountType.BLUE)
        self.storage.subscriptions = [
            ("t_gone", "Gym", "01-06-2028", 50),
            ("t_gone", "Dudu", "01-06-2028", -1000),
            ("t_stays", "Cloud", "01-06-2028", 10),
        ]

    def test_closing_reports_success(self):
        self.assertEqual(Logics.del_account(self.account),
                         (True, "Account 't_gone' deleted successfully."))

    def test_closing_takes_the_subscriptions_with_it(self):
        Logics.del_account(self.account)
        self.assertEqual(self.storage.get_subscriptions("t_gone"), [])

    def test_another_customer_is_untouched(self):
        Logics.del_account(self.account)
        self.assertEqual(self.storage.get_subscriptions("t_stays"),
                         [("Cloud", "01-06-2028", 10)])
        self.assertIn("t_stays", self.storage.accounts)

    def test_subscriptions_go_before_the_account(self):
        """Order matters: a failure must not orphan rows a re-registration inherits."""
        Logics.del_account(self.account)
        methods = [call[0] for call in self.storage.calls]
        self.assertLess(methods.index("delete_subscriptions"),
                        methods.index("delete_account"))

    def test_closing_an_account_that_is_not_there(self):
        self.assertEqual(Logics.del_account(account("nobody")),
                         (False, "Account 'nobody' not found."))


if __name__ == "__main__":
    unittest.main()
