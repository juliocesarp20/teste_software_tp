import pytest
from unittest.mock import Mock
from model.loan import Loan
from repository.loan_repository import LoanRepository

@pytest.fixture
def user_repository_mock():
    user_repository = Mock()
    user_repository.get_user_by_id = Mock()
    return user_repository


@pytest.fixture
def loan_repository_fixture(user_repository_mock):
    return LoanRepository(user_repository_mock)

def test_create_loan(loan_repository_fixture, user_repository_mock):
    user_id = 1
    amount = 1000
    interest_rate = 0.1
    term_months = 12

    user_repository_mock.get_user_by_id.return_value = user_id

    loan = loan_repository_fixture.create_loan(user_id, amount, interest_rate, term_months)

    assert isinstance(loan, Loan)
    assert loan.get_user_id() == user_id

def test_create_loan(loan_repository_fixture, user_repository_mock):
    user_id = 1
    amount = 1000
    interest_rate = 0.1
    term_months = 12

    user_repository_mock.get_user_by_id.return_value = user_id

    loan = loan_repository_fixture.create_loan(user_id, amount, interest_rate, term_months)

    assert isinstance(loan, Loan)
    assert loan.get_user_id() == user_id

def test_create_loan_with_invalid_user(loan_repository_fixture,user_repository_mock):
    user_id = 1  
    amount = 1000
    interest_rate = 0.1
    term_months = 12

    user_repository_mock.get_user_by_id.return_value = None

    with pytest.raises(ValueError, match="User does not exist. Cannot create a loan for a non-existent user."):
        loan_repository_fixture.create_loan(user_id, amount, interest_rate, term_months)

def test_create_loan_with_negative_amount(loan_repository_fixture, user_repository_mock):
    user_id = 1
    amount = -100
    interest_rate = 0.1
    term_months = 12

    user_repository_mock.get_user_by_id.return_value = user_id

    with pytest.raises(ValueError, match="Loan amount must be greater than zero."):
        loan_repository_fixture.create_loan(user_id, amount, interest_rate, term_months)

def test_create_loan_with_invalid_interest_rate(loan_repository_fixture, user_repository_mock):
    user_id = 1
    amount = 1000
    interest_rate = -0.1
    term_months = 12

    user_repository_mock.get_user_by_id.return_value = user_id

    with pytest.raises(ValueError, match="Interest rate must be between 0 and 1."):
        loan_repository_fixture.create_loan(user_id, amount, interest_rate, term_months)

def test_create_loan_with_zero_months(loan_repository_fixture, user_repository_mock):
    user_id = 1
    amount = 1000
    interest_rate = 0.1
    term_months = 0 

    user_repository_mock.get_user_by_id.return_value = user_id

    with pytest.raises(ValueError, match="Loan term must be greater than zero."):
        loan_repository_fixture.create_loan(user_id, amount, interest_rate, term_months)


def test_create_loan_with_zero_amount(loan_repository_fixture, user_repository_mock):
    user_id = 1
    amount = 0
    interest_rate = 0.1
    term_months = 12

    user_repository_mock.get_user_by_id.return_value = user_id

    with pytest.raises(ValueError, match="Loan amount must be greater than zero."):
        loan_repository_fixture.create_loan(user_id, amount, interest_rate, term_months)



def test_get_loans_by_user_id(loan_repository_fixture,user_repository_mock):
    user_id = 1
    amount = 1000
    interest_rate = 0.1
    term_months = 12

    user_repository_mock.get_user_by_id.return_value = user_id

    loan = loan_repository_fixture.create_loan(user_id, amount, interest_rate, term_months)

    loans = loan_repository_fixture.get_loans_by_user_id(user_id)

    assert loans[0] == loan

def test_get_loans_by_user_id_with_no_loans(loan_repository_fixture):
    user_id = 1

    loans = loan_repository_fixture.get_loans_by_user_id(user_id)
    assert len(loans) == 0


