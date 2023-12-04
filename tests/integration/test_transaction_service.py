import pytest
from model.currency import Currency
from model.transaction import Transaction
from services.transaction_service import UserNotFoundException, BudgetException

@pytest.mark.usefixtures("test_database_path", "user_repository_instance", "transaction_repository_instance")
class TestTransactionService:

    def test_execute_and_save_successful_transaction(self, user_service_instance, transaction_service_instance):
        sender_id = user_service_instance.create_user("Sender", "password", "sender@example.com", "1990-01-01",
                                                      currency=Currency(1.0, "USD"))
        receiver_id = user_service_instance.create_user("Receiver", "password", "receiver@example.com", "1990-01-01",
                                                         currency=Currency(1.0, "USD"))
        user_service_instance.deposit_funds(sender_id, 100.0)

        transaction_service_instance.execute_and_save(sender_id, receiver_id, 50.0, Currency(1.0, "USD"))

        sender_balance = user_service_instance.get_user_by_id(sender_id).account.balance
        receiver_balance = user_service_instance.get_user_by_id(receiver_id).account.balance
        transactions = transaction_service_instance.list_transactions()

        assert sender_balance == 50.0
        assert receiver_balance == 50.0

    def test_execute_and_save_insufficient_funds(self, user_service_instance, transaction_service_instance):
        sender_id = user_service_instance.create_user("Sender", "password", "sender@example.com", "1990-01-01",
                                                      currency=Currency(1.0, "USD"))
        receiver_id = user_service_instance.create_user("Receiver", "password", "receiver@example.com", "1990-01-01",
                                                         currency=Currency(1.0, "USD"))
        user_service_instance.deposit_funds(sender_id, 30.0)

        with pytest.raises(BudgetException, match="Insufficient funds for the transaction"):
            transaction_service_instance.execute_and_save(sender_id, receiver_id, 50.0, Currency(1.0, "USD"))
    
    def test_execute_and_save_successful_transaction_with_loan(self, user_service_instance, transaction_service_instance, loan_service_instance):
        sender_id = user_service_instance.create_user("Sender", "password", "sender@example.com", "1990-01-01",
                                                      currency=Currency(1.0, "USD"))
        receiver_id = user_service_instance.create_user("Receiver", "password", "receiver@example.com", "1990-01-01",
                                                         currency=Currency(1.0, "USD"))

        loan_service_instance.process_loan(sender_id, 100.0, 0.1, 12)

        transaction_service_instance.execute_and_save(sender_id, receiver_id, 50.0, Currency(1.0, "USD"))

        sender_balance = user_service_instance.get_user_by_id(sender_id).account.balance
        receiver_balance = user_service_instance.get_user_by_id(receiver_id).account.balance
        transactions = transaction_service_instance.list_transactions()

        assert sender_balance == 50.0
        assert receiver_balance == 50.0
        assert len(transactions) == 1

    def test_execute_and_save_successful_transaction_with_loan_and_different_currencies(self, user_service_instance, transaction_service_instance, loan_service_instance):
        sender_id = user_service_instance.create_user("Sender", "password", "sender@example.com", "1990-01-01",
                                                      currency=Currency(1.0, "USD"))
        receiver_id = user_service_instance.create_user("Receiver", "password", "receiver@example.com", "1990-01-01",
                                                         currency=Currency(1.1, "EUR"))

        loan_service_instance.process_loan(sender_id, 100.0, 0.1, 12)

        transaction_service_instance.execute_and_save(sender_id, receiver_id, 50.0, Currency(1.0, "USD"))

        sender_balance_usd = user_service_instance.get_user_by_id(sender_id).account.balance
        receiver_balance = user_service_instance.get_user_by_id(receiver_id).account.balance
        transactions = transaction_service_instance.list_transactions()

        assert sender_balance_usd == 50.0
        assert receiver_balance == pytest.approx(45.45, rel=1e-1)
        assert len(transactions) == 1

    def test_execute_and_save_invalid_users(self, transaction_service_instance):
        with pytest.raises(UserNotFoundException, match="Invalid sender or receiver ID"):
            transaction_service_instance.execute_and_save(100, 200, 50.0, Currency(1.0, "USD"))
