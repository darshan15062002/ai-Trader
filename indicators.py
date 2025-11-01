import pandas as pd
import ta

def add_indicators(df: pd.DataFrame) -> pd.DataFrame:
    """
    Takes a DataFrame with columns: ['Date', 'Open', 'High', 'Low', 'Close', 'Volume']
    and returns a new DataFrame with added technical indicators.
    """

    # Ensure 'Close' column exists
    if "Close" not in df.columns:
        raise ValueError("DataFrame must contain 'Close' column")

    # --- Moving Averages ---
    df["SMA_20"] = df["Close"].rolling(window=20, min_periods=1).mean()
    df["SMA_50"] = df["Close"].rolling(window=50, min_periods=1).mean()

    # --- RSI (Relative Strength Index) ---
    rsi = ta.momentum.RSIIndicator(close=df["Close"], window=14, fillna=True)
    df["RSI_14"] = rsi.rsi()

    # --- MACD (Moving Average Convergence Divergence) ---
    macd = ta.trend.MACD(close=df["Close"], fillna=True)
    df["MACD"] = macd.macd()
    df["MACD_signal"] = macd.macd_signal()
    df["MACD_diff"] = macd.macd_diff()

    # --- Drop rows with missing data from early periods ---
    df = df.dropna().copy()

    # --- Set index properly if not done ---
    if "Date" in df.columns:
        df["Date"] = pd.to_datetime(df["Date"])
        df.set_index("Date", inplace=True)

    return df
