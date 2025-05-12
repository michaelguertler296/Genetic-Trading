import matplotlib.pyplot as plt

def plot_sp500_data(df):
    plt.figure(figsize=(10, 5))
    plt.plot(df['date'], df['SP500'], label='S&P 500')
    plt.title('S&P 500 Index Prices')
    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.legend()
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

def plot_simulation_results(df):
    plt.figure(figsize=(12, 6))
    # plt.plot(df['date'], df['cash'], label='cash', color='blue')
    # plt.plot(df['date'], df['position'], label='S&P 500', color='orange')
    plt.plot(df['date'], df['portfolio_value'], label='portfolio', color='green')
    plt.plot(df['date'], df['cash_strategy'], label='cash strategy', color='red')
    plt.plot(df['date'], df['sp_strategy'], label='S&P 500 strategy', color='purple')
    plt.plot(df['date'], df['dca_strategy'], label='DCA strategy', color='brown')
    plt.xlabel("Date")
    plt.ylabel("USD")
    plt.title("Trading Strategy Portfolio Value")
    plt.legend()
    plt.grid(True)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()