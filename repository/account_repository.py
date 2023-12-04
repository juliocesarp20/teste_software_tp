import sqlite3
import json
from model.currency import Currency
from model.account import Account
from model.account import BudgetException

class AccountRepository:
    def __init__(self, database_path='test_database.db'):
        self.conn = sqlite3.connect(database_path)

    def save_account(self, user_id, account):
        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT INTO accounts (user_id, balance, currency)
            VALUES (?, ?, ?)
        ''', (user_id, account.balance, json.dumps(account.currency.to_dict())))
        self.conn.commit()

    def get_account_by_user_id(self, user_id):
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM accounts WHERE user_id = ?', (user_id,))
        row = cursor.fetchone()
        if row:
            _,user_id, balance, currency_json = row
            currency_data = json.loads(currency_json)
            currency = Currency.from_dict(currency_data)
            return Account(user_id, balance, currency)
        else:
            return None

    def deposit_funds(self, user_id, amount):
        account = self.get_account_by_user_id(user_id)
        if account:
            cursor = self.conn.cursor()
            cursor.execute('''
                UPDATE accounts
                SET balance = ?
                WHERE user_id = ?
            ''', (amount, user_id))
            self.conn.commit()
        else:
            raise BudgetException(f"Account not found for user_id {user_id}")

    def withdraw_funds(self, user_id, amount):
        account = self.get_account_by_user_id(user_id)
        if account:
            cursor = self.conn.cursor()
            cursor.execute('''
                UPDATE accounts
                SET balance = ?
                WHERE user_id = ?
            ''', (account.balance, user_id))
            self.conn.commit()
        else:
            raise BudgetException(f"Account not found for user_id {user_id}")

    def close_connection(self):
        self.conn.close()
