# AlphaScope — Investment Intelligence

A reproducible Python research project for discovering low-priced equities and cryptocurrencies. Low unit price is not intrinsic value. This is not investment advice or an automated trading system.

## Getting started

Use Python 3.11 or newer. In a terminal:

```bash
git clone https://github.com/samuel6183/alphascope-investment-intelligence.git
cd alphascope-investment-intelligence
python -m pip install -r requirements.txt
python -m unittest discover -s tests -v
python scan.py
```

## Understanding the code

| File | Purpose |
|---|---|
| scan.py | Requests stock and crypto data, records errors and exports CSV |
| screening.py | Validates numeric fields and applies explicit filters |
| tests/test_screening.py | Tests normal, missing, invalid and boundary values |
| docs/methodology.md | Documents assumptions and research limitations |

The screen function returns a Boolean and a list of rejection reasons. A Boolean is True or False. A dictionary maps field names to values. The main loop visits each asset, calls the screen function and records its decision.

## Results

Open outputs/screen.csv in Excel. Filter eligible=True to view candidates. Inspect outputs/errors.json to identify missing coverage. Never treat a passing screen as a buy recommendation.

## Roadmap

1. Verify live provider coverage and quote freshness.
2. Expand the universe and include fundamental data.
3. Develop separate equity and crypto scoring models.
4. Validate with historical point-in-time data and transaction costs.
5. Build a dashboard.

The initial USD 5 price and USD 100,000 turnover thresholds are heuristic. Provider data may be delayed, incomplete or subject to rate limits. No predictive performance has yet been demonstrated.
