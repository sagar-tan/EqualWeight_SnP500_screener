import pandas as pd


def filter_by_sector(df, fundamentals_df=None, include=None, exclude=None):
    if fundamentals_df is None:
        return df
    include = include or None
    exclude = exclude or []
    merged = df.merge(fundamentals_df[['Ticker', 'sector']], on='Ticker', how='left')
    if include:
        merged = merged[merged['sector'].isin(include)]
    if exclude:
        merged = merged[~merged['sector'].isin(exclude)]
    return merged.drop(columns=['sector'], errors='ignore')