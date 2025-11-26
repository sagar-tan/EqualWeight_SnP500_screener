import pandas as pd

def filter_by_price(df, min_price=5, max_price=None):
    if min_price is not None:
        df = df[df['Price']>=min_price]
    if max_price is not None:
        df = df[df['Price']<=max_price]
    return df
