import pandas as pd

def filter_by_pe(df, fundamentals_df=None, max_pe=50):
    if fundamentals_df is None:
        return df
    merged = df.merge(fundamentals_df[['Ticker', 'trailingPE', 'forwardPE']], on='Ticker', how='left')
    merged['pe'] = merged['trailingPE'].fillna(merged['forwardPE'])
    merged = merged[merged['pe'].notna()]
    merged = merged[merged['pe'] <= max_pe]
    return merged.drop(columns=['trailingPE','forwardPE','pe'], errors='ignore')