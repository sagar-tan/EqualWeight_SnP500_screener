import pandas as pd


def filter_by_marketcap(df, fundamentals_df=None, min_mcap=1e9):
    if fundamentals_df is None:
        return df
    merged = df.merge(fundamentals_df[['Ticker', 'marketCap']], on='Ticker', how='left')
    merged = merged[merged['marketCap'] >= min_mcap]
    return merged.drop(columns=['marketCap'], errors='ignore')