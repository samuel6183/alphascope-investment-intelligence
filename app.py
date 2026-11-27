"""AlphaScope public research demo. No live market feed or trading."""
import io
import pandas as pd
import streamlit as st
from dashboard import prepare, filter_assets
from quant import prices_from_csv, risk_metrics, equal_weight_backtest, bootstrap_paths, valuation, fundamental_ratios
import numpy as np

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
tab1,tab2,tab3,tab4,tab5 = st.tabs(["Market screener","Scenario calculator","Methodology","Historical risk & backtest","Fundamentals & valuation"])
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

with tab4:
    st.subheader("Historical risk and fixed-universe backtest")
    st.caption("Upload authorized adjusted daily prices with date and one column per asset. Use a single asset-class calendar. No predictive claims.")
    history=st.file_uploader("Adjusted price history CSV",type=["csv"],key="history")
    periods=st.selectbox("Observations per year",[252,365])
    fee=st.number_input("Trading cost (basis points)",min_value=0,max_value=1000,value=10)
    try:
        if history and history.size>5_000_000:
            raise ValueError("Maximum file size 5 MB")
        if history:
            raw=pd.read_csv(history)
        else:
            rng=np.random.default_rng(42)
            raw=pd.DataFrame({"date":pd.bdate_range("2024-01-01",periods=252),"DEMO-A":100*np.cumprod(1+rng.normal(.0003,.015,252)),"DEMO-B":100*np.cumprod(1+rng.normal(.0002,.02,252))})
            st.info("Synthetic historical example, not actual returns. Use 252 periods.")
        p=prices_from_csv(raw)
        if p.shape[1]>50 or len(p)>10000:
            raise ValueError("Maximum 50 assets and 10,000 dates")
        st.dataframe(risk_metrics(p,periods))
        net=equal_weight_backtest(p,fee)
        st.line_chart(pd.concat([net,p/p.iloc[0]],axis=1))
        st.caption("Equal-weight daily rebalancing, initial and trading costs. Individual buy-and-hold comparison lines exclude costs. No survivor-bias correction.")
        st.dataframe(p.pct_change().dropna().corr())
        paths=bootstrap_paths(p,horizon=periods)
        st.write("Illustrative IID bootstrap terminal return quantiles (5%, median, 95%)",np.quantile(paths,[.05,.5,.95]))
        st.caption("Not calibrated probabilities; ignores serial dependence, regime changes and costs.")
    except Exception as exc:
        st.error(str(exc))
with tab5:
    st.subheader("User-supplied trailing fundamentals")
    st.caption("Fictional defaults. Use consistent currency units and reporting period. No automatic filing ingestion.")
    inputs={}
    for label,default in [("Revenue",100.),("Net income",10.),("Operating cash flow",20.),("Capital expenditure",5.),("Debt",30.),("Equity",50.),("Market capitalization",100.)]:
        inputs[label]=st.number_input(label,value=default,key="fund_"+label)
    try:
        st.json({k:(float(v) if np.isfinite(v) else None) for k,v in fundamental_ratios(*inputs.values()).items()})
    except ValueError as exc:
        st.error(str(exc))
    st.subheader("Earnings multiple scenario")
    e=st.number_input("Annual common earnings (millions)",min_value=0.,value=5.2)
    s=st.number_input("Common shares (millions)",min_value=.001,value=42.55)
    m=st.number_input("Assumed earnings multiple",min_value=0.,value=12.)
    d=st.slider("Additional dilution (%)",0,100,0)
    st.metric("Scenario value per share",f"{valuation(e,s,m,d/100):.2f}")
    st.caption("Assumed multiple and earnings, not an independently estimated intrinsic value.")
