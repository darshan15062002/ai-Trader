# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Comprehensive README with features, installation, and usage guide
- MIT License for open-source distribution
- Contributing guidelines (CONTRIBUTING.md)
- Code of Conduct
- GitHub issue templates (bug report, feature request, question)
- Pull request template
- Examples and tutorials (EXAMPLES.md)
- Project documentation improvements

### Changed
- Enhanced project documentation structure
- Improved code organization

### Security
- API key should be moved to environment variables (TODO)

## [1.0.0] - 2025-11-15

### Added
- Initial release of AITrader
- Gemini AI integration for trading decisions
- Technical indicators (SMA, RSI, MACD)
- Portfolio management system
- Multi-agent support
- FastAPI REST API
- Backtesting engine
- Daily market data updates
- Trade logging and history
- Snapshot system for portfolio tracking
- Report engine with template support
- Web dashboard interface

### Features
- **AI Trading Agent**
  - Google Gemini 2.5 Flash integration
  - Intelligent decision-making based on technical indicators
  - Multi-stock analysis

- **Technical Analysis**
  - Simple Moving Averages (SMA 20, SMA 50)
  - Relative Strength Index (RSI 14)
  - MACD with signal line and histogram
  - Customizable indicator parameters

- **Portfolio Management**
  - Real-time portfolio tracking
  - Position management (buy/sell/hold)
  - Profit/loss calculation
  - Cash management

- **Data Management**
  - yfinance integration for market data
  - CSV data storage
  - Daily data updates
  - Historical data analysis

- **API Endpoints**
  - Account management
  - Trade execution
  - Portfolio snapshots
  - Stock data access

### Supported Stocks
- RELIANCE (Reliance Industries)
- TCS (Tata Consultancy Services)
- INFY (Infosys)
- HDFCBANK (HDFC Bank)
- ICICIBANK (ICICI Bank)
- BHARTIARTL (Bharti Airtel)
- SBIN (State Bank of India)
- ITC (ITC Limited)
- LT (Larsen & Toubro)
- HINDUNILVR (Hindustan Unilever)

### Known Issues
- API key hardcoded (should use environment variables)
- Limited error handling in some modules
- No stop-loss mechanism
- No real-time data streaming

### Dependencies
- yfinance - Market data
- pandas - Data manipulation
- ta - Technical analysis
- google.generativeai - AI decision-making
- fastapi - REST API
- uvicorn - ASGI server
- motor - MongoDB async driver
- jinja2 - Template engine
- python-dotenv - Environment variables

---

## Release Notes

### Version 1.0.0 - Initial Release

This is the first public release of AITrader. The system is fully functional for:
- Automated trading with AI decision-making
- Technical analysis and backtesting
- Portfolio management
- API access for monitoring

**⚠️ Important Notes:**
- This is educational software - use at your own risk
- Test thoroughly with paper trading before real money
- Not financial advice

**Getting Started:**
1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt`
3. Configure Gemini API key
4. Run: `python main.py`

**Future Plans:**
- Enhanced risk management
- More technical indicators
- Real-time data streaming
- Mobile app
- Broker API integration
- Machine learning models

---

For detailed information about each version, see the [releases page](https://github.com/darshan15062002/ai-Trader/releases).
