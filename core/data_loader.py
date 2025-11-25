import yfinance as yf
import pandas as pd
import numpy as np
#fetching S&P 500 symbols form csv source
def get_sp500_symbols():
    url = "https://raw.githubusercontent.com/datasets/s-and-p-500-companies/master/data/constituents.csv"
    table = pd.read_csv(url)
    symbols = table["Symbol"].tolist()
    #converting the csv format to yfinance format
    symbols = [s.replace(".", "-") for s in symbols]
    return symbols
def fetch_latest_prices(symbols):
    prices = yf.download(symbols, period = "1d", threads = True, auto_adjust = True, progress = False)
    if "Close" in prices:
        close  = prices["Close"].iloc[0]
    else:
        close = prices.iloc[0]
    df = pd.DataFrame({"Ticker": close.index, "Price": close.values})
    df = df.dropna(subset=["Price"])
    return df
def fetch_fundamentals(symbols):
    infos = {}
    for s in symbols:
        try:
            t = yf.Ticker(s)
            info = t.info
            infos[s] = info
        except Exception:
            infos[s] = {}
    df = pd.DataFrame.from_dict(infos, orient = 'index')
    df.index.name = 'Ticker'
    df.reset_index(inplace=True)
    return df
def fetch_history(symbols, period= '1y'):
    hist = yf.download(symbols, period=period, auto_adjust = True, progress = False)
    if 'Close' in hist:
        return hist['Close']
    return hist
    

