import pandas as pd
import requests

ETF_MAP = {
    "NIFTYBEES": "Nifty BeES",
    "JUNIORBEES": "Junior BeES",
    "BANKBEES": "Bank BeES",
    "GOLDBEES": "Gold BeES",
    "SILVERBEES": "Silver ETF",
    "MON100": "Motilal Oswal Nasdaq 100 ETF",
    "MONIFTY500": "Motilal Oswal Nifty 500 ETF",
    "MASPTOP50": "Mirae Asset S&P 500 Top 50 ETF",
    "MIDCAPETF": "Midcap ETF",
    "NIF100BEES": "Nifty 100 ETF",
    "CPSEETF": "CPSE ETF",
    "ICICI22": "Bharat 22 ETF",
    "INFRAIETF": "Infrastructure ETF",
    "METALIETF": "Metal ETF",
    "MOCAPITAL": "Capital Market ETF",
    "LIQUIDCASE": "Liquid ETF"
}

print("Downloading AMFI NAV data...")

url = "https://www.amfiindia.com/spages/NAVAll.txt"

response = requests.get(url, timeout=60)
response.raise_for_status()

data = response.text

rows = []

for line in data.splitlines():

    cols = line.split(";")

    if len(cols) < 5:
        continue

    scheme_name = cols[3].strip()

    try:
        nav = float(cols[4])
    except:
        continue

    for symbol, search_text in ETF_MAP.items():

        if search_text.lower() in scheme_name.lower():

            rows.append({
                "SYMBOL": symbol,
                "NAV": nav
            })

df = pd.DataFrame(rows)

if not df.empty:

    df = (
        df.sort_values("SYMBOL")
          .drop_duplicates(subset=["SYMBOL"], keep="first")
    )

else:

    df = pd.DataFrame(columns=["SYMBOL", "NAV"])

df.to_csv("ETF_NAV.csv", index=False)

print(df)

print(f"\nETF_NAV.csv created with {len(df)} records")
