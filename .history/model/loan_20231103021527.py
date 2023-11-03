class Loan:
    def __init__(self, user_id, amount, interest_rate, term_months):
        self.user_id = user_id
        self.amount = amount
        self.interest_rate = interest_rate
        self.term_months = term_months
        self.remaining_balance = amount + (amount * (self.interest_rate / 12 * self.term_months))
        self.paid_amount = 0
        self.current_month = 1 

    def make_monthly_payment(self, payment_amount):
        if self.remaining_balance == 0:
            raise ValueError("Loan is already paid off.")
        if self.remaining_balance - payment_amount < 0:
            raise ValueError("Payment exceeds monthly remaining balance")
        if self.is_paid_off():
            raise ValueError("Loan term is already completed.")
        if payment_amount <= 0:
            raise ValueError("Payment amount must be greater than zero.")

        if self.current_month == self.term_months:
            if payment_amount < (self.remaining_balance):
                raise ValueError("Final payment is less than the remaining balance and interest.")
            self.remaining_balance = 0
        else:
            self.remaining_balance -= payment_amount

        self.paid_amount += payment_amount
        self.current_month += 1


    def pay_off_remaining_months(self):
        if self.remaining_balance == 0:
            raise ValueError("Loan is already paid off.")
        if self.is_paid_off():
            raise ValueError("Loan term is already completed.")

        
        total_remaining_balance = self.remaining_balance
        
        self.remaining_balance = 0
        self.paid_amount += total_remaining_balance
        self.current_month = self.term_months
    
    def apply_discount(self, discount_rate):
        if discount_rate < 0 or discount_rate > 1:
            raise ValueError("Discount rate must be between 0 and 1.")
        self.interest_rate *= (1 - discount_rate)

    def is_paid_off(self):
        return self.remaining_balance == 0

    def get_user_id(self):
        return self.user_id

    def get_current_month(self):
        return self.current_month
