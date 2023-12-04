import sqlite3
from model.loan import Loan

class LoanRepository:
    def __init__(self, conn):
        self.conn = conn

    def save_loan(self, loan):
        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT INTO loans (user_id, amount, interest_rate, term_months)
            VALUES (?, ?, ?, ?)
        ''', (loan.get_user_id(), loan.amount, loan.interest_rate, loan.term_months))
        self.conn.commit()

    def get_loans_by_user_id(self, user_id):
        cursor = self.conn.cursor()
        cursor.execute('SELECT id, user_id, amount, interest_rate, term_months FROM loans WHERE user_id = ?', (user_id,))
        rows = cursor.fetchall()

        loans = []
        for row in rows:
            loan_id, user_id, amount, interest_rate, term_months = row
            loan = Loan(
                id=loan_id,
                user_id=user_id,
                amount=amount,
                interest_rate=interest_rate,
                term_months=term_months
            )
            loans.append(loan)

        return loans

    def get_all_loans(self):
        cursor = self.conn.cursor()
        cursor.execute('SELECT id, user_id, amount, interest_rate, term_months FROM loans')
        rows = cursor.fetchall()

        loans = []
        for row in rows:
            loan_id, user_id, amount, interest_rate, term_months = row
            loan = Loan(
                id=loan_id,
                user_id=user_id,
                amount=amount,
                interest_rate=interest_rate,
                term_months=term_months
            )
            loans.append(loan)

        return loans
    
    def filter_loans_sql(self, condition, parameters=None):
        cursor = self.conn.cursor()
        query = f'SELECT * FROM loans WHERE {condition}'
        cursor.execute(query, parameters)
        rows = cursor.fetchall()

        loans = [Loan(*row) for row in rows]
        return loans

    def filter_by_balance(self, max_balance):
        condition = 'amount - paid_amount <= ?'
        parameters = (max_balance,)
        return self.filter_loans_sql(condition, parameters)

    def filter_by_paid_amount(self, min_paid_amount):
        condition = 'paid_amount >= ?'
        parameters = (min_paid_amount,)
        return self.filter_loans_sql(condition, parameters)

    def filter_by_loan_amount(self, max_loan_amount):
        condition = 'amount <= ?'
        parameters = (max_loan_amount,)
        return self.filter_loans_sql(condition, parameters)

    def filter_by_term(self, min_term_months, max_term_months):
        condition = 'term_months BETWEEN ? AND ?'
        parameters = (min_term_months, max_term_months)
        return self.filter_loans_sql(condition, parameters)

    def filter_by_interest_rate(self, max_interest_rate):
        condition = 'interest_rate <= ?'
        parameters = (max_interest_rate,)
        return self.filter_loans_sql(condition, parameters)

    def close_connection(self):
        self.conn.close()
