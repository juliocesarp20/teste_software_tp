class LoanRepository:
    def __init__(self, user_repository):
        self.loans = []
        self.user_repository = user_repository

    def create_loan(self, user_id, amount, interest_rate, term_months):
        if not self.user_repository.user_exists(user_id):
            raise ValueError("User does not exist. Cannot create a loan for a non-existent user.")
        loan = Loan(user_id, amount, interest_rate, term_months)
        self.loans.append(loan)
        return loan

    def get_loans_by_user_id(self, user_id):
        return [loan for loan in self.loans if loan.get_user_id() == user_id]

    def get_all_loans(self):
        return self.loans