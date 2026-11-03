"""
50/200-day moving average backtest and drawdown charts (Python version of the Excel model).
"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import os

# --- Auto find Excel file so name error never happens ---
folder = os.path.dirname(os.path.abspath(__file__))
excel_files = [f for f in os.listdir(folder) if f.endswith(".xlsx")]
if not excel_files:
    raise SystemExit(f"No .xlsx file found in {folder}")
FILE = os.path.join(folder, excel_files[0])
print(f"Using file: {FILE}")

TRADING_DAYS = 252

# ---------- 1. Load Date and Close
sheets = pd.read_excel(FILE, sheet_name=None)
data = None
for name, sh in sheets.items():
    sh.columns = [str(c).strip() for c in sh.columns]
    if {"Date", "Close"}.issubset(sh.columns):
        data = sh[["Date", "Close"]].dropna().copy()
        break
if data is None:
    raise SystemExit("Could not find a sheet with 'Date' and 'Close' columns.")
data["Date"] = pd.to_datetime(data["Date"])
data = data.set_index("Date")
price = data["Close"]
print(f"{len(price)} trading days, {price.index[0]:%d %b %Y} to {price.index[-1]:%d %b %Y}")

# ---------- 2. Moving averages, signal, returns
ma50 = price.rolling(50).mean()
ma200 = price.rolling(200).mean()
signal = (ma50 > ma200).astype(float)
signal[ma200.isna()] = 0

daily_ret = price.pct_change().fillna(0)
strat_ret = signal.shift(1).fillna(0) * daily_ret

# ---------- 3. Growth of 1 unit, peak and drawdown
growth_s = (1 + strat_ret).cumprod()
growth_b = (1 + daily_ret).cumprod()
peak_s = growth_s.cummax()
peak_b = growth_b.cummax()
dd_s = growth_s / peak_s - 1
dd_b = growth_b / peak_b - 1

# ---------- 4. Summary numbers
years = len(price) / TRADING_DAYS
def summary(g, r, dd):
    return {"Total growth (x)": g.iloc[-1],
            "CAGR": g.iloc[-1] ** (1 / years) - 1,
            "Sharpe (annualized)": r.iloc[1:].mean() / r.iloc[1:].std() * np.sqrt(TRADING_DAYS),
            "Max drawdown": dd.min()}
res = pd.DataFrame({"50/200 MA strategy": summary(growth_s, strat_ret, dd_s),
                    "Buy & hold": summary(growth_b, daily_ret, dd_b)})
print()
print(f"{'':<22}{'Strategy':>12}{'Buy & hold':>12}")
print(f"{'Total growth':<22}{res.loc['Total growth (x)','50/200 MA strategy']:>11.2f}x{res.loc['Total growth (x)','Buy & hold']:>11.2f}x")
print(f"{'CAGR':<22}{res.loc['CAGR','50/200 MA strategy']*100:>11.1f}%{res.loc['CAGR','Buy & hold']*100:>11.1f}%")
print(f"{'Sharpe (annualized)':<22}{res.loc['Sharpe (annualized)','50/200 MA strategy']:>12.2f}{res.loc['Sharpe (annualized)','Buy & hold']:>12.2f}")
print(f"{'Max drawdown':<22}{res.loc['Max drawdown','50/200 MA strategy']*100:>11.1f}%{res.loc['Max drawdown','Buy & hold']*100:>11.1f}%")

# ---------- 5. Chart 1: growth of 1 unit
fig, ax = plt.subplots(figsize=(10, 5))
ax.plot(growth_s.index, growth_s, color="#2563A8", lw=2, label="50/200 MA strategy")
ax.plot(growth_b.index, growth_b, color="#D97706", lw=2, label="Buy & hold")
ax.set_title("Figure 1: Growth of 1 unit, 50/200 MA strategy vs buy-and-hold")
ax.set_ylabel("Growth of 1 unit"); ax.grid(alpha=0.25); ax.legend()
ax.xaxis.set_major_locator(mdates.YearLocator()); ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y"))
plt.tight_layout(); plt.savefig("figure1_growth.png", dpi=150)
plt.show()

# ---------- 6. Chart 2: drawdown from the previous peak
fig, ax = plt.subplots(figsize=(10, 5))
ax.plot(dd_s.index, dd_s * 100, color="#2563A8", lw=2, label="50/200 MA strategy")
ax.plot(dd_b.index, dd_b * 100, color="#D97706", lw=2, label="Buy & hold")
ax.fill_between(dd_s.index, dd_s * 100, 0, color="#2563A8", alpha=0.10)
for dd, c in ((dd_s, "#2563A8"), (dd_b, "#D97706")):
    d = dd.idxmin()
    ax.scatter([d], [dd.min() * 100], color=c, zorder=5)
    ax.annotate(f"{dd.min()*100:.1f}% ({d:%b %Y})", (d, dd.min() * 100),
                xytext=(10, -18), textcoords="offset points", color=c, fontweight="bold")
ax.axhline(0, color="black", lw=0.8)
ax.set_ylim(min(dd_s.min(), dd_b.min()) * 100 - 7, 3)
ax.set_title("Figure 2: Drawdown from previous peak")
ax.set_ylabel("Drawdown (%)"); ax.grid(alpha=0.25); ax.legend(loc="lower left")
ax.xaxis.set_major_locator(mdates.YearLocator()); ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y"))
plt.tight_layout(); plt.savefig("figure2_drawdown.png", dpi=150)
plt.show()
print("\nSaved: figure1_growth.png, figure2_drawdown.png")
