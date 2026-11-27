"""Pure data validation and filtering functions used by the dashboard."""
import numpy as np
import pandas as pd

REQUIRED = ["symbol","asset_type","price","market_cap","daily_dollar_volume","source","collected_at"]

def prepare(frame):
    """Reject malformed rows instead of silently imputing investment data."""
    missing = set(REQUIRED) - set(frame.columns)
    if missing:
        raise ValueError("Missing columns: " + ", ".join(sorted(missing)))
    data = frame[REQUIRED + (["asset_id"] if "asset_id" in frame else [])].copy()
    if data.empty:
        raise ValueError("Empty dataset")
    for col in ["price","market_cap","daily_dollar_volume"]:
        data[col] = pd.to_numeric(data[col], errors="coerce")
        if not (np.isfinite(data[col]) & (data[col] > 0)).all():
            raise ValueError("Invalid numeric field: " + col)
    for col in ["symbol","source","asset_type"]:
        if data[col].isna().any() or data[col].astype(str).str.strip().eq("").any():
            raise ValueError("Missing field: " + col)
    data["symbol"] = data.symbol.astype(str).str.strip().str.upper()
    data["asset_type"] = data.asset_type.astype(str).str.strip().str.lower()
    if not data.asset_type.isin(["stock","crypto"]).all():
        raise ValueError("Unknown asset type")
    data["collected_at"] = pd.to_datetime(data.collected_at, utc=True, errors="coerce")
    if data.collected_at.isna().any():
        raise ValueError("Invalid collection timestamp")
    key = data.symbol.copy()
    if "asset_id" in data:
        mask = data.asset_type.eq("crypto") & data.asset_id.notna() & data.asset_id.astype(str).str.strip().ne("")
        key.loc[mask] = data.loc[mask,"asset_id"].astype(str).str.strip()
    if pd.DataFrame({"type":data.asset_type,"key":key}).duplicated().any():
        raise ValueError("Duplicate assets; upload a single snapshot")
    return data

def filter_assets(data, asset_type, price, volume, cap, search=""):
    """Apply transparent thresholds, not an investment score."""
    mask = (data.price <= price) & (data.daily_dollar_volume >= volume) & (data.market_cap >= cap)
    if asset_type != "All":
        mask &= data.asset_type.eq(asset_type)
    if search:
        mask &= data.symbol.str.contains(search, case=False, regex=False)
    return data.loc[mask].sort_values(["asset_type","price","symbol"])
