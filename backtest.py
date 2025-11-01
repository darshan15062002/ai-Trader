def backtest(df, initial_cash=10000):
    cash = initial_cash
    position = 0  # number of shares
    prev_signal = 0

    for i in range(1, len(df)):
        price = df["Close"].iloc[i]
        signal = df["Signal"].iloc[i]

        # Buy signal
        if signal == 1 and prev_signal != 1:
            position = cash / price
            cash = 0

        # Sell signal
        elif signal == -1 and prev_signal != -1:
            cash = position * price
            position = 0

        prev_signal = signal

    # Final value
    final_value = cash if position == 0 else position * df["Close"].iloc[-1]
    return round(final_value, 2)
