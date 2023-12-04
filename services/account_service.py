from model.account import Account,BudgetException

class AccountService:
    def __init__(self, account_repository):
        self.account_repository = account_repository

    def create_account(self, initial_balance=0, currency=None):
        account = Account(initial_balance, currency)
        self.account_repository.save_account(account)
        return account

    def get_account_by_id(self, account_id):
        return self.account_repository.get_account_by_id(account_id)

    def deposit(self, account_id, amount, target_currency=None):
        if (amount<=0):
            raise BudgetException("Invalid deposit amount. Amount must be greater than zero.")
        try:
            self.account_repository.deposit_funds(account_id, amount)
            return self.account_repository.get_account_by_id(account_id)
        except BudgetException as e:
            raise BudgetException(f"Account with ID {account_id} not found")

    def withdraw(self, account_id, amount, target_currency=None):
        if (amount<=0):
            raise BudgetException("Invalid withdrawal amount. Amount must be greater than zero.")
        try:
            account = self.account_repository.get_account_by_id(account_id)
            if (account.balance < amount):
                raise BudgetException("Insufficient funds. Cannot withdraw more than the available balance.")
            self.account_repository.withdraw_funds(account_id, amount)
            return self.account_repository.get_account_by_id(account_id)
        except Exception as e:
            raise Exception(f"Account with ID {account_id} not found")

    def get_balance(self, account_id):
        account = self.account_repository.get_account_by_id(account_id)
        if account:
            return account.get_balance()
        else:
            raise BudgetException(f"Account with ID {account_id} not found")

    def get_balance_in_currency(self, account_id, target_currency):
        account = self.account_repository.get_account_by_id(account_id)
        if account:
            return account.get_balance_in_currency(target_currency)
        else:
            raise BudgetException(f"Account with ID {account_id} not found")
