import os
import sys
import pytest
import sqlite3

model_path = os.path.abspath("model")
sys.path.append(model_path)

repository_path = os.path.abspath("repository")
sys.path.append(repository_path)

from services.user_service import UserService
from services.transaction_service import TransactionService
from services.loan_service import LoanService
from repository.user_repository import UserRepository
from repository.transaction_repository import TransactionRepository
from repository.loan_repository import LoanRepository
def create_database(path):
    conn = sqlite3.connect(path)

    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS accounts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            balance REAL,
            currency TEXT,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS loans (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            amount REAL,
            interest_rate REAL,
            term_months INTEGER,
            paid_amount REAL DEFAULT 0,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY,
            sender_id INTEGER,
            receiver_id INTEGER,
            amount REAL,
            currency TEXT,
            FOREIGN KEY(sender_id) REFERENCES accounts(id),
            FOREIGN KEY(receiver_id) REFERENCES accounts(id)
        )
''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            password TEXT,
            email TEXT,
            birth_date TEXT
        )
''')

    # Commit the changes and close the connection
    conn.commit()
    conn.close()

# Fixture to create the test database
@pytest.fixture
def test_database_path():
    test_db_path = 'test_database_integration.db'
    create_database(test_db_path)
    yield test_db_path
    # Fixture finalizer: Delete the test database after each test
    delete_test_database(test_db_path)

def delete_test_database(test_db_path):
    # Delete the test database file
    try:
        import os
        os.remove(test_db_path)
    except FileNotFoundError:
        pass  # File not found, no action needed


@pytest.fixture
def user_repository_instance(test_database_path):
    conn = sqlite3.connect(test_database_path)
    user_repository = UserRepository(conn)
    yield user_repository
    conn.close()

@pytest.fixture
def transaction_repository_instance(test_database_path):
    conn = sqlite3.connect(test_database_path)
    transaction_repository = TransactionRepository(conn)
    yield transaction_repository
    conn.close()

@pytest.fixture
def loan_repository_instance(test_database_path):
    conn = sqlite3.connect(test_database_path)
    loan_repository = LoanRepository(conn)
    yield loan_repository
    conn.close()

@pytest.fixture
def user_service_instance(user_repository_instance):
    return UserService(user_repository_instance)

@pytest.fixture
def transaction_service_instance(user_repository_instance, transaction_repository_instance):
    return TransactionService(user_repository_instance, transaction_repository_instance)

@pytest.fixture
def loan_service_instance(user_repository_instance, loan_repository_instance):
    return LoanService(user_repository_instance, loan_repository_instance)