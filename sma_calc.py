import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

def calculate_signals(data):
    data['SMA5']     = data['Close'].rolling(5).mean()
    data['SMA20']    = data['Close'].rolling(20).mean()
    data['Signal']   = np.where(data['SMA5'] > data['SMA20'], 1, 0)
    data['Position'] = data['Signal'].diff()
    return data

def calculate_strategy_return(data):
    buy_times  = list(data.index[data['Position'] ==  1])
    sell_times = list(data.index[data['Position'] == -1])

    if sell_times and buy_times and sell_times[0] < buy_times[0]:
        sell_times.pop(0)
    if buy_times and (len(buy_times) > len(sell_times)):
        sell_times.append(data.index[-1])

    trade_returns = []
    for buy_dt, sell_dt in zip(buy_times, sell_times):
        buy_price  = data.loc[buy_dt,  'Close']
        sell_price = data.loc[sell_dt, 'Close']
        trade_returns.append((sell_price / buy_price) - 1)

    cumulative = np.prod([1 + r for r in trade_returns])
    return (cumulative - 1) * 100

# === Main ===
ticker = 'TRENT.NS'
data   = yf.download(ticker, period='6mo', auto_adjust=False)

data = calculate_signals(data)
strategy_return = calculate_strategy_return(data)
print(f"Total Strategy Return over period: {strategy_return:.2f}%")

# 2. Compute SMAs
data['SMA5'] = data['Close'].rolling(5).mean()
data['SMA20'] = data['Close'].rolling(20).mean()

# 3. Generate signals
data['Signal'] = np.where(data['SMA5'] > data['SMA20'], 1, 0)
data['Position'] = data['Signal'].diff()

# 4. Set style
# 5. Create figure & axis
fig, ax = plt.subplots(figsize=(14, 8), dpi=100)

# 6. Plot price and SMAs
ax.plot(data.index, data['Close'], label='Close Price', linewidth=1.5, alpha=0.8)
ax.plot(data.index, data['SMA5'], label='5‑Day SMA', linewidth=2)
ax.plot(data.index, data['SMA20'], label='20‑Day SMA', linewidth=2)

# 7. Identify Buy/Sell points
buys  = data[data['Position'] == 1]
sells = data[data['Position'] == -1]

# 8. Highlight regions (optional)
for idx in buys.index:
    ax.axvspan(idx - pd.Timedelta(days=0.5),
               idx + pd.Timedelta(days=0.5),
               color='#2ca02c', alpha=0.1, zorder=1)
for idx in sells.index:
    ax.axvspan(idx - pd.Timedelta(days=0.5),
               idx + pd.Timedelta(days=0.5),
               color='#d62728', alpha=0.1, zorder=1)

# 9. Plot Buy signals
ax.scatter(buys.index, buys['SMA5'],
           marker='^', s=200,
           facecolors='#2ca02c', edgecolors='black',
           linewidths=1.5,
           label='Buy Signal', zorder=5)  # green :contentReference[oaicite:4]{index=4}

# 10. Plot Sell signals
ax.scatter(sells.index, sells['SMA5'],
           marker='v', s=200,
           facecolors='#d62728', edgecolors='black',
           linewidths=1.5,
           label='Sell Signal', zorder=5)  # red :contentReference[oaicite:5]{index=5}

# 11. Annotate signals
for idx, row in buys.iterrows():
    ax.annotate('BUY',
                xy=(idx, row['SMA5']),
                xytext=(0, 20),
                textcoords='offset points',
                ha='center', va='bottom',
                fontsize=12, fontweight='bold',
                color='#2ca02c',
                arrowprops=dict(arrowstyle='-|>', lw=1.5, color='#2ca02c'),
                zorder=6)  # bold, offset :contentReference[oaicite:6]{index=6}

for idx, row in sells.iterrows():
    ax.annotate('SELL',
                xy=(idx, row['SMA5']),
                xytext=(0, -25),
                textcoords='offset points',
                ha='center', va='top',
                fontsize=12, fontweight='bold',
                color='#d62728',
                arrowprops=dict(arrowstyle='-|>', lw=1.5, color='#d62728'),
                zorder=6)

# 12. Improve date formatting
ax.xaxis.set_major_locator(mdates.WeekdayLocator(interval=2))  # bi‑weekly :contentReference[oaicite:7]{index=7}
ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %d'))
fig.autofmt_xdate()

# 13. Legend and labels
ax.set_title(f'{ticker} SMA Crossover Strategy', fontsize=20, fontweight='bold')
ax.set_xlabel('Date', fontsize=16)
ax.set_ylabel('Price (USD)', fontsize=16)
ax.legend(loc='upper left', framealpha=0.8, fontsize=14)

manager = plt.get_current_fig_manager()
try:
    manager.window.showMaximized()   # works on QtAgg, TkAgg
except AttributeError:
    manager.full_screen_toggle()     # fallback
    
plt.tight_layout()
plt.show()
