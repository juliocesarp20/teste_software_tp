from currency import Currency
import pytest

class MockCurrency(Currency):
    def __init__(self, value, name):
        super().__init__(value, name)

def test_convert_from_weaker_to_stronger():
    brl = MockCurrency(0.2, "BRL")
    eur = MockCurrency(1.1, "EUR")
    amount = 100
    converted_amount = brl.convert_to(eur, amount)
    assert converted_amount == pytest.approx(amount * (0.2 / 1.1), abs=1e-3)

def test_convert_from_stronger_to_weaker():
    eur = MockCurrency(1.1, "EUR")
    usd = MockCurrency(1.0, "USD")
    amount = 100
    converted_amount = eur.convert_to(usd, amount)
    assert converted_amount == pytest.approx(amount * (1.1 / 1.0), abs=1e-3)

def test_convert_from_much_weaker_to_weaker():
    yen = MockCurrency(0.007, "YEN")
    cad = MockCurrency(0.7, "CAD")
    amount = 100
    converted_amount = yen.convert_to(cad, amount)
    assert converted_amount == pytest.approx(amount * (0.007 / 0.7), abs=1e-3)

def test_convert_from_equal_to_equal():
    usd1 = MockCurrency(1.0, "USD")
    usd2 = MockCurrency(1.0, "USD")
    amount = 100
    converted_amount = usd1.convert_to(usd2, amount)
    assert converted_amount == pytest.approx(amount, abs=1e-3)

def test_convert_from_much_weaker_to_stronger():
    yen = MockCurrency(0.007, "YEN")
    eur = MockCurrency(1.1, "EUR")
    amount = 100
    converted_amount = yen.convert_to(eur, amount)
    assert converted_amount == pytest.approx(amount * (0.007 / 1.1), abs=1e-3)

def test_convert_from_stronger_to_much_weaker():
    eur = MockCurrency(1.1, "EUR")
    yen = MockCurrency(0.007, "YEN")
    amount = 100
    converted_amount = eur.convert_to(yen, amount)
    assert converted_amount == pytest.approx(amount * (1.1 / 0.007), abs=1e-3)

def test_convert_to_invalid_target():
    brl = MockCurrency(0.2, "BRL")
    amount = 100
    with pytest.raises(ValueError) as exc_info:
        brl.convert_to("EUR", amount)
    assert str(exc_info.value) == "Target currency must be an instance of Currency."

def test_convert_to_negative_amount():
    eur = MockCurrency(1.1, "EUR")
    negative = MockCurrency(50,"ARG")
    with pytest.raises(ValueError) as exc_info:
        eur.convert_to(negative,-100)
    assert str(exc_info.value) == "Amount cannot be negative or zero when converting currencies."

def test_eq_equal():
    currency1 = MockCurrency(0.2, "BRL")
    currency2 = MockCurrency(0.2, "BRL")
    assert currency1 == currency2

def test_eq_not_equal():
    currency1 = MockCurrency(0.2, "BRL")
    currency2 = MockCurrency(1.1, "EUR")
    assert not (currency1 == currency2)

def test_eq_not_instance():
    currency = MockCurrency(0.2, "BRL")
    assert not (currency == "BRL")
