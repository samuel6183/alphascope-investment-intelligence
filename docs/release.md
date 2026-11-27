# AlphaScope research edition — release scope

A self-contained research toolkit, not a production trading platform. The public demo uses synthetic examples; users supply authorized snapshots and adjusted price history. The earlier eight-stock / 250-crypto live collection is a limited personal research workflow, not an authorized public data feed.

## Quantitative methods
- Historical return: final/initial wealth raised to periods per year / number of returns, minus one.
- Volatility: sample daily standard deviation times square root of periods per year.
- Sharpe and Sortino: zero risk-free rate; undefined ratios are missing.
- Drawdown: wealth divided by running peak minus one; historical daily VaR is the nonnegative loss corresponding to the empirical fifth percentile.
- Backtest: fixed, user-selected universe, daily equal weights, initial purchase cost and rebalancing cost on absolute traded notional. No point-in-time universe, delisting adjustment or strategy selection. This is a descriptive illustration subject to survivorship bias, not evidence of alpha.
- Bootstrap: IID joint daily return sampling with fixed seed; ignores serial dependence, fees and structural change. Model quantiles are not calibrated real-world probabilities.
- Valuation: annual common earnings / diluted shares times assumed P/E. Not an intrinsic valuation estimate.
- Fundamentals: user-supplied trailing data; FCF = operating cash flow minus positive capex; nonpositive equity makes leverage and ROE undefined.

Use adjusted prices on an aligned calendar, 252 periods for equities and 365 for daily crypto; do not mix calendars. The toolkit checks large gaps, not exchange-specific holidays or corporate actions. No automated trade execution, ML model, predictive ranking or optimal portfolio is claimed.

## Outstanding external dependencies
Owner deployment through Streamlit, license choice, market data rights, applicable regulatory review. Automated fundamental ingestion and broad point-in-time historical datasets are future extensions, not release requirements. No verified investment recommendation.
