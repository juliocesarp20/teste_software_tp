def make_monthly_payment(self, payment_amount):
    if self.remaining_balance == 0:
        raise ValueError("Loan is already paid off.")
    if self.remaining_balance + (self.amount * (self.interest_rate / 12)) - payment_amount < 0:
        raise ValueError("Payment exceeds monthly remaining balance")
    if self.is_paid_off():
        raise ValueError("Loan term is already completed.")
    if payment_amount <= 0:
        raise ValueError("Payment amount must be greater than zero.")

    monthly_interest = self.amount * (self.interest_rate / 12)
    monthly_principal = payment_amount - monthly_interest

    if self.current_month == self.term_months:
        if payment_amount < (self.remaining_balance + monthly_interest):
            raise ValueError("Final payment is less than the remaining balance and interest.")
        self.remaining_balance = 0
    else:
        self.remaining_balance -= monthly_principal

    self.paid_amount += payment_amount
    self.current_month += 1