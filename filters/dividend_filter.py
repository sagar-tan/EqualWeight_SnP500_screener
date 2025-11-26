import pandas as pd


def filter_by_dividend(df, fundamentals_df=None, min_yield=0.0):
    if fundamentals_df is None:
        return df
    merged = df.merge(fundamentals_df[['Ticker', 'dividendYield']], on='Ticker', how='left')
    merged['dividendYield'] = merged['dividendYield'].fillna(0)
    merged = merged[merged['dividendYield'] >= min_yield]
    return merged.drop(columns=['dividendYield'], errors='ignore')