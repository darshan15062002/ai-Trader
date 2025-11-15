# 🤖 AITrader - AI-Powered Stock Trading System

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Gemini AI](https://img.shields.io/badge/Powered%20by-Gemini%20AI-4285F4)](https://ai.google.dev/)

An intelligent automated trading system that uses Google's Gemini AI to make data-driven trading decisions on Indian stock markets (NSE). The system combines technical indicators with AI-powered decision-making to manage portfolios autonomously.

![AITrader Architecture](https://via.placeholder.com/800x400/1a1a2e/ffffff?text=AITrader+System+Architecture)

## 🌟 Features

### Core Capabilities
- **🧠 AI-Powered Decision Making**: Uses Google Gemini 2.5 Flash for intelligent trading decisions
- **📊 Technical Analysis**: Implements multiple indicators (SMA, RSI, MACD)
- **💼 Portfolio Management**: Multi-agent system with independent portfolios
- **📈 Real-time Data**: Fetches live market data using yfinance
- **🔄 Automated Trading**: Daily automated execution with trade logging
- **📉 Backtesting Engine**: Test strategies on historical data
- **🌐 REST API**: FastAPI-based interface for monitoring and control
- **📸 Snapshot System**: Daily portfolio snapshots for performance tracking

### Technical Highlights
- Multiple trading agents running concurrently
- Risk management with cash position tracking
- Trade history and performance analytics
- Configurable trading strategies
- MongoDB integration for data persistence
- Report generation system

## 🏗️ Architecture

```
AITrader/
├── main.py              # Main trading execution engine
├── agent/               # AI trading agents
│   └── gemini_agent.py  # Gemini AI decision-making logic
├── api.py               # FastAPI REST endpoints
├── strategy.py          # Trading strategy implementations
├── indicators.py        # Technical indicator calculations
├── backtest.py          # Backtesting engine
├── daily_update.py      # Market data updater
├── snapshot.py          # Portfolio snapshot management
├── data/                # Historical stock data (CSV)
├── ReportEngine/        # Reporting and analysis system
└── templates/           # Web dashboard templates
```

### System Flow

```
┌─────────────────┐
│  Market Data    │ (yfinance)
│  Fetcher        │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Technical      │ (SMA, RSI, MACD)
│  Indicators     │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Gemini AI      │ (Decision Making)
│  Agent          │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Trade          │ (Buy/Sell/Hold)
│  Execution      │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Portfolio      │ (MongoDB/JSON)
│  Management     │
└─────────────────┘
```

## 🚀 Getting Started

### Prerequisites

- Python 3.8 or higher
- Google Gemini API key
- MongoDB (optional, for data persistence)
- Internet connection for market data

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/darshan15062002/ai-Trader.git
cd ai-Trader
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Set up your Gemini API key**
```python
# Edit agent/gemini_agent.py
genai.configure(api_key="YOUR_API_KEY_HERE")
```

4. **Initialize account configuration**
```bash
# Create account.json with initial setup
{
    "name": "agent-1",
    "credits": 1000000,
    "portfolio": []
}
```

### Quick Start

#### Run a Single Trading Session
```bash
python main.py
```

#### Update Market Data
```bash
python daily_update.py
```

#### Run Backtesting
```bash
python backtest.py
```

#### Start the API Server
```bash
python api.py
# Access at http://localhost:8000
```

## 📊 Supported Stocks

Currently tracking 10 major NSE stocks:
- **RELIANCE** - Reliance Industries
- **TCS** - Tata Consultancy Services
- **INFY** - Infosys
- **HDFCBANK** - HDFC Bank
- **ICICIBANK** - ICICI Bank
- **BHARTIARTL** - Bharti Airtel
- **SBIN** - State Bank of India
- **ITC** - ITC Limited
- **LT** - Larsen & Toubro
- **HINDUNILVR** - Hindustan Unilever

## 🧪 Technical Indicators

### Moving Averages
- **SMA 20**: 20-day Simple Moving Average
- **SMA 50**: 50-day Simple Moving Average

### Momentum Indicators
- **RSI 14**: Relative Strength Index (14 periods)
  - Overbought: > 70
  - Oversold: < 30

### Trend Indicators
- **MACD**: Moving Average Convergence Divergence
- **MACD Signal**: Signal line
- **MACD Diff**: Histogram

## 🎯 Trading Strategy

The AI agent considers multiple factors:

1. **Trend Analysis**: SMA crossovers for trend direction
2. **Momentum**: RSI for overbought/oversold conditions
3. **Confirmation**: MACD for momentum confirmation
4. **Risk Management**: Position sizing based on available capital
5. **Portfolio Balance**: Diversification across multiple stocks

### Example Decision Logic
```python
# Bullish signals
- SMA_20 > SMA_50  (Uptrend)
- RSI < 70  (Not overbought)
- MACD > MACD_signal  (Positive momentum)
→ BUY signal

# Bearish signals
- SMA_20 < SMA_50  (Downtrend)
- RSI > 30  (Not oversold)
- MACD < MACD_signal  (Negative momentum)
→ SELL signal
```

## 📡 API Endpoints

### Portfolio Management
- `GET /` - Dashboard view
- `GET /accounts` - List all trading accounts
- `GET /accounts/{agent_name}` - Get specific agent details
- `GET /snapshots/{agent_name}` - Get portfolio snapshots

### Trade Operations
- `POST /buy` - Execute buy order
- `POST /sell` - Execute sell order

### Market Data
- `GET /stocks` - List all tracked stocks
- `GET /stocks/{symbol}` - Get specific stock data

## 📈 Performance Tracking

The system automatically creates daily snapshots of:
- Portfolio value
- Individual position P&L
- Total credits (cash + holdings)
- Trade history

Access snapshots via:
```bash
GET http://localhost:8000/snapshots/{agent_name}
```

## 🔧 Configuration

### Account Setup (`account.json`)
```json
[
    {
        "name": "gemini-flash-2.0",
        "credits": 1000000,
        "portfolio": []
    }
]
```

### Adding More Stocks

1. Edit `daily_update.py` to add stock symbols
2. Run data update: `python daily_update.py`
3. Restart the system

## 🧪 Backtesting

Test your strategies on historical data:

```python
from backtest import backtest
import pandas as pd
from indicators import add_indicators

df = pd.read_csv("data/RELIANCE.csv")
df = add_indicators(df)
final_value = backtest(df, initial_cash=100000)
print(f"Final Portfolio Value: ₹{final_value}")
```

## 📊 Report Engine

The ReportEngine module provides:
- HTML report generation
- Template-based analysis
- Multi-language support
- Custom LLM integration

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes:

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

See [CONTRIBUTING.md](CONTRIBUTING.md) for detailed guidelines.

## 🛣️ Roadmap

- [ ] Add more technical indicators (Bollinger Bands, Fibonacci)
- [ ] Implement stop-loss and take-profit mechanisms
- [ ] Real-time WebSocket data streaming
- [ ] Advanced risk management algorithms
- [ ] Multi-timeframe analysis
- [ ] Sentiment analysis from news/social media
- [ ] Mobile app for monitoring
- [ ] Paper trading mode
- [ ] Integration with broker APIs for live trading
- [ ] Machine learning model for pattern recognition

## ⚠️ Disclaimer

**This is educational software for learning purposes only.**

- Not financial advice
- Use at your own risk
- Test thoroughly with paper trading before real money
- Past performance doesn't guarantee future results
- The developers are not responsible for any financial losses

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Google Gemini AI for intelligent decision-making
- yfinance for market data
- TA-Lib for technical indicators
- FastAPI for the REST API framework
- The open-source community

## 📧 Contact

**Darshan** - [@darshan15062002](https://github.com/darshan15062002)

Project Link: [https://github.com/darshan15062002/ai-Trader](https://github.com/darshan15062002/ai-Trader)

---

⭐ **If you find this project useful, please consider giving it a star!** ⭐

## 📸 Screenshots

### Dashboard
![Dashboard](https://via.placeholder.com/800x400/2c3e50/ffffff?text=Trading+Dashboard)

### Performance Analytics
![Analytics](https://via.placeholder.com/800x400/34495e/ffffff?text=Performance+Analytics)

---

Made with ❤️ by Darshan
