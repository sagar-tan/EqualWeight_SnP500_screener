import pandas as pd

# calculate daily returns std over a window and filter by max_vol (fractional daily std)
def filter_by_volatility(df, price_history_df=None, window_days=60, max_vol=0.05):
    if price_history_df is None:
        return df

    returns = price_history_df.pct_change().dropna()

    vol = returns.rolling(window=window_days).std().iloc[-1]

    vol = vol.reset_index()
    vol.columns = ['Ticker', 'volatility']

    merged = df.merge(vol, on='Ticker', how='left')

    merged = merged[merged['volatility'] <= max_vol]

    return merged.drop(columns=['volatility'], errors='ignore')
