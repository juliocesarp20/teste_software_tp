import pytest
from loan import Loan

@pytest.fixture
def user_fixture():
    return 1  # You can set the user ID as needed for your tests

# Test Loan creation
def test_create_loan(user_fixture):
    user_id = user_fixture
    amount = 1000
    interest_rate = 0.1
    term_months = 12
    loan = Loan(user_id, amount, interest_rate, term_months)

    assert loan.user_id == user_id
    assert loan.amount == amount
    assert loan.interest_rate == interest_rate
    assert loan.term_months == term_months
    assert loan.remaining_balance == amount
    assert loan.paid_amount == 0

# Test making a payment
def test_make_payment(user_fixture):
    user_id = user_fixture
    amount = 1000
    interest_rate = 0.1
    term_months = 12
    loan = Loan(user_id, amount, interest_rate, term_months)

    payment_amount = 200
    loan.make_payment(payment_amount)

    assert loan.paid_amount == payment_amount
    assert loan.remaining_balance == (amount - payment_amount)

# Test making a payment that exceeds the remaining balance
def test_make_payment_exceeds_balance(user_fixture):
    user_id = user_fixture
    amount = 1000
    interest_rate = 0.1
    term_months = 12
    loan = Loan(user_id, amount, interest_rate, term_months)

    payment_amount = 1200
    with pytest.raises(ValueError):
        loan.make_payment(payment_amount)

# Test making a payment for an already paid-off loan
def test_make_payment_already_paid_off(user_fixture):
    user_id = user_fixture
    amount = 1000
    interest_rate = 0.1
    term_months = 12
    loan = Loan(user_id, amount, interest_rate, term_months)

    payment_amount = 1200
    loan.make_payment(payment_amount)

    with pytest.raises(ValueError):
        loan.make_payment(payment_amount)

# Test making a payment with a negative amount
def test_make_payment_negative_amount(user_fixture):
    user_id = user_fixture
    amount = 1000
    interest_rate = 0.1
    term_months = 12
    loan = Loan(user_id, amount, interest_rate, term_months)

    payment_amount = -200
    with pytest.raises(ValueError):
        loan.make_payment(payment_amount)

# Test loan payoff status
def test_is_paid_off(user_fixture):
    user_id = user_fixture
    amount = 1000
    interest_rate = 0.1
    term_months = 12
    loan = Loan(user_id, amount, interest_rate, term_months)

    assert not loan.is_paid_off()

    payment_amount = 1200
    loan.make_payment(payment_amount)

    assert loan.is_paid_off()

# Test applying a discount
def test_apply_discount(user_fixture):
    user_id = user_fixture
    amount = 1000
    interest_rate = 0.1
    term_months = 12
    loan = Loan(user_id, amount, interest_rate, term_months)

    discount_rate = 0.2
    loan.apply_discount(discount_rate)

    assert loan.interest_rate == 0.08  # 10% - 20% = 8%
