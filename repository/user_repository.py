import sqlite3
import datetime
import re
import json
from model.currency import Currency
from model.user import User
from model.account import Account
from repository.account_repository import AccountRepository

class UserRepository:
    def __init__(self, database_path='test_database.db'):
        self.conn = sqlite3.connect(database_path)
        self.account_repository = AccountRepository(database_path)

    def generate_id(self):
        cursor = self.conn.cursor()
        cursor.execute('SELECT MAX(id) FROM users')
        result = cursor.fetchone()
        return (result[0] or 0) + 1

    def create_user(self, username, password, email, birth_date, currency=None):
        cursor = self.conn.cursor()
        user_id = self.generate_id()
        cursor.execute('''
            INSERT INTO users (id, username, password, email, birth_date)
            VALUES (?, ?, ?, ?, ?)
        ''', (user_id, username, password, email, birth_date))
        self.conn.commit()
        self.account_repository.save_account(user_id, Account(currency=currency))
        return user_id

    def edit_user(self, user_id, new_username=None, new_email=None, new_birth_date=None,
                  currency=None):
        cursor = self.conn.cursor()
        update_fields = []

        if new_username:
            update_fields.append(('username', new_username))
        if new_email:
            update_fields.append(('email', new_email))
        if new_birth_date:
            update_fields.append(('birth_date', new_birth_date))

        if not update_fields:
            return False

        update_fields.append(('id', user_id))
        update_fields_str = ', '.join([f'{field} = ?' for field, _ in update_fields])

        cursor.execute(f'''
            UPDATE users
            SET {update_fields_str}
            WHERE id = ?
        ''', [value for _, value in update_fields] + [user_id])

        self.conn.commit()
        return True

    def delete_user(self, user_id):
        cursor = self.conn.cursor()
        cursor.execute('DELETE FROM users WHERE id = ?', (user_id,))
        self.account_repository.delete_account_by_user_id(user_id)
        self.conn.commit()

    def deposit_funds(self, user_id, amount):
        self.account_repository.deposit_funds(user_id, amount)

    def withdraw_funds(self, user_id, amount):
        self.account_repository.withdraw_funds(user_id, amount)

    def get_user_by_id(self, user_id):
        cursor = self.conn.cursor()
        cursor.execute('''
            SELECT users.id, users.username, users.password, users.email, 
                   users.birth_date, accounts.balance, accounts.currency
            FROM users
            LEFT JOIN accounts ON users.id = accounts.user_id
            WHERE users.id = ?
        ''', (user_id,))
        row = cursor.fetchone()

        if row:
            user_id, username, password, email, birth_date, balance, currency_json = row
            currency_data = json.loads(currency_json) if currency_json else None
            currency = Currency.from_dict(currency_data) if currency_data else None
            account = Account(user_id, balance, currency) if balance is not None else None
            return User(user_id, username, password, email, birth_date, account)
        else:
            return None

    def filter_users(self, filter_func):
        cursor = self.conn.cursor()
        cursor.execute('SELECT id, username, password, email, birth_date FROM users')
        rows = cursor.fetchall()

        users = []
        for row in rows:
            user_id, username, password, email, birth_date = row
            user = User(
                id=user_id,
                username=username,
                password=password,
                email=email,
                birth_date=birth_date
            )
            if filter_func(user):
                users.append(user)

        return users


    def filter_by_username(self, username_pattern):
        def filter_func(user):
            return re.match(username_pattern, user.username)
        return self.filter_users(filter_func)

    def filter_by_email(self, email_pattern):
        def filter_func(user):
            return re.match(email_pattern, user.email)
        return self.filter_users(filter_func)

    def filter_by_age(self, min_age, max_age):
        today = datetime.date.today()
        def filter_func(user):
            birth_date = datetime.datetime.strptime(user.birth_date, "%Y-%m-%d").date()
            age = today.year - birth_date.year - (
                (today.month, today.day) < (birth_date.month, birth_date.day))
            return min_age <= age <= max_age
        return self.filter_users(filter_func)

    def filter_by_currency(self, target_currency):
        def filter_func(user):
            return user.currency == target_currency
        return self.filter_users(filter_func)
