import pandas as pd

master = pd.read_csv("ETF_MASTER.csv")

symbols_needed = pd.read_csv("ETF_NAV.csv")

master = master[
    master["SYMBOL"].isin(
        symbols_needed["SYMBOL"]
    )
]
