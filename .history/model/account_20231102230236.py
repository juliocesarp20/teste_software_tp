class BudgetException(BaseException):
    pass

class Account:
    def __init__(self, initial_balance=0,user_id, currency=None):
        self.balance = initial_balance
        self.currency = currency
        self.user_id = user_id

    def deposit(self, amount, target_currency=None):
        if amount <= 0:
            raise BudgetException(
                "Invalid deposit amount. Amount must be greater than zero.")
        if self.currency and target_currency and self.currency != target_currency:
            raise ValueError("Currency conversion not supported.")
        self.balance += amount

    def withdraw(self, amount, target_currency=None):
        if amount <= 0:
            raise BudgetException(
                "Invalid withdrawal amount. Amount must be greater than zero.")
        if amount > self.balance:
            raise BudgetException(
                "Insufficient funds. Cannot withdraw more than the available balance.")
        if self.currency and target_currency and self.currency != target_currency:
            raise ValueError("Currency conversion not supported.")
        self.balance -= amount

    def get_balance(self):
        return self.balance

    def get_balance_in_currency(self, target_currency):
        if self.currency:
            if target_currency:
                return self.balance * (target_currency.value / self.currency.value)
            else:
                raise ValueError("No target currency specified for conversion.")
        else:
            raise BudgetException("No currency specified for the account.")
