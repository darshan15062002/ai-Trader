def generate_signals(df):
    """
    Simple moving average crossover strategy:
    Buy when short SMA crosses above long SMA, sell when below.
    """
    df["Signal"] = 0
    df.loc[df["SMA_20"] > df["SMA_50"], "Signal"] = 1   # Buy
    df.loc[df["SMA_20"] < df["SMA_50"], "Signal"] = -1  # Sell
    return df