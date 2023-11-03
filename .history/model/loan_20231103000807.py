class Loan:
    def __init__(self, user_id, amount, interest_rate, term_months):
        self.user_id = user_id
        self.amount = amount
        self.interest_rate = interest_rate
        self.term_months = term_months
        self.remaining_balance = amount
        self.paid_amount = 0

    def make_payment(self, payment_amount):
        if self.remaining_balance == 0:
            raise ValueError("Loan is already paid off.")
        if payment_amount <= 0:
            raise ValueError("Payment amount must be greater than zero.")
        if payment_amount > self.remaining_balance:
            raise ValueError("Payment amount exceeds the remaining balance.")

        interest_payment = self.remaining_balance * (self.interest_rate / 12)
        principal_payment = payment_amount - interest_payment

        self.remaining_balance -= principal_payment
        self.paid_amount += payment_amount

    def is_paid_off(self):
        return self.remaining_balance == 0

    def get_user_id(self):
        return self.user_id
