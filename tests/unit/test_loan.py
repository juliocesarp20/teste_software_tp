import pytest
from loan import Loan

@pytest.fixture
def user_fixture():
    return 1

def test_make_payment_paid_amount(user_fixture):
    user_id = user_fixture
    amount = 1000
    interest_rate = 0.1
    term_months = 12
    loan = Loan(user_id, amount, interest_rate, term_months)

    payment_amount = 200

    loan.make_monthly_payment(payment_amount)

    assert loan.paid_amount == pytest.approx(payment_amount, abs=1e-2)

def test_make_payment_remaining_balance(user_fixture):
    user_id = user_fixture
    amount = 1000
    interest_rate = 0.1
    term_months = 3
    loan = Loan(user_id, amount, interest_rate, term_months)

    payment_amount = 200

    loan.make_monthly_payment(payment_amount)

    assert loan.remaining_balance == pytest.approx(amount - payment_amount + (amount * interest_rate/12 *term_months), abs=1e-2)

def test_monthly_payment_is_paid_off(user_fixture):
    user_id = user_fixture
    amount = 1000
    interest_rate = 0.1
    term_months = 3
    loan = Loan(user_id, amount, interest_rate, term_months)

    payment_amount = 500
    loan.make_monthly_payment(payment_amount)
    payment_amount = 525
    loan.make_monthly_payment(payment_amount)

    assert loan.remaining_balance == 0

    assert loan.is_paid_off()

def test_monthly_payment_is_paid_off_one_month_term(user_fixture):
    user_id = user_fixture
    amount = 1000
    interest_rate = 0.12
    term_months = 1
    loan = Loan(user_id, amount, interest_rate, term_months)

    payment_amount = 1010
    loan.make_monthly_payment(payment_amount)

    assert pytest.approx(loan.remaining_balance, abs=1e-2) == 0

def test_monthly_payment_is_paid_off_twelve_month_term(user_fixture):
    user_id = user_fixture
    amount = 1000
    interest_rate = 0.1
    term_months = 12
    loan = Loan(user_id, amount, interest_rate, term_months)

    payment_amount = 100 
    for _ in range(11):
        loan.make_monthly_payment(payment_amount)

    assert loan.is_paid_off()

def test_monthly_payment_is_paid_off_over_twelve_month_term(user_fixture):
    user_id = user_fixture
    amount = 1000
    interest_rate = 1
    term_months = 24
    loan = Loan(user_id, amount, interest_rate, term_months)

    payment_amount = 125
    for _ in range(24):
        loan.make_monthly_payment(payment_amount)

    assert loan.is_paid_off()


def test_make_payment_exceeds_balance(user_fixture):
    user_id = user_fixture
    amount = 1000
    interest_rate = 0.1
    term_months = 12
    loan = Loan(user_id, amount, interest_rate, term_months)

    payment_amount = 1200
    with pytest.raises(ValueError):
        loan.make_monthly_payment(payment_amount)

def test_make_payment_already_paid_off(user_fixture):
    user_id = user_fixture
    amount = 1000
    interest_rate = 0.1
    term_months = 12
    loan = Loan(user_id, amount, interest_rate, term_months)

    loan.pay_off_remaining_months()

    with pytest.raises(ValueError):
        loan.pay_off_remaining_months()

def test_make_payment_negative_amount(user_fixture):
    user_id = user_fixture
    amount = 1000
    interest_rate = 0.1
    term_months = 12
    loan = Loan(user_id, amount, interest_rate, term_months)

    payment_amount = -200
    with pytest.raises(ValueError):
        loan.make_monthly_payment(payment_amount)

def test_is_paid_off(user_fixture):
    user_id = user_fixture
    amount = 1000
    interest_rate = 0.1
    term_months = 12
    loan = Loan(user_id, amount, interest_rate, term_months)

    loan.pay_off_remaining_months()

    assert loan.is_paid_off()

def test_apply_discount(user_fixture):
    user_id = user_fixture
    amount = 1000
    interest_rate = 0.1
    term_months = 12
    loan = Loan(user_id, amount, interest_rate, term_months)

    discount_rate = 0.2
    loan.apply_discount(discount_rate)
    

    assert pytest.approx(loan.interest_rate, abs=1e-2) == 0.08 
