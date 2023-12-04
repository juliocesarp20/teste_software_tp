from model.account import BudgetException
from model.transaction import Transaction
from services.user_service import UserNotFoundException
class TransactionService:
    def __init__(self, user_repository, transaction_repository):
        self.user_repository = user_repository
        self.transaction_repository = transaction_repository

    def execute_and_save(self, sender_id, receiver_id, amount, currency):
        sender = self.user_repository.get_user_by_id(sender_id)
        receiver = self.user_repository.get_user_by_id(receiver_id)

        if sender is None or receiver is None:
            raise UserNotFoundException("Invalid sender or receiver ID")

        sender_account = sender.account
        receiver_account = receiver.account

        if sender_account.balance < amount:
            raise BudgetException("Insufficient funds for the transaction")

        self.user_repository.withdraw_funds(sender_id, amount)

        amount_in_receiver_currency = sender_account.currency.convert_to(receiver_account.currency, amount)

        self.user_repository.deposit_funds(receiver_id,amount_in_receiver_currency)

        transaction = Transaction(sender_id, receiver_id, amount_in_receiver_currency, currency.name)
        self.transaction_repository.save_transaction(transaction)

    def list_transactions(self):
        return self.transaction_repository.get_all_transactions()

    def filter_by_sender_id(self, sender_id):
        return self.transaction_repository.filter_by_sender_id(sender_id)

    def filter_by_receiver_id(self, receiver_id):
        return self.transaction_repository.filter_by_receiver_id(receiver_id)

    def filter_by_amount(self, min_amount, max_amount):
        return self.transaction_repository.filter_by_amount(min_amount, max_amount)

    def filter_by_currency(self, currency):
        return self.transaction_repository.filter_by_currency(currency)
