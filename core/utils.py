import pandas as pd
def safe_merge(left, right, on = 'Ticker'):
    return left.merge(right, on=on, how = 'left')

def summary_stats(df, portfolio_size):  #literally just tells the status of the stocks
    invested = (df['Shares']*df['Price']).sum()
    remaining = portfolio_size-invested
    return{
        'n_stocks': len(df),
        'invested': invested,
        'remaining_cash': remaining,
        'Total_Portfolio': portfolio_size
    }

