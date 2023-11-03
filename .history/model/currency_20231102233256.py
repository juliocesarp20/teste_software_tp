from abc import ABC, abstractmethod

class Currency(ABC):
    @abstractmethod
    def __init__(self, value, name):
        self.value = value
        self.name = name

    def convert_to(self, target_currency, amount):
        if not isinstance(target_currency, Currency):
            raise ValueError("Target currency must be an instance of Currency.")

        if amount < 0:
            raise ValueError("Amount cannot be negative when converting currencies.")

        if self.value <= 1:
            exchange_rate = self.value / target_currency.value
        else:
            exchange_rate = self.value * target_currency.value

        converted_amount = amount * exchange_rate

        return converted_amount

    def __eq__(self, other):
        if isinstance other, Currency:
            return self.name == other.name and self.value == other.value
        return False
