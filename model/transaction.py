class Transaction:
    def __init__(self, transaction_id, sender_id, receiver_id, amount):
        self.id = transaction_id
        self.sender_id = sender_id
        self.receiver_id = receiver_id
        self.amount = amount
