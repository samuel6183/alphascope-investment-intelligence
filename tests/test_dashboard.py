import unittest
import pandas as pd
from dashboard import prepare, filter_assets

class DashboardTests(unittest.TestCase):
    def setUp(self):
        self.frame = pd.DataFrame([dict(symbol="demo",asset_type="stock",price=1,market_cap=1000000,daily_dollar_volume=100000,source="Synthetic",collected_at="2026-01-01")])
    def test_boundary(self):
        self.assertEqual(len(filter_assets(prepare(self.frame),"stock",1,100000,1000000)),1)
    def test_missing(self):
        with self.assertRaises(ValueError):
            prepare(self.frame.drop(columns="price"))
    def test_duplicate(self):
        with self.assertRaises(ValueError):
            prepare(pd.concat([self.frame,self.frame]))
    def test_invalid(self):
        with self.assertRaises(ValueError):
            prepare(self.frame.assign(price=float("inf")))
    def test_literal_search(self):
        self.assertTrue(filter_assets(prepare(self.frame),"All",5,0,0,"[").empty)
