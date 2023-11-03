import re
import datetime

from model.account import Account
from model.user import User


class UserNotFoundException(Exception):
    pass


class MailInvalidException(Exception):
    pass


class AgeInvalidException(Exception):
    pass


class UserRepository:
    def __init__(self):
        self.users = []
        self.current_id = 0

    def generate_id(self):
        self.current_id += 1
        return self.current_id

    def is_adult(self, birth_date):
        today = datetime.date.today()
        birth_date = datetime.datetime.strptime(birth_date, "%Y-%m-%d").date()
        age = today.year - birth_date.year - (
                (today.month, today.day) < (birth_date.month, birth_date.day))
        return age >= 18

    def is_valid_email(self, email):
        pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        return re.match(pattern, email)

    def create_user(self, username, password, email, birth_date, currency=None):
        if not self.is_valid_email(email):
            raise MailInvalidException("Invalid email format")
        if not self.is_adult(birth_date):
            raise AgeInvalidException("Age requirement of 18 years old not met")

        user = User(self.generate_id(), username, password, email, birth_date,
                    currency=currency)
        self.users.append(user)

        return user.id

    def edit_user(self, user_id, new_username=None, new_email=None, new_birth_date=None,
                  currency=None):
        user = self.get_user_by_id(user_id)
        if user is None:
            raise UserNotFoundException(f"User with ID {user_id} not found")

        if new_username:
            user.username = new_username
        if new_email:
            if not self.is_valid_email(new_email):
                raise MailInvalidException("Invalid email format")
            user.email = new_email
        if new_birth_date:
            if not self.is_adult(new_birth_date):
                raise AgeInvalidException("Age requirement of 18 years old not met")
            user.birth_date = new_birth_date
        if currency:
            user.currency = currency

    def delete_user(self, user_id):
        self.users = [user for user in self.users if user.id != user_id]

    def deposit_funds(self, user_id, amount):
        user = self.get_user_by_id(user_id)
        if user:
            user.account.deposit(amount)
        else:
            raise UserNotFoundException(f"User with ID {user_id} not found")

    def withdraw_funds(self, user_id, amount):
        user = self.get_user_by_id(user_id)
        if user:
            user.account.withdraw(amount)
        else:
            raise UserNotFoundException(f"User with ID {user_id} not found")

    def get_user_by_id(self, user_id):
        for user in self.users:
            if user.id == user_id:
                return user
        return None

    def get_users_by_currency(self, currency):
        users_with_currency = []
        for user in self.users:
            if user.account.currency == currency:
                users_with_currency.append(user)
        return users_with_currency
