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
    assert pytest.approx(converted_amount, amount * (0.2 / 1.1), rel=1e-3)

def test_convert_from_stronger_to_weaker():
    eur = MockCurrency(1.1, "EUR")
    usd = MockCurrency(1.0, "USD")
    amount = 100
    converted_amount = eur.convert_to(usd, amount)
    assert pytest.approx(converted_amount, amount * (1.1 / 1.0), rel=1e-3)

def test_convert_from_much_weaker_to_weaker():
    yen = MockCurrency(0.007, "YEN")
    cad = MockCurrency(0.7, "CAD")
    amount = 100
    converted_amount = yen.convert_to(cad, amount)
    assert pytest.approx(converted_amount, amount * (0.007 / 0.7), rel=1e-3)

def test_convert_from_equal_to_equal():
    usd1 = MockCurrency(1.0, "USD")
    usd2 = MockCurrency(1.0, "USD")
    amount = 100
    converted_amount = usd1.convert_to(usd2, amount)
    assert pytest.approx(converted_amount, amount, rel=1e-3)

def test_convert_from_much_weaker_to_stronger():
    yen = MockCurrency(0.007, "YEN")
    eur = MockCurrency(1.1, "EUR")
    amount = 100
    converted_amount = yen.convert_to(eur, amount)
    assert pytest.approx(converted_amount, amount * (0.007 / 1.1), rel=1e-3)

def test_convert_from_stronger_to_much_weaker():
    eur = MockCurrency(1.1, "EUR")
    yen = MockCurrency(0.007, "YEN")
    amount = 100
    converted_amount = eur.convert_to(yen, amount)
    assert pytest.approx(converted_amount, amount * (1.1 / 0.007), rel=1e-3)
