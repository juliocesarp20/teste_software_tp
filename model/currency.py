class Currency():
    def __init__(self, value, name, symbol = "$"):
        self.value = value
        self.name = name
        self.symbol = symbol

    def convert_to(self, target_currency, amount):
        if not isinstance(target_currency, Currency):
            raise ValueError("Target currency must be an instance of Currency.")

        if amount <= 0:
            raise ValueError("Amount cannot be negative or zero when converting currencies.")
        
        if self.value >=1 and target_currency.value < 1:
            exchange_rate = self.value / target_currency.value
        elif self.value <= 1:
            exchange_rate = self.value / target_currency.value
        else:
            exchange_rate = self.value * target_currency.value

        converted_amount = amount * exchange_rate

        return converted_amount
    
    def to_dict(self):
        return {
            "value": self.value,
            "name": self.name,
            "symbol": self.symbol
        }

    @classmethod
    def from_dict(cls, data):
        return cls(data["value"], data["name"], data["symbol"])

    def __eq__(self, other):
        if isinstance(other, Currency):
            return self.name == other.name and self.value == other.value
        return False
    
    def __str__(self):
        return f"{self.name} = {self.value}"


class BRL(Currency):
    def __init__(self):
        super().__init__(0.2, "BRL","R$")


class EUR(Currency):
    def __init__(self):
        super().__init__(1.1, "EUR","€")


class USD(Currency):
    def __init__(self):
        super().__init__(1, "USD","$")


class YEN(Currency):
    def __init__(self):
        super().__init__(0.007, "YEN","¥")


class CAD(Currency):
    def __init__(self):
        super().__init__(0.7, "CAD","C$")
