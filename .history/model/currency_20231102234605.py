from abc import ABC, abstractmethod

class Currency(ABC):
    @abstractmethod
    def __init__(self, value, name):
        self.value = value
        self.name = name

    def convert_to(self, target_currency, amount):
        if not isinstance(target_currency, Currency):
            raise ValueError("Target currency must be an instance of Currency.")
        
        if amount <= 0:
            raise ValueError("Amount cannot be negative or zero when converting currencies.")
        
        if self.value <= 1:
            if target_currency.value <= 1:
                exchange_rate = self.value / target_currency.value
            else:
                raise ValueError("Cannot convert from weaker currency to stronger currency.")
        else:
            if target_currency.value <= 1:
                raise ValueError("Cannot convert from stronger currency to weaker currency.")
            exchange_rate = self.value * target_currency.value
        
        converted_amount = amount * exchange_rate
        
        return converted_amount



    def __eq__(self, other):
        if isinstance(other, Currency):
            return self.name == other.name and self.value == other.value
        return False


class BRL(Currency):
    def __init__(self):
        super().__init__(0.2, "BRL")


class EUR(Currency):
    def __init__(self):
        super().__init__(1.1, "EUR")


class USD(Currency):
    def __init__(self):
        super().__init__(1, "USD")


class YEN(Currency):
    def __init__(self):
        super().__init__(0.007, "YEN")


class CAD(Currency):
    def __init__(self):
        super().__init__(0.7, "CAD")