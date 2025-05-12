import pandas as pd

# RSI (Relative Strength Index)
def compute_rsi(series, period=14):
    delta = series.diff()
    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)
    avg_gain = gain.rolling(window=period).mean()
    avg_loss = loss.rolling(window=period).mean()
    rs = avg_gain / (avg_loss + 1e-9)
    rsi = 100 - (100 / (1 + rs))
    return rsi

# MACD (Moving Average Convergence Divergence)
def compute_macd(series, short_window=12, long_window=26, signal_window=9):
    ema_short = series.ewm(span=short_window, adjust=False).mean()
    ema_long = series.ewm(span=long_window, adjust=False).mean()
    macd_line = ema_short - ema_long
    signal_line = macd_line.ewm(span=signal_window, adjust=False).mean()
    macd_hist = macd_line - signal_line
    return macd_hist

# ROC (Rate of Change)
def compute_roc(series, period=12):
    return series.pct_change(periods=period) * 100