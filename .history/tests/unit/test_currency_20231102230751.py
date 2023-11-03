import unittest

class MockCurrency:
    def __init__(self, value, name):
        self.value = value
        self.name = name

class TestCurrencyConversion(unittest.TestCase):
    
    def test_brl_to_eur_conversion(self):
        brl = MockCurrency(0.2, "BRL")
        eur = MockCurrency(1.1, "EUR")
        amount = 100
        converted_amount = brl.convert_to(eur, amount)
        self.assertAlmostEqual(converted_amount, amount * (0.2 / 1.1), delta=0.001)

    def test_eur_to_usd_conversion(self):
        eur = MockCurrency(1.1, "EUR")
        usd = MockCurrency(1.0, "USD")
        amount = 100
        converted_amount = eur.convert_to(usd, amount)
        self.assertAlmostEqual(converted_amount, amount * (1.1 / 1.0), delta=0.001)

    def test_yen_to_cad_conversion(self):
        yen = MockCurrency(0.007, "YEN")
        cad = MockCurrency(0.7, "CAD")
        amount = 100
        converted_amount = yen.convert_to(cad, amount)
        self.assertAlmostEqual(converted_amount, amount * (0.007 / 0.7), delta=0.001)

    def test_usd_to_usd_conversion(self):
        usd1 = MockCurrency(1.0, "USD")
        usd2 = MockCurrency(1.0, "USD")
        amount = 100
        converted_amount = usd1.convert_to(usd2, amount)
        self.assertEqual(converted_amount, amount)

if __name__ == '__main__':
    unittest.main()
