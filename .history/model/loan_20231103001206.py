class Loan:
    def __init__(self, user_id, amount, interest_rate, term_months):
        self.user_id = user_id
        self.amount = amount
        self.interest_rate = interest_rate
        self.term_months = term_months
        self.remaining_balance = amount
        self.paid_amount = 0
        self.current_month = 1  # Start from month 1

    def make_monthly_payment(self, payment_amount):
        if self.remaining_balance == 0:
            raise ValueError("Loan is already paid off.")
        if self.is_paid_off():
            raise ValueError("Loan term is already completed.")
        if payment_amount <= 0:
            raise ValueError("Payment amount must be greater than zero.")

        monthly_interest = self.remaining_balance * (self.interest_rate / 12)
        monthly_principal = payment_amount - monthly_interest

        if self.current_month == self.term_months:
            # This is the final payment
            if payment_amount < (self.remaining_balance + monthly_interest):
                raise ValueError("Final payment is less than the remaining balance and interest.")
            # Pay off the remaining balance
            self.remaining_balance = 0
        else:
            self.remaining_balance -= monthly_principal

        self.paid_amount += payment_amount
        self.current_month += 1

    def is_paid_off(self):
        return self.remaining_balance == 0

    def get_user_id(self):
        return self.user_id

    def get_current_month(self):
        return self.current_month
