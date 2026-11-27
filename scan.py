"""Collect a small research universe and export all screening decisions."""
import csv
import json
from datetime import datetime, timezone
from pathlib import Path
import requests
import yfinance as yf
from screening import screen

STOCKS = ["BLND", "LSAK", "CCLD", "PLX", "EPM", "BATL", "BRN", "CURI"]

def collect_stocks():
    # Use ticker metadata; provider fields may be missing or delayed.
    rows, errors = [], []
    for symbol in STOCKS:
        try:
            info = yf.Ticker(symbol).info
            if info.get("currency") != "USD":
                raise ValueError("Missing or non-USD quote currency")
            price = info.get("regularMarketPrice") or info.get("currentPrice")
            volume = info.get("regularMarketVolume") or info.get("volume")
            rows.append(dict(symbol=symbol, asset_type="stock", price=price,
                daily_dollar_volume=price * volume if price and volume else None,
                market_cap=info.get("marketCap"), source="Yahoo Finance"))
        except Exception as exc:
            errors.append({"asset": symbol, "error": str(exc)})
    return rows, errors

def collect_crypto():
    # CoinGecko returns USD prices, market capitalization and 24-hour volume.
    response = requests.get("https://api.coingecko.com/api/v3/coins/markets",
        params={"vs_currency":"usd", "order":"market_cap_desc", "per_page":250, "page":1},
        timeout=30)
    response.raise_for_status()
    return [dict(symbol=c["symbol"].upper(), asset_id=c["id"], asset_type="crypto",
        price=c.get("current_price"), daily_dollar_volume=c.get("total_volume"),
        market_cap=c.get("market_cap"), source="CoinGecko") for c in response.json()]

def main():
    rows, errors = collect_stocks()
    try:
        rows.extend(collect_crypto())
    except Exception as exc:
        errors.append({"asset":"crypto universe", "error":str(exc)})
    collected_at = datetime.now(timezone.utc).isoformat()
    for row in rows:
        eligible, reasons = screen(row)
        row.update(eligible=eligible, reasons="; ".join(reasons), collected_at=collected_at)
    out = Path("outputs")
    out.mkdir(exist_ok=True)
    fields = ["symbol","asset_id","asset_type","price","daily_dollar_volume","market_cap","source","eligible","reasons","collected_at"]
    with (out / "screen.csv").open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)
    (out / "errors.json").write_text(json.dumps(errors, indent=2), encoding="utf-8")
    print(f"Collected {len(rows)} assets; {sum(r['eligible'] for r in rows)} passed; {len(errors)} collection errors.")
    if not rows:
        raise SystemExit("No data collected. Review outputs/errors.json.")

if __name__ == "__main__":
    main()
