# Moving Average Strategy Backtester

Backtest of a 50/200-day moving average crossover on one stock, compared with buy-and-hold. Built in Excel, then repeated in Python (Pandas, NumPy, Matplotlib).

## Rule

- Hold the stock when the 50-day average is above the 200-day average, otherwise stay in cash
- Each day's signal is applied to the next day's return, so the test never uses future information

## Result (1 Feb 2019 to 20 Feb 2026, 1,773 trading days)

| Measure | 50/200 MA strategy | Buy and hold |
|---|---|---|
| Growth of 1 unit | 2.70x | 4.10x |
| CAGR | 15.1% | 22.2% |
| Annualized volatility | 23.0% | 28.6% |
| Sharpe ratio (annualized, risk-free = 0) | 0.73 | 0.85 |
| Maximum drawdown | **-28.0%** | -37.1% |

The strategy was in the market on 1,219 of the 1,773 days. Its worst drawdown (-28.0%) came in the March 2020 crash, when it was still invested. It then moved to cash during the 2022 decline, where buy-and-hold fell to -37.1% (Nov 2022). The strategy earned less and had a lower Sharpe ratio than buy-and-hold, because it also missed part of the rallies.

## Limitations

- One stock and one pair of moving averages, so it does not show how the rule works elsewhere
- No trading costs, taxes or slippage
- Returns are 0 during the first 200 days, before a signal exists
- Sharpe ratio uses a risk-free rate of 0
- Historical results do not predict future returns

## Files

- `Moving_Average_Strategy_Backtester (1).xlsx`: prices, signals, returns, summary sheet
- `Moving_average_backtest.py`: Python version (keep it in the same folder as the .xlsx file and run it). It gives the same results as Excel: 15.1% CAGR, 0.73 Sharpe, -28.0% max drawdown
- `figure1_growth.png`, `figure2_drawdown.png`: growth and drawdown charts
