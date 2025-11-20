import pandas as pd
from indicators import add_indicators
from strategy import generate_signals
from backtest import backtest
import os
import json
from agent.gemini_agent import decide_action
from daily_update import update_market_data
import sys
import datetime



data_dir = "data"
ACCOUNT_FILE = "account.json" 
stock_data = {}



for filename in os.listdir(data_dir):
    if filename.endswith(".csv"):
        symbol = filename.replace(".csv", "")
        df = pd.read_csv(os.path.join(data_dir, filename))
        df = add_indicators(df)
        # Extract only the latest indicator values
        latest = df[["SMA_20", "SMA_50", "RSI_14", "MACD", "MACD_signal", "MACD_diff", "price"]].iloc[-1].to_dict()

        # Store in stock_data for the agent to use
        stock_data[symbol] = latest
        print(f"📈 Loaded and prepared {symbol}")

print(stock_data)

trade_log = []
def main():
    with open(ACCOUNT_FILE, "r") as f:
        accounts = json.load(f)

    for account in accounts:
        print(f"\n🤖 Agent: {account['name']}")
        portfolio = account.get("portfolio", [])
        cash = account.get("credits", 0)


        # Ask Gemini for next actions
        actions = decide_action(account["name"], portfolio, stock_data, cash)
        print(actions)
        for decision in actions["decisions"]:
            symbol = decision["symbol"]
            action = decision["action"].upper()
            qty = decision["quantity"]
            price = stock_data[symbol].get("price", 0)
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            print(f"➡️ {symbol}: {action} {qty} @ ₹{price}")

            if action == "BUY" and qty > 0:
                cost = qty * price
                if cost > cash:
                    print(f"⚠️ Insufficient funds to buy {qty}x {symbol} (Need ₹{cost}, have ₹{cash})")
                    continue

                cash -= cost
                

                # Check if symbol already in portfolio
                found = next((s for s in portfolio if s["symbol"] == symbol), None)
                if found:
                    # Update average buy price
                    
                    total_qty = found["quantity"] + qty
                    found["buy_price"] = (
                        (found["buy_price"] * found["quantity"]) + cost
                    ) / total_qty
                    found["quantity"] = total_qty
                else:
                    portfolio.append({
                        "symbol": symbol,
                        "quantity": qty,
                        "buy_price": price
                    })

                trade_log.append({
                    "time": timestamp,
                    "symbol": symbol,
                    "action": "BUY",
                    "quantity": qty,
                    "price": price,
                    "cash_after": cash
                })

            elif action == "SELL" and qty > 0:
                found = next((s for s in portfolio if s["symbol"] == symbol), None)
                if not found:
                    print(f"⚠️ Attempted to sell {symbol} not in portfolio.")
                    continue

                qty_to_sell = min(qty, found["quantity"])
                revenue = qty_to_sell * price
                cash += revenue
                found["quantity"] -= qty_to_sell

                realized_profit = (price - found["buy_price"]) * qty_to_sell
                if found["quantity"] == 0:
                    portfolio.remove(found)

                trade_log.append({
                    "time": timestamp,
                    "symbol": symbol,
                    "action": "SELL",
                    "quantity": qty_to_sell,
                    "price": price,
                    "profit": realized_profit,
                    "cash_after": cash
                })

            else:
                print(f"⏸️ {symbol}: No action or invalid quantity.")

         # 🔁 IMPORTANT: Update the account in memory with new state
        account["portfolio"] = portfolio
        account["credits"] = cash

    # 💾 Save all updated accounts back to file
    with open(ACCOUNT_FILE, "w") as f:
        json.dump(accounts, f, indent=4)

    print("\n📝 Trade Log:")
    for trade in trade_log:
        print(f"🕒 {trade['time']}: {trade['symbol']} - {trade['action']} {trade['quantity']} @ ₹{trade['price']}")
        if trade['action'] == "SELL":
            print(f"   Profit: ₹{trade['profit']}")
        print(f"   Cash After: ₹{trade['cash_after']}")

if __name__ == "__main__":
    try:
        update_market_data()
        main()
        print("✅ Daily trading completed successfully!")
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)  # Critical: tells Render job failed


