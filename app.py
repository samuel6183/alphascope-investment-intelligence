"""AlphaScope public research demo. No live market feed or trading."""
import io
import pandas as pd
import streamlit as st
from dashboard import prepare, filter_assets

st.set_page_config(page_title="AlphaScope", page_icon="📊", layout="wide")
st.title("AlphaScope | Investment Intelligence")
st.caption("Research tools • transparent screening • no trading or return guarantees")
st.warning("Demo data are fictional. Uploaded data are supplied by you and are not independently verified. A passing filter does not mean an asset is undervalued.")
demo = """symbol,asset_type,price,market_cap,daily_dollar_volume,source,collected_at
DEMO-A,stock,0.8,20000000,500000,Synthetic,2026-01-01T00:00:00Z
DEMO-B,stock,3.2,90000000,1200000,Synthetic,2026-01-01T00:00:00Z
DEMO-C,crypto,0.004,8000000,350000,Synthetic,2026-01-01T00:00:00Z
DEMO-D,stock,0.3,5000000,1000,Synthetic,2026-01-01T00:00:00Z
"""
upload = st.file_uploader("Upload your own authorized market CSV (optional)", type=["csv"])
try:
    if upload and upload.size > 5_000_000:
        raise ValueError("Maximum CSV size is 5 MB.")
    data = prepare(pd.read_csv(upload if upload else io.StringIO(demo)))
except Exception as exc:
    st.error(f"Cannot read dataset: {exc}")
    st.stop()
st.info("User-supplied dataset" if upload else "Synthetic demonstration — not actual market quotes")
st.caption("Collection timestamps (UTC): " + str(data.collected_at.min()) + " to " + str(data.collected_at.max()))
with st.sidebar:
    st.header("Screening rules")
    asset_type = st.selectbox("Asset class", ["All", "stock", "crypto"])
    price = st.number_input("Maximum price (USD)", min_value=0.000001, value=5.0, format="%.6f")
    volume = st.number_input("Minimum daily turnover (USD)", min_value=0, value=100000, step=10000)
    cap = st.number_input("Minimum market capitalization (USD)", min_value=0, value=1000000, step=100000)
    search = st.text_input("Search ticker")
result = filter_assets(data, asset_type, price, volume, cap, search)
a,b,c = st.columns(3)
a.metric("Valid observations", len(data))
b.metric("Matching observations", len(result))
c.metric("Asset classes", data.asset_type.nunique())
tab1,tab2,tab3 = st.tabs(["Market screener","Scenario calculator","Methodology"])
with tab1:
    st.dataframe(result, hide_index=True, use_container_width=True)
    if not result.empty:
        st.bar_chart(result.assign(label=result.asset_type + ":" + result.symbol).groupby("label").daily_dollar_volume.sum())
    st.caption("Turnover measures differ between equity sessions and crypto 24-hour periods. Do not interpret them as identical.")
with tab2:
    amount = st.number_input("Hypothetical investment (KES)", min_value=0.0, value=5000.0)
    change = st.slider("Hypothetical return (%)", -100, 500, 0)
    st.metric("Scenario ending value (KES)", f"{amount*(1+change/100):,.2f}")
    st.caption("No forecast. Excludes fees, taxes and currency changes.")
with tab3:
    st.markdown("### Methodology\nThe screener uses price, trading turnover and market capitalization. It does not estimate intrinsic value, classify stablecoins, or predict future returns.\n\nData must contain symbol, asset_type, price, market_cap, daily_dollar_volume, source and collected_at. All prices and monetary fields are USD. Each timestamp must represent the collection time, not necessarily the quote time.\n\nPublic demo intentionally avoids automatic redistribution of third-party market quotes. Upload only data you are authorized to process.")
