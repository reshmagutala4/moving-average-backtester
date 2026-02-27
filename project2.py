import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Load data
df = pd.read_csv("Moving Average Strategy Backtester_(1).csv")

# Convert Date
df['Date'] = pd.to_datetime(df['Date'], format='%d-%m-%Y')
df = df.sort_values('Date')
df.set_index('Date', inplace=True)

# Calculate Moving Averages
df['SMA_50'] = df['Close'].rolling(window=50).mean()
df['SMA_200'] = df['Close'].rolling(window=200).mean()

# Generate Signals
df['Signal'] = 0
df.loc[df['SMA_50'] > df['SMA_200'], 'Signal'] = 1

# Strategy Returns
df['Daily_Return'] = df['Close'].pct_change()
df['Strategy_Return'] = df['Daily_Return'] * df['Signal'].shift(1)

# Cumulative Returns
df['Cumulative_Strategy'] = (1 + df['Strategy_Return']).cumprod()
df['Cumulative_BuyHold'] = (1 + df['Daily_Return']).cumprod()

# Performance Metrics
strategy_return = df['Cumulative_Strategy'].iloc[-1]
buyhold_return = df['Cumulative_BuyHold'].iloc[-1]

strategy_daily = df['Strategy_Return'].dropna()
sharpe_ratio = np.sqrt(252) * (strategy_daily.mean() / strategy_daily.std())

rolling_max = df['Cumulative_Strategy'].cummax()
drawdown = df['Cumulative_Strategy'] / rolling_max - 1
max_drawdown = drawdown.min()

# Print Results
print("Strategy Return:", strategy_return)
print("Buy & Hold Return:", buyhold_return)
print("Sharpe Ratio:", sharpe_ratio)
print("Maximum Drawdown:", max_drawdown)

# Plot
plt.figure(figsize=(10,5))
plt.plot(df['Cumulative_Strategy'], label='Strategy')
plt.plot(df['Cumulative_BuyHold'], label='Buy & Hold')
plt.legend()
plt.title("Moving Average Strategy Backtest")
plt.show()