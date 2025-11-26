import pandas as pd
def safe_merge(left, right, on = 'Ticker'):
    return left.merge(right, on=on, how = 'left')
def summary_stats(df, portfolio_size):
    invested = (df['Shares']*df['Price']).sum()
    remaining = portfolio_size-invested
    return{
        
    }

