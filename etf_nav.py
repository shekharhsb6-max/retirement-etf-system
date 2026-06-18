import pandas as pd
import requests

print("Loading ETF Master...")

master = pd.read_csv("ETF_MASTER.csv")

print(f"{len(master)} ETFs found")

print("Downloading AMFI NAV data...")

url = "https://www.amfiindia.com/spages/NAVAll.txt"

response = requests.get(url, timeout=60)

response.raise_for_status()

amfi_data = response.text

rows = []

for _, row in master.iterrows():

    symbol = str(row["SYMBOL"]).strip()

    scheme_name = str(row["SCHEME_NAME"]).strip()

    nav_found = ""

    for line in amfi_data.splitlines():

        cols = line.split(";")

        if len(cols) < 5:
            continue

        amfi_scheme = cols[3].strip()

        try:
            nav = float(cols[4])
        except:
            continue

        if scheme_name.lower() in amfi_scheme.lower():

            nav_found = nav

            break

    rows.append([
        symbol,
        nav_found
    ])

    print(f"{symbol} -> {nav_found}")

df = pd.DataFrame(
    rows,
    columns=["SYMBOL","NAV"]
)

df.to_csv(
    "ETF_NAV.csv",
    index=False
)

print("\nETF_NAV.csv updated successfully")
