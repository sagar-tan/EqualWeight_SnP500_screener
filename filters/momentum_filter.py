import pandas as pd


# simple momentum over past N months
def filter_by_momentum(df, price_history_df=None, months=3, min_return=0.0):
    if price_history_df is None:
        return df
    # convert months to approx trading days
    days = months * 21
    pct = (price_history_df.iloc[-1] / price_history_df.shift(days).iloc[-1]) - 1
    pct = pct.reset_index()
    pct.columns = ['Ticker', 'momentum']
    merged = df.merge(pct, on='Ticker', how='left')
    merged = merged[merged['momentum'] >= min_return]
    return merged.drop(columns=['momentum'], errors='ignore')