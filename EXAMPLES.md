# 📚 AITrader Examples

This document provides practical examples of using AITrader for various trading scenarios.

## Table of Contents
- [Basic Setup](#basic-setup)
- [Running Your First Trade](#running-your-first-trade)
- [Backtesting a Strategy](#backtesting-a-strategy)
- [Using the API](#using-the-api)
- [Multi-Agent Trading](#multi-agent-trading)
- [Custom Strategies](#custom-strategies)

## Basic Setup

### 1. Initial Account Configuration

Create `account.json` with your starting capital:

```json
[
    {
        "name": "gemini-flash-2.0",
        "credits": 1000000,
        "portfolio": []
    }
]
```

### 2. Download Market Data

```bash
python daily_update.py
```

This fetches the latest data for all configured stocks.

## Running Your First Trade

### Simple Trading Session

```bash
python main.py
```

**Expected Output:**
```
📈 Loaded and prepared RELIANCE
📈 Loaded and prepared TCS
📈 Loaded and prepared INFY
...

🤖 Agent: gemini-flash-2.0
➡️ RELIANCE: BUY 100 @ ₹2450.50
➡️ TCS: HOLD 0 @ ₹3890.25
➡️ INFY: BUY 50 @ ₹1520.00

📝 Trade Log:
🕒 2025-11-15 10:30:00: RELIANCE - BUY 100 @ ₹2450.50
   Cash After: ₹754950.0

✅ Daily trading completed successfully!
```

## Backtesting a Strategy

### Example 1: Test on Single Stock

```python
import pandas as pd
from indicators import add_indicators
from strategy import generate_signals
from backtest import backtest

# Load historical data
df = pd.read_csv("data/RELIANCE.csv")

# Add technical indicators
df = add_indicators(df)

# Generate buy/sell signals
df = generate_signals(df)

# Run backtest with ₹100,000 initial capital
initial_cash = 100000
final_value = backtest(df, initial_cash)

# Calculate returns
returns = ((final_value - initial_cash) / initial_cash) * 100

print(f"Initial Investment: ₹{initial_cash:,.2f}")
print(f"Final Value: ₹{final_value:,.2f}")
print(f"Total Return: {returns:.2f}%")
```

**Expected Output:**
```
Initial Investment: ₹100,000.00
Final Value: ₹145,320.50
Total Return: 45.32%
```

### Example 2: Compare Multiple Stocks

```python
import os
import pandas as pd
from indicators import add_indicators
from strategy import generate_signals
from backtest import backtest

stocks = ["RELIANCE", "TCS", "INFY", "HDFCBANK"]
initial_cash = 100000
results = {}

for stock in stocks:
    df = pd.read_csv(f"data/{stock}.csv")
    df = add_indicators(df)
    df = generate_signals(df)
    
    final_value = backtest(df, initial_cash)
    returns = ((final_value - initial_cash) / initial_cash) * 100
    
    results[stock] = {
        "final_value": final_value,
        "returns": returns
    }

# Display results
print(f"\n{'Stock':<15} {'Final Value':<15} {'Returns':<10}")
print("-" * 40)
for stock, data in sorted(results.items(), key=lambda x: x[1]["returns"], reverse=True):
    print(f"{stock:<15} ₹{data['final_value']:>12,.2f} {data['returns']:>8.2f}%")
```

**Expected Output:**
```
Stock           Final Value     Returns   
----------------------------------------
TCS             ₹152,450.00    52.45%
RELIANCE        ₹145,320.50    45.32%
INFY            ₹132,890.75    32.89%
HDFCBANK        ₹118,750.25    18.75%
```

## Using the API

### Start the API Server

```bash
python api.py
```

Server runs at `http://localhost:8000`

### API Examples

#### 1. Get All Accounts

```bash
curl http://localhost:8000/accounts
```

**Response:**
```json
[
    {
        "name": "gemini-flash-2.0",
        "credits": 754950.0,
        "portfolio": [
            {
                "symbol": "RELIANCE",
                "quantity": 100,
                "buy_price": 2450.50
            }
        ]
    }
]
```

#### 2. Get Specific Account

```bash
curl http://localhost:8000/accounts/gemini-flash-2.0
```

#### 3. Execute Buy Order

```bash
curl -X POST http://localhost:8000/buy \
  -H "Content-Type: application/json" \
  -d '{
    "agent_name": "gemini-flash-2.0",
    "symbol": "TCS",
    "quantity": 50,
    "price": 3890.25
  }'
```

#### 4. Execute Sell Order

```bash
curl -X POST http://localhost:8000/sell \
  -H "Content-Type: application/json" \
  -d '{
    "agent_name": "gemini-flash-2.0",
    "symbol": "RELIANCE",
    "quantity": 50,
    "price": 2480.00
  }'
```

#### 5. Get Portfolio Snapshots

```bash
curl http://localhost:8000/snapshots/gemini-flash-2.0
```

**Response:**
```json
[
    {
        "date": "2025-11-15",
        "agent_name": "gemini-flash-2.0",
        "credits": 754950.0,
        "portfolio": [...],
        "total_credits": 999875.0
    }
]
```

## Multi-Agent Trading

### Setup Multiple Agents

Edit `account.json`:

```json
[
    {
        "name": "aggressive-trader",
        "credits": 500000,
        "portfolio": []
    },
    {
        "name": "conservative-trader",
        "credits": 500000,
        "portfolio": []
    },
    {
        "name": "day-trader",
        "credits": 200000,
        "portfolio": []
    }
]
```

### Run Multi-Agent Session

```bash
python main.py
```

Each agent will make independent decisions based on the same market data.

### Compare Agent Performance

```python
import json

with open("account.json", "r") as f:
    accounts = json.load(f)

print(f"{'Agent':<25} {'Cash':<15} {'Portfolio Value':<15} {'Total':<15}")
print("-" * 70)

for agent in accounts:
    cash = agent["credits"]
    portfolio_value = sum(
        pos["quantity"] * pos["buy_price"] 
        for pos in agent["portfolio"]
    )
    total = cash + portfolio_value
    
    print(f"{agent['name']:<25} ₹{cash:>12,.2f} ₹{portfolio_value:>12,.2f} ₹{total:>12,.2f}")
```

## Custom Strategies

### Example: RSI-Based Strategy

Create `custom_strategy.py`:

```python
def generate_rsi_signals(df):
    """
    RSI-based strategy:
    - Buy when RSI < 30 (oversold)
    - Sell when RSI > 70 (overbought)
    """
    df["Signal"] = 0
    df.loc[df["RSI_14"] < 30, "Signal"] = 1   # Buy
    df.loc[df["RSI_14"] > 70, "Signal"] = -1  # Sell
    return df
```

### Example: MACD Crossover Strategy

```python
def generate_macd_signals(df):
    """
    MACD crossover strategy:
    - Buy when MACD crosses above signal line
    - Sell when MACD crosses below signal line
    """
    df["Signal"] = 0
    df.loc[df["MACD"] > df["MACD_signal"], "Signal"] = 1   # Buy
    df.loc[df["MACD"] < df["MACD_signal"], "Signal"] = -1  # Sell
    return df
```

### Test Custom Strategy

```python
import pandas as pd
from indicators import add_indicators
from backtest import backtest
from custom_strategy import generate_rsi_signals

df = pd.read_csv("data/RELIANCE.csv")
df = add_indicators(df)
df = generate_rsi_signals(df)

final_value = backtest(df, 100000)
print(f"RSI Strategy Final Value: ₹{final_value:,.2f}")
```

## Advanced Examples

### Portfolio Rebalancing

```python
import json

def rebalance_portfolio(agent_name, target_allocation):
    """
    Rebalance portfolio to match target allocation.
    
    target_allocation: dict like {"RELIANCE": 0.3, "TCS": 0.3, "INFY": 0.4}
    """
    with open("account.json", "r") as f:
        accounts = json.load(f)
    
    agent = next(a for a in accounts if a["name"] == agent_name)
    total_value = agent["credits"]
    
    # Calculate total portfolio value
    for pos in agent["portfolio"]:
        total_value += pos["quantity"] * pos["buy_price"]
    
    # Calculate target values
    target_values = {
        symbol: total_value * allocation 
        for symbol, allocation in target_allocation.items()
    }
    
    print(f"Total Portfolio Value: ₹{total_value:,.2f}")
    print("\nTarget Allocation:")
    for symbol, value in target_values.items():
        print(f"  {symbol}: ₹{value:,.2f}")

# Example usage
rebalance_portfolio("gemini-flash-2.0", {
    "RELIANCE": 0.25,
    "TCS": 0.25,
    "INFY": 0.25,
    "HDFCBANK": 0.25
})
```

### Risk Analysis

```python
import pandas as pd
import numpy as np

def calculate_risk_metrics(df):
    """Calculate various risk metrics."""
    df["Returns"] = df["Close"].pct_change()
    
    # Volatility (annualized)
    volatility = df["Returns"].std() * np.sqrt(252)
    
    # Maximum Drawdown
    cumulative = (1 + df["Returns"]).cumprod()
    running_max = cumulative.cummax()
    drawdown = (cumulative - running_max) / running_max
    max_drawdown = drawdown.min()
    
    # Sharpe Ratio (assuming 5% risk-free rate)
    risk_free_rate = 0.05
    excess_returns = df["Returns"].mean() * 252 - risk_free_rate
    sharpe_ratio = excess_returns / volatility
    
    return {
        "volatility": volatility,
        "max_drawdown": max_drawdown,
        "sharpe_ratio": sharpe_ratio
    }

# Calculate for multiple stocks
stocks = ["RELIANCE", "TCS", "INFY"]
for stock in stocks:
    df = pd.read_csv(f"data/{stock}.csv")
    metrics = calculate_risk_metrics(df)
    
    print(f"\n{stock} Risk Metrics:")
    print(f"  Volatility: {metrics['volatility']:.2%}")
    print(f"  Max Drawdown: {metrics['max_drawdown']:.2%}")
    print(f"  Sharpe Ratio: {metrics['sharpe_ratio']:.2f}")
```

## Scheduled Trading

### Windows Task Scheduler

Create `run_daily_trade.bat`:

```batch
@echo off
cd C:\Darshan\AITrader
python main.py >> logs\trading_%date:~-4,4%%date:~-10,2%%date:~-7,2%.log 2>&1
```

Schedule to run daily at market open (9:15 AM IST).

### Linux Cron

Add to crontab:

```bash
15 9 * * 1-5 cd /home/user/AITrader && python main.py >> logs/trading_$(date +\%Y\%m\%d).log 2>&1
```

## Troubleshooting Examples

### Check Data Freshness

```python
import pandas as pd
from datetime import datetime, timedelta

def check_data_freshness(symbol):
    df = pd.read_csv(f"data/{symbol}.csv")
    df["Date"] = pd.to_datetime(df["Date"])
    latest_date = df["Date"].max()
    days_old = (datetime.now() - latest_date).days
    
    print(f"{symbol}: Latest data from {latest_date.date()} ({days_old} days old)")
    
    if days_old > 5:
        print(f"⚠️ WARNING: Data is stale! Run daily_update.py")
    else:
        print(f"✅ Data is fresh")

stocks = ["RELIANCE", "TCS", "INFY"]
for stock in stocks:
    check_data_freshness(stock)
```

### Verify Account Balance

```python
import json

def verify_account_balance(agent_name):
    with open("account.json", "r") as f:
        accounts = json.load(f)
    
    agent = next(a for a in accounts if a["name"] == agent_name)
    
    print(f"\n💰 Account: {agent_name}")
    print(f"Cash: ₹{agent['credits']:,.2f}")
    print(f"\nPortfolio:")
    
    total_invested = 0
    for pos in agent["portfolio"]:
        value = pos["quantity"] * pos["buy_price"]
        total_invested += value
        print(f"  {pos['symbol']}: {pos['quantity']} @ ₹{pos['buy_price']:.2f} = ₹{value:,.2f}")
    
    print(f"\nTotal Portfolio Value: ₹{total_invested:,.2f}")
    print(f"Total Account Value: ₹{(agent['credits'] + total_invested):,.2f}")

verify_account_balance("gemini-flash-2.0")
```

---

For more examples and tutorials, check the [project wiki](https://github.com/darshan15062002/ai-Trader/wiki).
