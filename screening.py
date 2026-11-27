"""Transparent preliminary screening, not a prediction of returns."""
import math

def screen(asset, max_price=5.0, min_volume=100_000):
    """Return eligibility and reasons. All monetary fields are USD."""
    reasons = []
    for key in ("price", "daily_dollar_volume", "market_cap"):
        value = asset.get(key)
        if not isinstance(value, (int, float)) or isinstance(value, bool) or not math.isfinite(value) or value <= 0:
            reasons.append(f"Invalid or missing {key}")
    if reasons:
        return False, reasons
    if asset["price"] > max_price:
        reasons.append("Above price threshold")
    if asset["daily_dollar_volume"] < min_volume:
        reasons.append("Insufficient liquidity")
    return not reasons, reasons

def liquidity_ratio(asset):
    """Daily turnover relative to market cap; not a measure of intrinsic value."""
    return asset["daily_dollar_volume"] / asset["market_cap"]
