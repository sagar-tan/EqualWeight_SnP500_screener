PORTFOLIO_SIZE = 100000
ALLOW_FRACTIONAL = False
OUTPUT_FILE = "equal_weight_filtered.xlsx"
#adding the filter settings
FILTERS = {
    "price": {"min_price":5, "max_price": None},
    "volatility": {"window_days":60, "max_vol": 0.05},
    "pe": {"max_pe":50},
    "dividend": {"min_yield":0.0},
    "sector": {"include":None, "exclude":[]},
    "momentum": {"months":3, "min_return": 0.0},
    "volume": {"min_avg_volume":100000},
    "marketcap": {"min_mcap":1e9},
    "beta": {"max_beta": 2.0},
}

#pipeline order: order in which the filters will be applied

PIPELINE = [
    "price",
    "volume",
    "marketcap",
    "pe",
    "dividend",
    "beta",
    "volatility",
    "sector",
]