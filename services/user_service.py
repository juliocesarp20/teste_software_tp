import re
import datetime

class UserNotFoundException(Exception):
    pass

class MailInvalidException(Exception):
    pass

class AgeInvalidException(Exception):
    pass

class UserService:
    def __init__(self, user_repository):
        self.user_repository = user_repository

    def is_adult(self, birth_date):
        today = datetime.date.today()
        birth_date = datetime.datetime.strptime(birth_date, "%Y-%m-%d").date()
        age = today.year - birth_date.year - (
                (today.month, today.day) < (birth_date.month, birth_date.day))
        return age >= 18

    def is_valid_email(self, email):
        pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        return re.match(pattern, email)
    
    def get_all_users(self):
        return self.user_repository.get_all_users()

    def create_user(self, username, password, email, birth_date, currency=None):
        if not self.is_valid_email(email):
            raise MailInvalidException("Invalid email format")
        if not self.is_adult(birth_date):
            raise AgeInvalidException("Age requirement of 18 years old not met")

        user_id = self.user_repository.create_user(username, password, email, birth_date, currency)
        return user_id

    def edit_user(self, user_id, new_username=None, new_email=None, new_birth_date=None,
                  currency=None):
        if new_email != None and not self.is_valid_email(new_email):
            raise MailInvalidException("Invalid email format")
        if new_birth_date != None and not self.is_adult(new_birth_date):
            raise AgeInvalidException("Age requirement of 18 years old not met")

        return self.user_repository.edit_user(user_id, new_username, new_email, new_birth_date, currency)

    def delete_user(self, user_id):
        self.user_repository.delete_user(user_id)

    def deposit_funds(self, user_id, amount):
        self.user_repository.deposit_funds(user_id, amount)

    def withdraw_funds(self, user_id, amount):
        self.user_repository.withdraw_funds(user_id, amount)

    def get_user_by_id(self, user_id):
        user = self.user_repository.get_user_by_id(user_id)
        if user == False:
            raise UserNotFoundException("User with ID "+str(user_id)+" not found")
        return user
    def filter_users(self, filter_func):
        return self.user_repository.filter_users(filter_func)

    def filter_by_username(self, username_pattern):
        return self.user_repository.filter_by_username(username_pattern)

    def filter_by_email(self, email_pattern):
        return self.user_repository.filter_by_email(email_pattern)

    def filter_by_age(self, min_age, max_age):
        return self.user_repository.filter_by_age(min_age, max_age)

    def filter_by_currency(self, target_currency):
        return self.user_repository.filter_by_currency(target_currency)
