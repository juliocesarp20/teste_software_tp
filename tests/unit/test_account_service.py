

import pytest
from unittest.mock import Mock
from model.account import Account, BudgetException
from model.currency import Currency
from services.account_service import AccountService

class MockCurrency(Currency):
    def __init__(self, value, name):
        super().__init__(value, name)

@pytest.fixture
def account():
    currency = MockCurrency(1, "FakeCurrency")
    return Account(initial_balance=100, currency=currency)

@pytest.fixture
def account_repository_mock():
    return Mock()

@pytest.fixture
def account_service(account_repository_mock):
    return AccountService(account_repository_mock)

def test_account_withdraw_entire_balance(account_service, account_repository_mock):
    currency = MockCurrency(1, "FakeCurrency")
    account = Account(initial_balance=150, currency=currency)
    account_repository_mock.get_account_by_id.return_value = account
    account_service.withdraw(1, 150)
    account = Account(initial_balance=0, currency=currency)
    account_repository_mock.get_account_by_id.return_value = account
    assert account_service.get_balance(1) == 0
    account_repository_mock.withdraw_funds.assert_called_with(1, 150)

def test_account_initial_balance(account_service, account, account_repository_mock):
    account_repository_mock.get_account_by_id.return_value = account

    assert account_service.get_balance(1) == 100
    account_repository_mock.get_account_by_id.assert_called_with(1)

def test_account_valid_deposit(account_service, account_repository_mock):
    currency = MockCurrency(1, "FakeCurrency")
    account = Account(initial_balance=150, currency=currency)
    account_repository_mock.get_account_by_id.return_value = account

    account_service.deposit(1, 50)

    assert account_service.get_balance(1) == 150
    account_repository_mock.deposit_funds.assert_called_with(1, 50)

def test_account_invalid_deposit_zero_amount(account_service, account, account_repository_mock):
    account_repository_mock.get_account_by_id.return_value = account

    with pytest.raises(BudgetException, match="Invalid deposit amount. Amount must be greater than zero."):
        account_service.deposit(1, 0)

def test_account_invalid_deposit_negative_amount(account_service, account, account_repository_mock):
    account_repository_mock.get_account_by_id.return_value = account

    with pytest.raises(BudgetException, match="Invalid deposit amount. Amount must be greater than zero."):
        account_service.deposit(1, -50)

def test_account_valid_withdrawal(account_service, account, account_repository_mock):
    account_repository_mock.get_account_by_id.return_value = account
    currency = MockCurrency(1, "FakeCurrency")

    account_service.withdraw(1, 50)

    account = Account(initial_balance=100, currency=currency)
    account_repository_mock.get_account_by_id.return_value = account

    assert account.get_balance() == 100
    account_repository_mock.withdraw_funds.assert_called_with(1, 50)

def test_account_invalid_withdrawal_zero_amount(account_service, account, account_repository_mock):
    account_repository_mock.get_account_by_id.return_value = account

    with pytest.raises(BudgetException, match="Invalid withdrawal amount. Amount must be greater than zero."):
        account_service.withdraw(1, 0)

def test_account_invalid_withdrawal_negative_amount(account_service, account, account_repository_mock):
    account_repository_mock.get_account_by_id.return_value = account

    with pytest.raises(BudgetException, match="Invalid withdrawal amount. Amount must be greater than zero."):
        account_service.withdraw(1, -50)

def test_account_invalid_withdrawal_insufficient_funds(account_service, account, account_repository_mock):
    account_repository_mock.get_account_by_id.return_value = account

    with pytest.raises(BudgetException, match="Insufficient funds. Cannot withdraw more than the available balance."):
        account_service.withdraw(1, 150)