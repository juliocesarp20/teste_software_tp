import os
import sys

# Append model, repository, and service paths to sys.path
model_path = os.path.abspath("model")
sys.path.append(model_path)

repository_path = os.path.abspath("repository")
sys.path.append(repository_path)

service_path = os.path.abspath("service")
sys.path.append(service_path)

# Import modules
from model.account import BudgetException
from model.currency import BRL, USD
from services.user_service import UserService
from services.transaction_service import TransactionService
from services.loan_service import LoanService
from repository.user_repository import UserRepository
from repository.transaction_repository import TransactionRepository
from repository.loan_repository import LoanRepository

def main():
    print("Account and transaction management system")

    # Instantiate repositories
    user_repository = UserRepository()
    transaction_repository = TransactionRepository()
    loan_repository = LoanRepository()

    # Instantiate services with repositories
    user_service = UserService(user_repository)
    transaction_service = TransactionService(user_service, transaction_repository)
    loan_service = LoanService(user_service, loan_repository)

    currency = USD()
    currency2 = BRL()

    user_service.create_user("joe", "2014", "joe2013@email.com", "2001-03-10", currency)
    user_service.create_user("alice", "alice123", "alice@email.com", "1995-05-20", currency2)

    #Deposita para o usuario 1 e 2
    user_service.deposit_funds(1, 100)
    user_service.deposit_funds(2, 200)

    #faz um emprestimo de 1000 para o usuario 1
    loan_service.process_loan(1, 1000, 0.1, 12)

    user1 = user_service.get_user_by_id(1)
    user2 = user_service.get_user_by_id(2)
    print(f"User 1 balance: {user1.account.balance}")
    print(f"User 2 balance: {user2.account.balance}")

    try:
        transaction_service.execute_and_save(1, 2, 50, currency)
        print("Transaction successful")
    except BudgetException as e:
        print(f"Transaction failed: {e}")

    user1 = user_service.get_user_by_id(1)
    user2 = user_service.get_user_by_id(2)
    print(f"User 1 balance: {user1.account.balance}")
    print(f"User 2 balance: {user2.account.balance}")

    filtered_transactions = transaction_service.filter_by_amount(0, 300)

    print("Filtered Transactions:")
    for transaction in filtered_transactions:
        print(
            f"Transaction ID: {transaction.transaction_id}, Amount: {transaction.amount}, Sender: {transaction.sender_id}, Receiver: {transaction.receiver_id}"
        )

    loan_service = LoanService(user_service, loan_repository)

    loan_service.process_loan(1, 1000, 0.1, 12)

    try:
        transaction_service.execute_and_save(1, 2, 1000, currency)
        print("Transaction successful")
    except BudgetException as e:
        print(f"Transaction failed: {e}")

    user1 = user_service.get_user_by_id(1)
    user2 = user_service.get_user_by_id(2)
    print(f"User 1 balance: {user1.account.balance}")
    print(f"User 2 balance: {user2.account.balance}")


if __name__ == "__main__":
    main()
