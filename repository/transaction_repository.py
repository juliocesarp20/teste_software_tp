import sqlite3
from model.transaction import Transaction

class TransactionRepository:
    def __init__(self, conn):
        self.conn = conn

    def save_transaction(self, transaction):
        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT INTO transactions (sender_id, receiver_id, amount, currency)
            VALUES (?, ?, ?, ?)
        ''', (transaction.sender_id, transaction.receiver_id, transaction.amount, transaction.currency))
        self.conn.commit()

    def get_transaction_by_id(self, transaction_id):
        cursor = self.conn.cursor()
        cursor.execute('SELECT id, sender_id, receiver_id, amount, currency FROM transactions')
        row = cursor.fetchone()

        if row:
            transaction_id, sender_id, receiver_id, amount, currency = row
            transaction = Transaction(
                id=transaction_id,
                sender_id=sender_id,
                receiver_id=receiver_id,
                amount=amount,
                currency=currency
            )
            return transaction
        else:
            return None

    def get_all_transactions(self):
        cursor = self.conn.cursor()
        cursor.execute('SELECT id, sender_id, receiver_id, amount, currency FROM transactions')
        rows = cursor.fetchall()

        transactions = []
        for row in rows:
            transaction_id, sender_id, receiver_id, amount, currency = row
            transaction = Transaction(
                id=transaction_id,
                sender_id=sender_id,
                receiver_id=receiver_id,
                amount=amount,
                currency=currency
            )
            transactions.append(transaction)

        return transactions
        
    def filter_transactions(self, filter_func):
        all_transactions = self.get_all_transactions()
        return list(filter(filter_func, all_transactions))

    def filter_by_sender_id(self, sender_id):
        def filter_func(transaction):
            return transaction.sender_id == sender_id
        return self.filter_transactions(filter_func)

    def filter_by_receiver_id(self, receiver_id):
        def filter_func(transaction):
            return transaction.receiver_id == receiver_id
        return self.filter_transactions(filter_func)

    def filter_by_amount(self, min_amount, max_amount):
        def filter_func(transaction):
            print(transaction.amount)
            return min_amount <= transaction.amount <= max_amount
        return self.filter_transactions(filter_func)

    def filter_by_currency(self, currency):
        def filter_func(transaction):
            return transaction.currency == currency
        return self.filter_transactions(filter_func)

    def close_connection(self):
        self.conn.close()
