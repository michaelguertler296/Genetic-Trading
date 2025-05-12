import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler, StandardScaler
from config import FRED_API_KEY, start_date, end_date
from data_fetching import fetch_fred_series
from visualization import plot_sp500_data, plot_simulation_results
from genetic_algorithm import GeneticAlgorithm
from preprocessing import process_data
from simulation import simulate_portfolio

# Fetch S&P Data
series_id = 'SP500'  # S&P 500 index from FRED
df = fetch_fred_series(series_id)

# Preprocess S&P Data
df = process_data(df)

# Set features and returns
features = ['short_ma', 'medium_ma', 'long_ma', 'rsi', 'macd', 'roc']
X = df[features].values
daily_returns = df['daily_return'].values

# Normalize feature matrix X
scaler = StandardScaler()
X = scaler.fit_transform(X)

# Genetic Algorthm Settings
ga = GeneticAlgorithm(
    population_size=500,
    generations=1000,
    mutation_rate=0.25,
    crossover_rate=0.5
)

# Run Genetic Algorithm
best_solution = ga.run(X, daily_returns)
# print('Best solution:', best_solution)

# Develop buy/sell signals using NN output between -1 and 1
df['signals'] = ga.generate_signal(best_solution, X)

# Simulate the portfolio
df = simulate_portfolio(df)

# Plot Portfolio Value 
plot_simulation_results(df)

# Guess for tomorrow's S&P 500 movement
latest_features = X[-1].reshape(1, -1)  # Shape (1, num_features)
tomorrow_signal = ga.generate_signal(best_solution, latest_features)[0]

print(f"Predicted signal for tomorrow: {tomorrow_signal:.4f}")