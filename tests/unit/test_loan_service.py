import pytest
from unittest.mock import Mock
from model.loan import Loan
from services.loan_service import LoanService

@pytest.fixture
def user_repository_mock():
    user_repository = Mock()
    user_repository.get_user_by_id = Mock()
    return user_repository

@pytest.fixture
def loan_repository_mock():
    return Mock()

@pytest.fixture
def loan_service(user_repository_mock, loan_repository_mock):
    return LoanService(user_repository_mock, loan_repository_mock)

@pytest.fixture
def user_fixture():
    return 1

def test_create_loan(loan_service, user_repository_mock, user_fixture):
    amount = 1000
    interest_rate = 0.1
    term_months = 12

    user_repository_mock.get_user_by_id.return_value = user_fixture

    loan = loan_service.create_loan(user_fixture, amount, interest_rate, term_months)

    assert isinstance(loan, Loan)
    assert loan.get_user_id() == user_fixture

def test_create_loan_over_rate_limit(loan_service, user_repository_mock, user_fixture):
    amount = 1000
    interest_rate = 10000
    term_months = 12

    user_repository_mock.get_user_by_id.return_value = user_fixture

    with pytest.raises(ValueError, match="Interest rate must be between 0 and 100."):
        loan_service.create_loan(user_fixture, amount, interest_rate, term_months)

def test_create_loan_with_invalid_user(loan_service, user_repository_mock):
    amount = 1000
    interest_rate = 0.1
    term_months = 12

    user_repository_mock.get_user_by_id.return_value = None

    with pytest.raises(ValueError, match="User does not exist. Cannot create a loan for a non-existent user."):
        loan_service.create_loan(user_fixture, amount, interest_rate, term_months)

def test_create_loan_with_negative_amount(loan_service, user_repository_mock, user_fixture):
    amount = -100
    interest_rate = 0.1
    term_months = 12

    user_repository_mock.get_user_by_id.return_value = user_fixture

    with pytest.raises(ValueError, match="Loan amount must be greater than zero."):
        loan_service.create_loan(user_fixture, amount, interest_rate, term_months)

def test_create_loan_with_invalid_interest_rate(loan_service, user_repository_mock, user_fixture):
    amount = 1000
    interest_rate = -0.1
    term_months = 12

    user_repository_mock.get_user_by_id.return_value = user_fixture

    with pytest.raises(ValueError, match="Interest rate must be between 0 and 1."):
        loan_service.create_loan(user_fixture, amount, interest_rate, term_months)

def test_create_loan_with_zero_months(loan_service, user_repository_mock, user_fixture):
    amount = 1000
    interest_rate = 0.1
    term_months = 0 

    user_repository_mock.get_user_by_id.return_value = user_fixture

    with pytest.raises(ValueError, match="Loan term must be greater than zero."):
        loan_service.create_loan(user_fixture, amount, interest_rate, term_months)

def test_create_loan_with_zero_amount(loan_service, user_repository_mock, user_fixture):
    amount = 0
    interest_rate = 0.1
    term_months = 12

    user_repository_mock.get_user_by_id.return_value = user_fixture

    with pytest.raises(ValueError, match="Loan amount must be greater than zero."):
        loan_service.create_loan(user_fixture, amount, interest_rate, term_months)

def test_get_loans_by_user_id(loan_service, user_repository_mock, user_fixture, loan_repository_mock):
    amount = 1000
    interest_rate = 0.1
    term_months = 12

    user_repository_mock.get_user_by_id.return_value = user_fixture

    loan = loan_service.create_loan(user_fixture, amount, interest_rate, term_months)
    
    loan_repository_mock.get_loans_by_user_id.return_value = [loan]

    loans = loan_service.get_loans_by_user_id(user_fixture)

    assert loans[0] == loan

def test_get_loans_by_user_id_with_no_loans(loan_service, loan_repository_mock):
    user_id = 1

    loan_repository_mock.get_loans_by_user_id.return_value = []
    loans = loan_service.get_loans_by_user_id(user_id)
    assert len(loans) == 0
