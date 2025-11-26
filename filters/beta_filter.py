import pandas as pd


def filter_by_beta(df, fundamentals_df=None, max_beta=2.0):
    if fundamentals_df is None:
        return df
    merged = df.merge(fundamentals_df[['Ticker', 'beta']], on='Ticker', how='left')
    merged = merged[merged['beta'].notna()]
    merged = merged[merged['beta'] <= max_beta]
    return merged.drop(columns=['beta'], errors='ignore')