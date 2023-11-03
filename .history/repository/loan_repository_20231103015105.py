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

        if interest_rate < 0 or interest_rate >= self.rate_limit:
            raise ValueError("Interest rate must be between 0 and {self.rate_limit}.")

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
