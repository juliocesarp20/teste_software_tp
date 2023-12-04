class BudgetException(BaseException):
    pass

class Account:
    def __init__(self,user_id = None, initial_balance=0,currency=None):
        self.balance = initial_balance
        self.currency = currency
        self.user_id = user_id

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

    def __str__(self):
        return f"{self.balance} = {self.currency} "