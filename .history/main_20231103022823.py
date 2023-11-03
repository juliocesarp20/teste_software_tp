import os
import sys

# Append model and repository paths to sys.path
model_path = os.path.abspath("model")
sys.path.append(model_path)

repository_path = os.path.abspath("repository")
sys.path.append(repository_path)

# Import modules
from model.account import BudgetException
from repository.user_repository import UserRepository
from model.currency import BRL, USD, Currency
from repository.transaction_repository import TransactionRepository
from model.loan import Loan
from repository.loan_repository import LoanRepository

def main():
    print("Account and transaction management system")

    currency = USD()
    currency2 = BRL()

    user_repository = UserRepository()

    transaction_repository = TransactionRepository(user_repository)

    loan_repository = LoanRepository(user_repository)

    user_repository.create_user("joe", "2014", "joe2013@email.com", "2001-03-10",currency)
    user_repository.create_user("alice", "alice123", "alice@email.com", "1995-05-20",currency2)

    user_repository.deposit_funds(1, 100)
    user_repository.deposit_funds(2, 200)

    loan_repository.create_loan(1, 1000, 0.1, 12)

    user1 = user_repository.get_user_by_id(1)
    user2 = user_repository.get_user_by_id(2)
    print(f"User 1 balance: {user1.account.balance}")
    print(f"User 2 balance: {user2.account.balance}")

    try:
        transaction_repository.execute_and_save(1, 2, 50, currency)
        print("Transaction successful")
    except BudgetException as e:
        print(f"Transaction failed: {e}")

    filtered_transactions = transaction_repository.filter_by_amount(50)

    print("Filtered Transactions:")
    for transaction in filtered_transactions:
        print(f"Transaction ID: {transaction.id}, Amount: {transaction.amount}, Sender: {transaction.sender_id}, Receiver: {transaction.receiver_id}")

if __name__ == "__main__":
    main()
