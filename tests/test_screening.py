import unittest
from screening import screen

class ScreeningTests(unittest.TestCase):
    def setUp(self):
        self.asset = dict(price=0.5, daily_dollar_volume=200000, market_cap=1000000)

    def test_pass(self):
        self.assertEqual(screen(self.asset), (True, []))

    def test_expensive(self):
        self.assertFalse(screen(dict(self.asset, price=6))[0])

    def test_illiquid(self):
        self.assertFalse(screen(dict(self.asset, daily_dollar_volume=10))[0])

    def test_missing(self):
        self.assertFalse(screen(dict(self.asset, market_cap=None))[0])

    def test_nan(self):
        self.assertFalse(screen(dict(self.asset, price=float("nan")))[0])

    def test_boundary(self):
        self.assertTrue(screen(dict(self.asset, price=5, daily_dollar_volume=100000))[0])

if __name__ == "__main__":
    unittest.main()
