class Transaction:
    def __init__(self, sender_id, receiver_id, amount,currency,id=None):
        self.sender_id = sender_id
        self.receiver_id = receiver_id
        self.amount = amount
        self.currency = currency
        self.transaction_id = id
