from model.account import BudgetException
from model.transaction import Transaction
from repository.user_repository import UserNotFoundException


class TransactionRepository:
    def __init__(self, user_repository):
        self.transactions = []
        self.user_repository = user_repository

    def add_transaction(self, transaction):
        """Add a transaction to the repository."""
        self.transactions.append(transaction)

    def get_transaction_by_id(self, transaction_id):
        for transaction in self.transactions:
            if transaction.id == transaction_id:
                return transaction
        return None

    def execute_and_save(self, sender_id, receiver_id, amount, currency):
        sender = self.user_repository.get_user_by_id(sender_id)
        receiver = self.user_repository.get_user_by_id(receiver_id)

        if sender is None or receiver is None:
            raise UserNotFoundException("Invalid sender or receiver ID")

        sender_account = sender.account
        receiver_account = receiver.account

        if sender_account.balance < amount:
            raise BudgetException("Insufficient funds for the transaction")

        amount_in_account_currency = amount / currency.value

        self.user_repository.withdraw_funds(sender_id, amount_in_account_currency)

        amount_in_receiver_currency = amount_in_account_currency * receiver.account.currency.value

        receiver_account.deposit(amount_in_receiver_currency)

        transaction = Transaction(sender_id, receiver_id, amount_in_receiver_currency,
                                  currency)
        self.add_transaction(transaction)

    def list_transactions(self):
        return self.transactions
