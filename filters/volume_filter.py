import pandas as pd

def filter_by_volume(df, fundamentals_df = None, min_avg_volume = 10000):
    merged= df.merge(fundamentals_df[['Ticker', 'averageVolume', 'averageVolume10days', 'volume']], on= 'Ticker', how='left')
    merged['avg_vol'] = merged['averageVolume'].fillna(merged['averageVolume10days']).fillna(merged['volume'])
    merged = merged[merged['avg_vol'] >= min_avg_volume]
    return merged.drop(columns=['averageVolume','averageVolume10days','volume','avg_vol'], errors='ignore')