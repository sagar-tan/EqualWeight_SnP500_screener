"""
 - loads S&P 500 symbols and prices
 - fetches fundamentals and history needed by filters
 - applies filters in the order defined in config.PIPELINE
 - computes equal weight allocations
 - writes final result to an Excel file defined in config.OUTPUT_FILE
"""

import logging
import sys
from typing import List

import pandas as pd

# core functions
from core.data_loader import get_sp500_symbols, fetch_latest_prices, fetch_fundamentals, fetch_history
from core.equal_weight import apply_equal_weight
from core.utils import summary_stats

# filters
from filters.price_filter import filter_by_price
from filters.volume_filter import filter_by_volume
from filters.marketcap_filter import filter_by_marketcap
from filters.pe_filter import filter_by_pe
from filters.dividend_filter import filter_by_dividend
from filters.beta_filter import filter_by_beta
from filters.volatility_filter import filter_by_volatility
from filters.momentum_filter import filter_by_momentum
from filters.sector_filter import filter_by_sector

import config

# sample screenshot path (local). kept here for reference or debug output.
SAMPLE_IMAGE_PATH = r"/mnt/data/1ac64b02-2d2d-42da-8b71-cff40b0586c3.png"

# setup basic logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger("run_pipeline")


def safe_fetch(symbols: List[str]):
    """
    Fetch prices, fundamentals, and history.
    Wrap downloads in try/except so one failure does not crash everything.
    """
    logger.info("Fetching latest prices for %d symbols", len(symbols))
    try:
        prices_df = fetch_latest_prices(symbols)
        logger.info("Prices fetched, rows: %d", len(prices_df))
    except Exception as e:
        logger.exception("Failed to fetch latest prices: %s", e)
        raise

    # fundamentals
    logger.info("Fetching fundamentals (this may take a while)...")
    try:
        fundamentals_df = fetch_fundamentals(prices_df["Ticker"].tolist())
        logger.info("Fundamentals fetched, rows: %d", len(fundamentals_df))
    except Exception as e:
        logger.warning("Failed to fetch fundamentals, continuing without them: %s", e)
        fundamentals_df = pd.DataFrame(columns=["Ticker"])

    # history for volatility and momentum
    logger.info("Fetching price history (1 year) ...")
    try:
        history_df = fetch_history(prices_df["Ticker"].tolist(), period="1y")
        logger.info("History fetched")
    except Exception as e:
        logger.warning("Failed to fetch history, continuing without it: %s", e)
        history_df = None

    return prices_df, fundamentals_df, history_df


def apply_pipeline(df: pd.DataFrame, fundamentals: pd.DataFrame, history: pd.DataFrame):
    """
    Apply filters in the order defined in config.PIPELINE.
    Each filter gets only the inputs it needs, and returns a filtered DataFrame.
    """
    working = df.copy()

    for step in config.PIPELINE:
        logger.info("Applying filter: %s", step)
        if step == "price":
            params = config.FILTERS.get("price", {})
            working = filter_by_price(working, **params)

        elif step == "volume":
            params = config.FILTERS.get("volume", {})
            working = filter_by_volume(working, fundamentals_df=fundamentals, **params)

        elif step == "marketcap":
            params = config.FILTERS.get("marketcap", {})
            working = filter_by_marketcap(working, fundamentals_df=fundamentals, **params)

        elif step == "pe":
            params = config.FILTERS.get("pe", {})
            working = filter_by_pe(working, fundamentals_df=fundamentals, **params)

        elif step == "dividend":
            params = config.FILTERS.get("dividend", {})
            working = filter_by_dividend(working, fundamentals_df=fundamentals, **params)

        elif step == "beta":
            params = config.FILTERS.get("beta", {})
            working = filter_by_beta(working, fundamentals_df=fundamentals, **params)

        elif step == "volatility":
            params = config.FILTERS.get("volatility", {})
            working = filter_by_volatility(working, price_history_df=history, **params)

        elif step == "momentum":
            params = config.FILTERS.get("momentum", {})
            working = filter_by_momentum(working, price_history_df=history, **params)

        elif step == "sector":
            params = config.FILTERS.get("sector", {})
            working = filter_by_sector(working, fundamentals_df=fundamentals, **params)

        else:
            logger.warning("Unknown pipeline step: %s, skipping", step)

        # defensive: drop any rows that lost price data during filtering
        if "Price" in working.columns:
            working = working.dropna(subset=["Price"])

        logger.info("Rows after %s: %d", step, len(working))

        # stop early if all filtered out
        if len(working) == 0:
            logger.warning("No symbols left after %s filter. Exiting pipeline.", step)
            break

    return working


def finalize_and_save(df: pd.DataFrame):
    """
    Compute equal weights and save final output.
    Also print a short summary.
    """
    logger.info("Applying equal weight allocation")
    final = apply_equal_weight(df, config.PORTFOLIO_SIZE, config.ALLOW_FRACTIONAL)

    # summary
    s = summary_stats(final, config.PORTFOLIO_SIZE)
    logger.info("Summary: n_stocks=%d invested=%.2f remaining_cash=%.2f",
                s["n_stocks"], s["invested"], s["remaining_cash"])

    # final clean up and save
    final = final.sort_values("Ticker").reset_index(drop=True)
    out = config.OUTPUT_FILE
    try:
        final.to_excel(out, index=False)
        logger.info("Saved final output to %s", out)
    except Exception as e:
        logger.exception("Failed to save output to %s: %s", out, e)
        raise

    return final


def main():
    logger.info("Starting EqualWeight Screener pipeline")
    symbols = get_sp500_symbols()
    logger.info("Loaded %d symbols", len(symbols))

    prices_df, fundamentals_df, history_df = safe_fetch(symbols)

    # initial DF for pipeline is prices_df
    df_after_filters = apply_pipeline(prices_df, fundamentals_df, history_df)

    if df_after_filters.empty:
        logger.error("No stocks left after filtering. Exiting.")
        return

    final = finalize_and_save(df_after_filters)

    logger.info("Pipeline finished successfully. Final rows: %d", len(final))
    # If you want to inspect example image for reference, path is:
    logger.debug("Sample output image path: %s", SAMPLE_IMAGE_PATH)


if __name__ == "__main__":
    main()
