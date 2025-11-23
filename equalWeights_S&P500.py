import yfinance as yf
import pandas as pd
import math

#SETTINGS

PORTFOLIO_SIZE = 100000 #the capital for investment
ALLOW_FRACTIONAL = False # True means fractional shares allocated

sp500_ticker = yf.tickers_sp500()
sp500_ticker = list(sp500_ticker) # converting the ticker data into a list

print(f"Loaded {len(sp500_ticker)} tickers from S&P 500")

#fetch Prices

print("Downloading latest prices, this may take a few seconds...")
prices = yf.download(sp500_ticker, period="1d")["Close"].iloc[0]

df = pd.DataFrame({
    "Ticker" : prices.index,
    "Price": prices.values
})

# EQUAL Weights

