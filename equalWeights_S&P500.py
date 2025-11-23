import yfinance as yf
import pandas as pd
import math
import lxml

#get list
url = "https://raw.githubusercontent.com/datasets/s-and-p-500-companies/master/data/constituents.csv"
table = pd.read_csv(url)
symbols = table["Symbol"].tolist()
print(f"loaded {len(symbols)} tickers")

#SETTINGS

PORTFOLIO_SIZE = 100000 #the capital for investment
ALLOW_FRACTIONAL = False # True means fractional shares allocated

#fetch Prices

print("Downloading latest prices, this may take a few seconds...")
prices = yf.download(symbols, period="1d")["Close"].iloc[0]

df = pd.DataFrame({#making a table that stores the ticker and price values
    "Ticker" : prices.index,
    "Price": prices.values
})

# EQUAL Weights

n = len(df)# finding out number of stocks in index
equal_weight = 1/n    # for equal weight dividing the number of stocks 

df["Weight"] = equal_weight # a table containing how much weight to be assigned

#Allocation

df["Dollar_Allocation"] = df["Weight"] * PORTFOLIO_SIZE

#No. of Shares allocation

if ALLOW_FRACTIONAL:
    df["Shares"] = df["Dollar_Allocation"]/df["Price"] # finding out share price if purchasing half stock is possible
else:
    df["Shares"] = (df["Dollar_Allocation"]/df["Price"]).apply(math.floor) # if fractional buying is not possible, we simply round down it which is meant by floor

#sort and save

df.sort_values("Ticker", inplace=True)      #sorting alphabetically
df.reset_index(drop=True, inplace=True)

#saving to excel
output_file = "Equal_Weight_SP500.xlsx"
df.to_excel(output_file, index=False)

print("output saved to : ", output_file)