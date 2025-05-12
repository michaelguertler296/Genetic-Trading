def simulate_portfolio(df, initial_cash=100.0):
    df = df.copy()

    df['cash'] = 0.0
    df['trade'] = 0.0
    df['position'] = 0.0
    df['portfolio_value'] = 0.0
    df['sp_strategy'] = 0.0
    df['cash_strategy'] = 0.0
    df['dca_strategy'] = 0.0

    cash = initial_cash
    dca_cash = initial_cash
    position = 0.0
    dca_position = 0.0
    sp_value = initial_cash

    for i in range(1, len(df)):
        signal = df.loc[i - 1, 'signals']  # Use yesterday's signal
        price_return = df.loc[i, 'daily_return']

        if signal > 0:
            trade = signal * cash  # Use % of cash to buy
            cash -= trade
            position += trade
        elif signal < 0:
            trade = abs(signal) * position  # Sell % of position
            cash += trade
            position -= trade
        else:
            trade = 0.0

        # S&P 500 Buy-and-Hold strategy
        sp_value *= (1 + price_return)
        df.loc[i, 'sp_strategy'] = sp_value

        # Cash Strategy
        df.loc[i, 'cash_strategy'] = initial_cash  # Constant for reference

        # DCA Strategy (1% of cash per day for 100 days)
        if i < 100:
            dca_trade = 0.01 * initial_cash
            dca_cash -= dca_trade
            dca_position += dca_trade
        else:
            dca_cash += dca_trade
            dca_position -= dca_trade

        dca_position *= (1 + price_return)
        df.loc[i, 'dca_strategy'] = dca_position + dca_cash
    
        # Update current position value with market movement
        position *= (1 + price_return)

        df.loc[i, 'cash'] = cash
        df.loc[i, 'trade'] = trade
        df.loc[i, 'position'] = position
        df.loc[i, 'portfolio_value'] = cash + position
      

    # Set first row values
    df.loc[0, ['cash', 'position', 'portfolio_value', 'sp_strategy', 'cash_strategy', 'dca_strategy']] = initial_cash
    
    return df