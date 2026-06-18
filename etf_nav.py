import pandas as pd
import requests

print("Loading ETF_MASTER.csv...")

master = pd.read_csv("ETF_MASTER.csv")

print(f"{len(master)} ETFs loaded")

print("Downloading AMFI NAV data...")

url = "https://www.amfiindia.com/spages/NAVAll.txt"

response = requests.get(url, timeout=60)
response.raise_for_status()

amfi_data = response.text.splitlines()

rows = []

for _, row in master.iterrows():

    symbol = str(row["SYMBOL"]).strip()
    scheme_name = str(row["SCHEME_NAME"]).strip()

    nav_found = ""
    matched_scheme = ""

    for line in amfi_data:

        cols = line.split(";")

        if len(cols) < 5:
            continue

        amfi_scheme = cols[3].strip()

        try:
            nav = float(cols[4])
        except:
            continue

        # EXACT MATCH
      

            nav_found = nav
            matched_scheme = amfi_scheme

            break

    if nav_found == "":
        print(f"NO MATCH: {symbol} -> {scheme_name}")
    else:
        print(f"MATCHED: {symbol} -> {nav_found}")

    rows.append([
        symbol,
        nav_found
    ])

df = pd.DataFrame(
    rows,
    columns=["SYMBOL", "NAV"]
)

df.to_csv(
    "ETF_NAV.csv",
    index=False
)

print("\nETF_NAV.csv created successfully")
print(df)
