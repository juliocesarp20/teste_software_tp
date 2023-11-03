import unittest
from ...model.currency import BRL, EUR, USD, YEN, CAD


class TestCurrencyConversion(unittest.TestCase):
    def test_brl_to_eur_conversion(self):
        brl = BRL()
        eur = EUR()
        amount = 100
        converted_amount = brl.convert_to(eur, amount)
        self.assertAlmostEqual(converted_amount, amount / 5.5, delta=0.001)

    def test_eur_to_usd_conversion(self):
        eur = EUR()
        usd = USD()
        amount = 100
        converted_amount = eur.convert_to(usd, amount)
        self.assertAlmostEqual(converted_amount, amount * 1.1, delta=0.001)

    def test_yen_to_cad_conversion(self):
        yen = YEN()
        cad = CAD()
        amount = 100
        converted_amount = yen.convert_to(cad, amount)
        self.assertAlmostEqual(converted_amount, amount / 100, delta=0.001)

    def test_usd_to_usd_conversion(self):
        usd1 = USD()
        usd2 = USD()
        amount = 100
        converted_amount = usd1.convert_to(usd2, amount)
        self.assertEqual(converted_amount, amount)


if __name__ == '__main__':
    unittest.main()
