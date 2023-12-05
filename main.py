import os
import sys
import sqlite3

model_path = os.path.abspath("model")
sys.path.append(model_path)

repository_path = os.path.abspath("repository")
sys.path.append(repository_path)

service_path = os.path.abspath("service")
sys.path.append(service_path)

from model.currency import USD, BRL
from services.user_service import UserService
from services.transaction_service import TransactionService
from services.loan_service import LoanService
from repository.user_repository import UserRepository
from repository.transaction_repository import TransactionRepository
from repository.loan_repository import LoanRepository
from model.account import BudgetException

def display_menu():
    print("\n=== Account and Transaction Management System ===")
    print("1. Deposit Funds")
    print("2. Withdraw Funds")
    print("3. Transfer Funds")
    print("4. Process Loan")
    print("5. Create User")
    print("6. Display Balances")
    print("7. Exit")

def deposit_funds(user_service, user_id, amount):
    try:
        user_service.deposit_funds(user_id, amount)
        print("Deposit successful")
    except BudgetException as e:
        print(f"Deposit failed: {e}")

def withdraw_funds(user_service, user_id, amount):
    try:
        user_service.withdraw_funds(user_id, amount)
        print("Withdrawal successful")
    except BudgetException as e:
        print(f"Withdrawal failed: {e}")

def transfer_funds(transaction_service, sender_id, receiver_id, amount, currency):
    try:
        transaction_service.execute_and_save(sender_id, receiver_id, amount, currency)
        print("Transaction successful")
    except BudgetException as e:
        print(f"Transaction failed: {e}")

def process_loan(loan_service, user_id, amount, interest_rate, months):
    try:
        loan_service.process_loan(user_id, amount, interest_rate, months)
        print("Loan processed successfully")
    except BudgetException as e:
        print(f"Loan processing failed: {e}")

def create_user(user_service, currency):
    username = input("Enter username: ")
    password = input("Enter password: ")
    email = input("Enter email: ")
    birthdate = input("Enter birthdate (YYYY-MM-DD): ")

    user_service.create_user(username, password, email, birthdate, currency)
    print("User created successfully")

def display_balances(user_service):
    users = user_service.get_all_users()
    print("\nUser Balances:")
    for user in users:
        print(f"User ID: {user.id}, Username: {user.username}, Balance: {user.account.balance}")

def main():
    print("Account and transaction management system")

    conn = sqlite3.connect("test_database.db")
    user_repository = UserRepository(conn)
    transaction_repository = TransactionRepository(conn)
    loan_repository = LoanRepository(conn)

    user_service = UserService(user_repository)
    transaction_service = TransactionService(user_service, transaction_repository)
    loan_service = LoanService(user_service, loan_repository)

    currency = USD()
    currency2 = BRL()

    while True:
        display_menu()
        choice = input("Enter your choice (1-7): ")

        if choice == "1":
            user_id = int(input("Enter user ID: "))
            amount = float(input("Enter deposit amount: "))
            deposit_funds(user_service, user_id, amount)
        elif choice == "2":
            user_id = int(input("Enter user ID: "))
            amount = float(input("Enter withdrawal amount: "))
            withdraw_funds(user_service, user_id, amount)
        elif choice == "3":
            sender_id = int(input("Enter sender's user ID: "))
            receiver_id = int(input("Enter receiver's user ID: "))
            amount = float(input("Enter transfer amount: "))

            currency_val = int(input("Enter currency - 1 for USD, 2 for BRL: "))
            if(currency_val == 1):
                currency_val = currency
            else:
                currency_val = currency2
            transfer_funds(transaction_service, sender_id, receiver_id, amount, currency)
        elif choice == "4":
            user_id = int(input("Enter user ID: "))
            amount = float(input("Enter loan amount: "))
            interest_rate = float(input("Enter interest rate: "))
            months = int(input("Enter loan duration (in months): "))
            process_loan(loan_service, user_id, amount, interest_rate, months)
        elif choice == "5":
            create_user(user_service, currency)
        elif choice == "6":
            display_balances(user_service)
        elif choice == "7":
            print("Exiting the program. Goodbye!")
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 7.")

if __name__ == "__main__":
    main()