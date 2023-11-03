from model.loan import Loan

class LoanRepository:
    def __init__(self, user_repository):
        self.loans = []
        self.user_repository = user_repository
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
        self.loans.append(loan)
        return loan

    def get_loans_by_user_id(self, user_id):
        return [loan for loan in self.loans if loan.get_user_id() == user_id]

    def get_all_loans(self):
        return self.loans
    
    def get_rate_limit(self):
        return self.rate_limit
    
    def filter_loans(self, filter_func):
        return [loan for loan in self.loans if filter_func(loan)]

    def filter_by_balance(self, max_balance):
        def filter_func(loan):
            return loan.remaining_balance <= max_balance
        return self.filter_loans(filter_func)

    def filter_by_paid_amount(self, min_paid_amount):
        def filter_func(loan):
            return loan.paid_amount >= min_paid_amount
        return self.filter_loans(filter_func)

    def filter_by_loan_amount(self, max_loan_amount):
        def filter_func(loan):
            return loan.amount <= max_loan_amount
        return self.filter_loans(filter_func)

    def filter_by_term(self, min_term_months, max_term_months):
        def filter_func(loan):
            return min_term_months <= loan.term_months <= max_term_months
        return self.filter_loans(filter_func)

    def filter_by_interest_rate(self, max_interest_rate):
        def filter_func(loan):
            return loan.interest_rate <= max_interest_rate
        return self.filter_loans(filter_func)
