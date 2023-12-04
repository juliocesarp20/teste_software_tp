from model.loan import Loan

class LoanService:
    def __init__(self, user_repository, loan_repository):
        self.user_repository = user_repository
        self.loan_repository = loan_repository
        self.rate_limit = 100

    def create_loan(self, user_id, amount, interest_rate, term_months):
        if self.user_repository.get_user_by_id(user_id) is None:
            raise ValueError("User does not exist. Cannot create a loan for a non-existent user.")

        if amount <= 0:
            raise ValueError("Loan amount must be greater than zero.")

        if interest_rate < 0 or interest_rate > self.rate_limit:
            raise ValueError(f"Interest rate must be between 0 and {self.rate_limit}.")

        if term_months <= 0:
            raise ValueError("Loan term must be greater than zero.")

        loan = Loan(user_id, amount, interest_rate, term_months)
        self.loan_repository.save_loan(loan)
        return loan
    
    def process_loan(self, user_id, amount, interest_rate, term_months):
        loan = self.create_loan(user_id, amount, interest_rate, term_months)

        self.user_repository.deposit_funds(user_id, loan.amount)
    
    def make_monthly_payment(self, loan_id, payment_amount):
        loan = self.loan_repository.get_loan_by_id(loan_id)
        if loan:
            loan.make_monthly_payment(payment_amount)
            self.loan_repository.save_loan(loan)
        else:
            raise ValueError(f"Loan with ID {loan_id} not found.")

    def pay_off_remaining_months(self, loan_id):
        loan = self.loan_repository.get_loan_by_id(loan_id)
        if loan:
            loan.pay_off_remaining_months()
            self.loan_repository.save_loan(loan)
        else:
            raise ValueError(f"Loan with ID {loan_id} not found.")

    def apply_discount(self, loan_id, discount_rate):
        loan = self.loan_repository.get_loan_by_id(loan_id)
        if loan:
            loan.apply_discount(discount_rate)
            self.loan_repository.save_loan(loan)
        else:
            raise ValueError(f"Loan with ID {loan_id} not found.")

    def is_paid_off(self, loan_id):
        loan = self.loan_repository.get_loan_by_id(loan_id)
        if loan:
            return loan.is_paid_off()
        else:
            raise ValueError(f"Loan with ID {loan_id} not found.")

    def get_current_month(self, loan_id):
        loan = self.loan_repository.get_loan_by_id(loan_id)
        if loan:
            return loan.get_current_month()
        else:
            raise ValueError(f"Loan with ID {loan_id} not found.")

    def get_loans_by_user_id(self, user_id):
        return self.loan_repository.get_loans_by_user_id(user_id)

    def get_all_loans(self):
        return self.loan_repository.get_all_loans()
    
    def get_rate_limit(self):
        return self.rate_limit
    
    def filter_loans(self, filter_func):
        return self.loan_repository.filter_loans(filter_func)

    def filter_by_balance(self, max_balance):
        return self.loan_repository.filter_by_balance(max_balance)

    def filter_by_paid_amount(self, min_paid_amount):
        return self.loan_repository.filter_by_paid_amount(min_paid_amount)

    def filter_by_loan_amount(self, max_loan_amount):
        return self.loan_repository.filter_by_loan_amount(max_loan_amount)

    def filter_by_term(self, min_term_months, max_term_months):
        return self.loan_repository.filter_by_term(min_term_months, max_term_months)

    def filter_by_interest_rate(self, max_interest_rate):
        return self.loan_repository.filter_by_interest_rate(max_interest_rate)
