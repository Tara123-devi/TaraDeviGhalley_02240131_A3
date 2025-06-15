import unittest
from TaraDeviGhalley_02240131_A3 import (
    BankAccount,
    InsufficientFundsError,
    InvalidAmountError,
    processUserInput
)

from unittest.mock import patch

class TestBankAccount(unittest.TestCase):
    def setUp(self):
        self.account1 = BankAccount("Sonam", 1000)
        self.account2 = BankAccount("Sangay", 500)

    def test_initial_balance(self):
        self.assertEqual(self.account1.balance, 1000)
        self.assertEqual(self.account2.balance, 500)

    def test_deposit(self):
        self.account1.deposit(200)
        self.assertEqual(self.account1.balance, 1200)
        with self.assertRaises(InvalidAmountError):
            self.account1.deposit(-100)
        with self.assertRaises(InvalidAmountError):
            self.account1.deposit(0)

    def test_withdraw(self):
        self.account1.withdraw(200)
        self.assertEqual(self.account1.balance, 800)
        with self.assertRaises(InsufficientFundsError):
            self.account1.withdraw(2000)
        with self.assertRaises(InvalidAmountError):
            self.account1.withdraw(-100)
        with self.assertRaises(InvalidAmountError):
            self.account1.withdraw(0)

    def test_transfer(self):
        self.account1.transfer(300, self.account2)
        self.assertEqual(self.account1.balance, 700)
        self.assertEqual(self.account2.balance, 800)
        with self.assertRaises(InsufficientFundsError):
            self.account1.transfer(2000, self.account2)
        with self.assertRaises(InvalidAmountError):
            self.account1.transfer(-100, self.account2)
        with self.assertRaises(InvalidAmountError):
            self.account1.transfer(0, self.account2)

    def test_mobile_topup(self):
        self.account1.mobile_topup(100, "17171122")
        self.assertEqual(self.account1.balance, 900)
        with self.assertRaises(InsufficientFundsError):
            self.account1.mobile_topup(2000, "17171122")
        with self.assertRaises(InvalidAmountError):
            self.account1.mobile_topup(-100, "17171122")
        with self.assertRaises(InvalidAmountError):
            self.account1.mobile_topup(0, "17171122")

    def test_transaction_history(self):
        self.account1.deposit(200)
        self.account1.withdraw(100)
        self.account1.transfer(50, self.account2)
        self.account1.mobile_topup(25, "17171122")
        transactions = self.account1.get_transactions()
        self.assertEqual(len(transactions), 4)
        self.assertIn("Deposited: 200", transactions)
        self.assertIn("Withdrew: 100", transactions)
        self.assertIn("Transferred: 50 to Sangay", transactions)
        self.assertIn("Mobile top-up: 25 to 17171122", transactions)

class TestProcessUserInput(unittest.TestCase):
    def setUp(self):
        self.accounts = {
            "Sonam": BankAccount("Sonam", 1000),
            "Sangay": BankAccount("Sangay", 500)
        }

    def test_select_account(self):
        with patch('builtins.input', return_value='Sonam'):
            _, current_account = processUserInput('2', self.accounts, None)
        self.assertIsNotNone(current_account)

    def test_invalid_account(self):
        with patch('builtins.input', return_value='InvalidName'):
            _, current_account = processUserInput('2', self.accounts, None)
        self.assertIsNone(current_account)

    def test_deposit_no_account(self):
        _, current_account = processUserInput('3', self.accounts, None)
        self.assertIsNone(current_account)

    def test_withdraw_no_account(self):
        _, current_account = processUserInput('4', self.accounts, None)
        self.assertIsNone(current_account)

    def test_transfer_no_account(self):
        _, current_account = processUserInput('5', self.accounts, None)
        self.assertIsNone(current_account)

    def test_topup_no_account(self):
        _, current_account = processUserInput('6', self.accounts, None)
        self.assertIsNone(current_account)

    def test_delete_no_account(self):
        _, current_account = processUserInput('7', self.accounts, None)
        self.assertIsNone(current_account)

    def test_view_no_account(self):
        _, current_account = processUserInput('8', self.accounts, None)
        self.assertIsNone(current_account)

    def test_invalid_choice(self):
        accounts, current_account = processUserInput('99', self.accounts, None)
        self.assertEqual(accounts, self.accounts)
        self.assertIsNone(current_account)

if __name__ == "__main__":
    unittest.main()
