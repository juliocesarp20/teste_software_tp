from abc import ABC, abstractmethod

class Currency(ABC):
    def __init__(self, value, name):
        self.value = value
        self.name = name

    @abstractmethod
    def convert_to(self, target_currency, amount):
        pass

    def __eq__(self, other):
        if isinstance(other, Currency):
            return self.name == other.name and self.value == other.value
        return False


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
