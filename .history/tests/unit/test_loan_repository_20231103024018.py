import pytest
from account import Account, BudgetException
from currency import Currency


class MockCurrency(Currency):
    def __init__(self, value, name):
        super().__init__(value, name)


@pytest.fixture
def account():
    currency = MockCurrency(1, "FakeCurrency")
    return Account(initial_balance=100, currency=currency)


def test_account_initial_balance(account):
    assert str(account.get_balance()) == "100"

def test_account_withdraw_entire_balance(account):
    account.withdraw(100)
    assert str(account.get_balance()) == "0"

def test_account_valid_deposit(account):
    account.deposit(50)
    assert str(account.get_balance()) == "150"


def test_account_invalid_deposit_zero_amount(account):
    with pytest.raises(BudgetException,
                       str("Invalid deposit amount. Amount must be greater than zero.")):
        account.deposit(0)


def test_account_invalid_deposit_negative_amount(account):
    with pytest.raises(BudgetException,
                       str("Invalid deposit amount. Amount must be greater than zero.")):
        account.deposit(-50)


def test_account_valid_withdrawal(account):
    account.withdraw(50)
    assert str(account.get_balance()) == "50"


def test_account_invalid_withdrawal_zero_amount(account):
    with pytest.raises(BudgetException,
                       str("Invalid withdrawal amount. Amount must be greater than zero.")):
        account.withdraw(0)


def test_account_invalid_withdrawal_negative_amount(account):
    with pytest.raises(BudgetException,
                       str("Invalid withdrawal amount. Amount must be greater than zero.")):
        account.withdraw(-50)


def test_account_invalid_withdrawal_insufficient_funds(account):
    with pytest.raises(BudgetException,
                       str("Insufficient funds. Cannot withdraw more than the "
                             "available balance.")):
        account.withdraw(150)
