from account import Account


class User:
    def __init__(self, id, username, password, email, birth_date, currency=None):
        self.id = id
        self.username = username
        self.password = password
        self.email = email
        self.birth_date = birth_date
        self.account = Account(currency=currency)
