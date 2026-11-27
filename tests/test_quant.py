import unittest
import numpy as np
import pandas as pd
from quant import prices_from_csv,risk_metrics,equal_weight_backtest,valuation,bootstrap_paths,fundamental_ratios

class QuantTests(unittest.TestCase):
    def setUp(self):
        self.p=prices_from_csv(pd.DataFrame({"date":pd.date_range("2024-01-01",periods=40),"A":100*1.01**np.arange(40),"B":100*1.01**np.arange(40)}))
    def test_return(self):
        self.assertAlmostEqual(risk_metrics(self.p).loc["A","annualized_return"],1.01**252-1)
    def test_drawdown(self):
        self.assertAlmostEqual(risk_metrics(self.p).loc["A","max_drawdown"],0)
    def test_backtest(self):
        self.assertAlmostEqual(equal_weight_backtest(self.p,0).iloc[-1],1.01**39)
    def test_cost(self):
        self.assertLess(equal_weight_backtest(self.p,10).iloc[-1],equal_weight_backtest(self.p,0).iloc[-1])
    def test_value(self):
        self.assertAlmostEqual(valuation(10,5,12,.2),20)
    def test_bootstrap(self):
        np.testing.assert_allclose(bootstrap_paths(self.p,10,20),1.01**10-1)
    def test_fundamentals(self):
        self.assertEqual(fundamental_ratios(100,10,20,5,30,50,100)["free_cash_flow"],15)
    def test_bad_prices(self):
        with self.assertRaises(ValueError):
            prices_from_csv(pd.DataFrame({"date":pd.date_range("2024-01-01",periods=40),"A":0}))
