import yfinance as yf
import pandas as pd
import os
import json
from datetime import datetime, timedelta
from indicators import add_indicators

DATA_DIR = "data"
ACCOUNT_FILE = "account.json"  # to store each agent’s cash & holdings

def fetch_yesterday_data(symbol):
    """Download yesterday’s data for a given stock"""
    end = datetime.now()
    start = end - timedelta(days=5)  # buffer in case of holidays
    df = yf.download(symbol + ".NS", start=start, end=end)
    print(f"⬇️ Fetched data for {symbol} from {start.date()} to {end.date()}")
    
    if df.empty:
        print(f"⚠️ No new data for {symbol}")
        return None
        
    # Flatten manually: take only the second-level columns
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.droplevel(0)  # drop "Price" level
    df.reset_index(inplace=True)

    # Now rename columns explicitly
    df.columns = ["Date", "Close", "High", "Low", "Open", "Volume"]
    df["Close"] = df["Close"].astype(float).round(6)
    df["High"] = df["High"].astype(float).round(6)
    df["Low"] = df["Low"].astype(float).round(6)
    df["Open"] = df["Open"].astype(float).round(6)
    df["Volume"] = df["Volume"].astype(float).astype(int)

    # df["Date"] = pd.to_datetime(df["Date"]).dt.strftime("%m/%d/%Y")
    # need this formate 2025-10-30 no timestamp
    
    df["Date"] = pd.to_datetime(df["Date"]).dt.strftime("%Y-%m-%d")
    # df["Date"] = df["Date"].dt.strftime("%y-%m-%d")
    

    return df.tail(1)

def update_csv(symbol):
   
    """Append yesterday’s data to existing CSV"""
    file_path = os.path.join(DATA_DIR, f"{symbol}.csv")
    new_data = fetch_yesterday_data(symbol)
    
    if new_data is None:
        return None

    # Load old data
    df_old = pd.read_csv(file_path)
    df_combined = pd.concat([df_old, new_data]).drop_duplicates(subset=["Date"])
    df_combined.to_csv(file_path, index=False)
    print(f"📅 Updated {symbol}.csv with {new_data['Date'].iloc[-1]}")
    return df_combined

def update_agent_accounts(symbol, df):
    """Update each agent’s portfolio with profit/loss based on the latest close."""

    latest = df.iloc[-1]
    latest_close = latest["Close"]

    # Load JSON as a normal Python object (list of dicts)
    with open(ACCOUNT_FILE, "r") as f:
        accounts = json.load(f)

    for account in accounts:
        portfolio = account.get("portfolio", [])
        credits = account.get("credits", 0)
        total_credits = account.get("total_credits", 0)

        for stock in portfolio:
            if stock["symbol"] == symbol:
                # Calculate today's profit/loss
                today_profit_loss = (latest_close - stock["buy_price"]) * stock["quantity"]

                # Update fields
                stock["total_profit_loss"] = stock.get("total_profit_loss", 0) + today_profit_loss
                stock["price"] = latest_close
                stock["last_updated"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                # Adjust credits (optional: if you want realized gains reflected)
                account["credits"] = credits + today_profit_loss
                print(f"🤖 Agent {account['name']} | {symbol}: ₹{today_profit_loss:.2f} today | Total: ₹{stock['total_profit_loss']:.2f}")

    # Save updates
    with open(ACCOUNT_FILE, "w") as f:
        json.dump(accounts, f, indent=4)


def main():
    symbols = [ "RELIANCE","TCS", "INFY", "HDFCBANK", "ICICIBANK","SBIN", "BHARTIARTL", "HINDUNILVR", "LT", "ITC"]
    for symbol in symbols:
        df = update_csv(symbol)
        return
        if df is not None:
            update_agent_accounts(symbol, df)
        break

if __name__ == "__main__":
    main()
