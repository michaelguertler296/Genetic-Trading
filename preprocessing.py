import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from visualization import plot_sp500_data
from economic_indicators import compute_roc, compute_macd, compute_rsi


def process_data(df):
    df = df.sort_values("date").reset_index(drop=True)

    # Compute economic indicators
    df['short_ma'] = df['SP500'].rolling(window=5).mean()  # Short moving average
    df['medium_ma'] = df['SP500'].rolling(window=10).mean()  # Medium moving average
    df['long_ma'] = df['SP500'].rolling(window=20).mean()  # Long moving average
    df['rsi'] = compute_rsi(df['SP500']) # Relative Strength Index
    df['macd'] = compute_macd(df['SP500']) # Moving Average Convergence Divergence
    df['roc'] = compute_roc(df['SP500'])

    # Compute daily returns
    df['daily_return'] = df['SP500'].pct_change().fillna(0)

    # Drop the first 20 rows to ensure all moving averages are valid
    df = df.iloc[20:].reset_index(drop=True)
    return df