import pandas as pd
from indicators import add_indicators
from strategy import generate_signals
from backtest import backtest
import os
import json
from agent.gemini_agent import decide_action



data_dir = "data"
ACCOUNT_FILE = "account.json" 
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

def main():
    with open(ACCOUNT_FILE, "r") as f:
        accounts = json.load(f)

    for account in accounts:
        print(f"\n🤖 Agent: {account['name']}")
        portfolio = account.get("portfolio", [])
        cash = account.get("credits", 0)

        # Ask Gemini for next actions
        actions = decide_action(account["name"], portfolio, stock_data, cash)
        print(actions,"dfdsfsdf")

    


if __name__ == "__main__":
    main()


