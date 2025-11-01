# # import yfinance as yf

# # data = yf.download("RELIANCE.NS", start="2023-01-01", end="2025-11-01")
# # print(data.head())
# # from nsepy import get_history
# # from datetime import date

# # data = get_history(symbol="RELIANCE",
# #                    start=date(2023,1,1),
# #                    end=date(2025,11,1))
# # print(data.head())

# import yfinance as yf
# from datetime import datetime, timedelta
# import os
# import pandas as pd

# # Create data folder if not exists
# os.makedirs("data", exist_ok=True)

# # Top 10 Indian stocks
# stocks = [
  
#      "LT.NS", "ITC.NS"
# ]

# # Date range – last 1 year
# end_date = datetime.now()
# start_date = end_date - timedelta(days=365)

# print(f"Fetching data from {start_date.date()} to {end_date.date()}")

# for symbol in stocks:
#     try:
#         print(f"📥 Downloading {symbol} ...")
#         data = yf.download(symbol, start=start_date, end=end_date, progress=False)
        
#         if data.empty:
#             print(f"⚠️ No data returned for {symbol}")
#             continue
        
#         # Clean data
#         data = data.dropna().sort_index()
#         data.index.name = "Date"

#         # Save to CSV
#         filename = f"data/{symbol.replace('.NS', '')}.csv"
#         data.to_csv(filename)
#         print(f"✅ Saved {symbol} to {filename}")
        
#     except Exception as e:
#         print(f"❌ Error fetching {symbol}: {e}")

# print("\n🎉 All stock data downloaded successfully!")

import pandas as pd
import os
from pathlib import Path

# Input and output folders
raw_folder = "data"
clean_folder = "cleaned_data"

# Ensure output folder exists
os.makedirs(clean_folder, exist_ok=True)

for filename in os.listdir(raw_folder):
    if filename.endswith(".csv"):
        file_path = os.path.join(raw_folder, filename)
        clean_path = os.path.join(clean_folder, filename)

        try:
            # Yahoo CSV has extra headers — skip first two rows
            df = pd.read_csv(file_path, header=1)

            # The first row often contains 'Ticker' — drop it
            df = df[df["Date"].str.contains(r"\d", na=False)]

            # Convert Date to datetime
            df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
            df.dropna(subset=["Date"], inplace=True)
            df.set_index("Date", inplace=True)

            # Keep only relevant columns
            df = df[["Open", "High", "Low", "Close", "Volume"]]

            # Convert numeric columns
            df = df.apply(pd.to_numeric, errors="coerce")
            df.dropna(inplace=True)

            # Sort by date
            df.sort_index(inplace=True)

            # Save cleaned CSV
            df.to_csv(clean_path)
            print(f"✅ Cleaned: {filename}")

        except Exception as e:
            print(f"❌ Error cleaning {filename}: {e}")

print("\n🎯 All done! Clean files saved to:", Path(clean_folder).resolve())
