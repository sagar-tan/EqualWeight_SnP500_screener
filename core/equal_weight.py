import pandas as pd
import math

def apply_equal_weight(df, portfolio_size, allow_fractional = False):
    df = df.copy()
    n = len(df)
    if n == 0 :
        return df
    df['Weight'] = 1.0/n
    df['Dollar_Allocation'] = df['Weight'] * portfolio_size
    if allow_fractional:
        df['Shares'] = df['Dollar_Allocation'] / df['Price']
    else:
        df['Shares'] = (df['Dollar_allocation']) / df['Price'].apply(lambda x: math.floor(x) if pd.notna(x) else 0)
    return df
