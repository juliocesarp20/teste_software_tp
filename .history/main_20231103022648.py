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
from model.currency import Currency
from repository.transaction_repository import TransactionRepository
from model.loan import Loan
from repository.loan_repository import LoanRepository

def main():
    print("Account and transaction management system")

    currency = Currency("abc", 3)

    # Create a user repository
    user_repository = UserRepository()

    # Create a transaction repository
    transaction_repository = TransactionRepository(user_repository)

    # Create a loan repository
    loan_repository = LoanRepository(user_repository)

    # Create two users
    user_repository.create_user("joe", "2014", "joe2013@email.com", "2001-03-10")
    user_repository.create_user("alice", "alice123", "alice@email.com", "1995-05-20")

    # Deposit funds for users
    user_repository.deposit_funds(1, 100)
    user_repository.deposit_funds(2, 200)

    # Create a loan for User 1
    loan_repository.create_loan(1, 1000, 0.1, 12)

    # Print user balances
    user1 = user_repository.get_user_by_id(1)
    user2 = user_repository.get_user_by_id(2)
    print(f"User 1 balance: {user1.account.balance}")
    print(f"User 2 balance: {user2.account.balance}")

    # Perform a transaction from User 1 to User 2
    try:
        transaction_repository.execute_and_save(1, 2, 50, currency)
        print("Transaction successful")
    except BudgetException as e:
        print(f"Transaction failed: {e}")

    # Filter transactions by balance
    filtered_transactions = transaction_repository.filter_transactions_by_balance(50)

    # Display the filtered transactions
    print("Filtered Transactions:")
    for transaction in filtered_transactions:
        print(f"Transaction ID: {transaction.id}, Amount: {transaction.amount}, Sender: {transaction.sender_id}, Receiver: {transaction.receiver_id}")

if __name__ == "__main__":
    main()
