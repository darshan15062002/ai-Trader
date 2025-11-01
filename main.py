import pandas as pd
from indicators import add_indicators
from strategy import generate_signals
from backtest import backtest
import os

# DATA_DIR = "data"

# def run_backtest_for_stock(symbol):
#     path = os.path.join(DATA_DIR, f"{symbol}.csv")
#     df = pd.read_csv(path, parse_dates=["Date"], index_col="Date")
#     df = add_indicators(df)
#     df = generate_signals(df)
#     print(f"🔍 Running backtest for {}...")
#     result = backtest(df)
#     print(f"📊 {symbol}: Final portfolio value = ₹{result}")

# if __name__ == "__main__":
#     stocks = ["RELIANCE", "TCS", "INFY", "HDFCBANK", "ICICIBANK",
#               "SBIN", "BHARTIARTL", "HINDUNILVR", "LT", "ITC"]
    
#     for s in stocks:
#         run_backtest_for_stock(s)

data_dir = "data"
stock_data = {}



for filename in os.listdir(data_dir):
    if filename.endswith(".csv"):
        symbol = filename.replace(".csv", "")
        df = pd.read_csv(os.path.join(data_dir, filename))
        df = add_indicators(df)
        # Extract only the latest indicator values
        latest = df[["SMA_20", "SMA_50", "RSI_14", "MACD", "MACD_signal", "MACD_diff"]].iloc[-1].to_dict()

        # Store in stock_data for the agent to use
        stock_data[symbol] = latest
        print(f"📈 Loaded and prepared {symbol}")

print(stock_data)
