"""Transparent research calculations; no fitted prediction model."""
import numpy as np
import pandas as pd

def prices_from_csv(frame):
    """Require a common, daily-ish calendar and positive adjusted prices."""
    if "date" not in frame or len(frame.columns)<2:
        raise ValueError("Expected date and at least one adjusted-price column")
    dates = pd.to_datetime(frame["date"], errors="raise", utc=True).dt.normalize()
    if dates.isna().any() or dates.duplicated().any():
        raise ValueError("Dates must be valid and unique")
    p = frame.drop(columns="date").apply(pd.to_numeric, errors="raise")
    p.index = pd.DatetimeIndex(dates, name="date")
    p = p.sort_index()
    if len(p)<31 or not np.isfinite(p.to_numpy()).all() or (p<=0).any().any():
        raise ValueError("Need at least 31 complete positive price observations")
    if p.index.to_series().diff().dropna().dt.days.max()>7:
        raise ValueError("Gaps above seven days; supply aligned daily data")
    return p

def risk_metrics(prices, periods=252):
    """Annualized historical statistics, zero risk-free rate."""
    r = prices.pct_change().dropna()
    vol = r.std(ddof=1)*np.sqrt(periods)
    wealth = prices/prices.iloc[0]
    downside = np.sqrt((r.clip(upper=0)**2).mean())*np.sqrt(periods)
    return pd.DataFrame({"annualized_return":wealth.iloc[-1]**(periods/len(r))-1,
        "annualized_volatility":vol,
        "max_drawdown":(wealth/wealth.cummax()-1).min(),
        "sharpe_zero_rf":r.mean()*periods/vol.replace(0,np.nan),
        "sortino_zero_rf":r.mean()*periods/downside.replace(0,np.nan),
        "historical_var_95_daily_loss":(-r.quantile(.05)).clip(lower=0)})

def equal_weight_backtest(prices, cost_bps=10):
    """Fixed universe, daily rebalancing; costs on traded notional.
    First observation is a funded portfolio, with initial purchase cost.
    No hindsight optimization or claim of predictive performance.
    """
    if not 0<=cost_bps<10000:
        raise ValueError("Invalid transaction cost")
    r=prices.pct_change().dropna()
    w=np.ones(prices.shape[1])/prices.shape[1]
    cost=cost_bps/10000
    wealth=[1-cost]
    for row in r.to_numpy():
        gross=1+float(w@row)
        drift=w*(1+row)/gross
        turnover=np.abs(drift-w).sum()
        wealth.append(wealth[-1]*gross*(1-cost*turnover))
    return pd.Series(wealth,index=prices.index,name="equal_weight_net")

def valuation(earnings, shares, multiple, dilution=0):
    """Scenario common earnings multiple; monetary units must match."""
    if not all(np.isfinite([earnings,shares,multiple,dilution])) or earnings<0 or shares<=0 or multiple<0 or dilution<0:
        raise ValueError("Require nonnegative assumptions and positive shares")
    return earnings*multiple/(shares*(1+dilution))

def bootstrap_paths(prices, horizon=252, simulations=1000, seed=42):
    """IID joint daily return resampling; equal weights; no costs.
    Preserves same-day cross-asset dependence, not serial dependence.
    """
    if not 1<=horizon<=1000 or not 1<=simulations<=5000:
        raise ValueError("Simulation size outside limits")
    r=prices.pct_change().dropna().mean(axis=1).to_numpy()
    draws=np.random.default_rng(seed).choice(r,size=(simulations,horizon))
    return np.prod(1+draws,axis=1)-1

def fundamental_ratios(revenue, net_income, operating_cash, capex, debt, equity, market_cap):
    """All inputs same currency and comparable trailing period.
    Capex supplied as positive spending; undefined ratios stay missing.
    """
    vals=[revenue,net_income,operating_cash,capex,debt,equity,market_cap]
    if not all(np.isfinite(vals)) or revenue<=0 or capex<0 or debt<0 or market_cap<=0:
        raise ValueError("Invalid fundamental inputs")
    fcf=operating_cash-capex
    return {"net_margin":net_income/revenue,"free_cash_flow":fcf,
        "fcf_yield":fcf/market_cap,"debt_to_equity":debt/equity if equity>0 else np.nan,
        "return_on_equity":net_income/equity if equity>0 else np.nan}
