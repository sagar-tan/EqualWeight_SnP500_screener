import streamlit as st
import pandas as pd
import io

from core.data_loader import get_sp500_symbols, fetch_latest_prices, fetch_fundamentals, fetch_history
from core.equal_weight import apply_equal_weight
from core.utils import summary_stats

from filters.price_filter import filter_by_price
from filters.volume_filter import filter_by_volume
from filters.marketcap_filter import filter_by_marketcap
from filters.pe_filter import filter_by_pe
from filters.dividend_filter import filter_by_dividend
from filters.beta_filter import filter_by_beta
from filters.volatility_filter import filter_by_volatility
from filters.momentum_filter import filter_by_momentum
from filters.sector_filter import filter_by_sector

st.set_page_config(page_title="S&P 500 Equal-Weight Screener", layout="wide")

st.title("📊 S&P 500 Equal Weight Screener")
st.write("Use the controls on the left to customize filter settings and then run the screener.")

# Sidebar settings
st.sidebar.header("Filter Settings")

# Portfolio settings
portfolio_size = st.sidebar.number_input("Portfolio Size", value=100000)

# Price filter
use_price = st.sidebar.checkbox("Enable Price Filter", value=True)
min_price = st.sidebar.number_input("Min Price", value=5)
max_price = st.sidebar.number_input("Max Price", value=1000)

# Volume filter
use_volume = st.sidebar.checkbox("Enable Volume Filter", value=True)
min_volume = st.sidebar.number_input("Min Average Volume", value=100000)

# Market cap filter
use_mcap = st.sidebar.checkbox("Enable Market Cap Filter", value=True)
min_mcap = st.sidebar.number_input("Min Market Cap (in USD)", value=1_000_000_000)

# PE filter
use_pe = st.sidebar.checkbox("Enable PE Filter", value=True)
max_pe = st.sidebar.number_input("Max PE Ratio", value=50)

# Dividend filter
use_dividend = st.sidebar.checkbox("Enable Dividend Filter", value=False)
min_yield = st.sidebar.number_input("Min Dividend Yield", value=0.0)

# Beta filter
use_beta = st.sidebar.checkbox("Enable Beta Filter", value=True)
max_beta = st.sidebar.number_input("Max Beta", value=2.0)

# Volatility filter
use_volatility = st.sidebar.checkbox("Enable Volatility Filter", value=True)
window_days = st.sidebar.number_input("Volatility Window (days)", value=60)
max_vol = st.sidebar.number_input("Max Daily Volatility", value=0.05)

# Momentum filter
use_momentum = st.sidebar.checkbox("Enable Momentum Filter", value=False)
months = st.sidebar.number_input("Momentum Months", value=3)
min_return = st.sidebar.number_input("Min Momentum Return", value=0.0)

# Sector filter
use_sector = st.sidebar.checkbox("Enable Sector Filter", value=False)
include_sector = st.sidebar.text_input("Include sectors (comma-separated)", "")
exclude_sector = st.sidebar.text_input("Exclude sectors (comma-separated)", "")

# Run button
run_button = st.sidebar.button("Run Screener 🚀")

# When clicked
if run_button:
    st.write("### Running Screener...")
    st.write("Fetching data...")

    symbols = get_sp500_symbols()
    prices_df = fetch_latest_prices(symbols)
    fundamentals = fetch_fundamentals(prices_df["Ticker"].tolist())
    history = fetch_history(prices_df["Ticker"].tolist())

    df = prices_df.copy()

    # Apply filters
    if use_price:
        df = filter_by_price(df, min_price=min_price, max_price=max_price)

    if use_volume:
        df = filter_by_volume(df, fundamentals_df=fundamentals, min_avg_volume=min_volume)

    if use_mcap:
        df = filter_by_marketcap(df, fundamentals_df=fundamentals, min_mcap=min_mcap)

    if use_pe:
        df = filter_by_pe(df, fundamentals_df=fundamentals, max_pe=max_pe)

    if use_dividend:
        df = filter_by_dividend(df, fundamentals_df=fundamentals, min_yield=min_yield)

    if use_beta:
        df = filter_by_beta(df, fundamentals_df=fundamentals, max_beta=max_beta)

    if use_volatility:
        df = filter_by_volatility(df, price_history_df=history, window_days=window_days, max_vol=max_vol)

    if use_momentum:
        df = filter_by_momentum(df, price_history_df=history, months=months, min_return=min_return)

    if use_sector:
        include_list = [s.strip() for s in include_sector.split(",") if s.strip()]
        exclude_list = [s.strip() for s in exclude_sector.split(",") if s.strip()]
        df = filter_by_sector(df, fundamentals_df=fundamentals, include=include_list, exclude=exclude_list)

    # Apply equal weight
    final = apply_equal_weight(df, portfolio_size=portfolio_size)

    # Summary
    stats = summary_stats(final, portfolio_size)
    st.subheader("📈 Summary")
    st.write(stats)

    # Show table
    st.subheader("📋 Screener Results")
    st.dataframe(final, use_container_width=True)

    # Download Excel
    buffer = io.BytesIO()
    final.to_excel(buffer, index=False)
    st.download_button("Download Excel File", data=buffer, file_name="screener_output.xlsx")
