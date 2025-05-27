import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

ticker = 'AAPL'
data = yf.download(ticker, period='6mo', auto_adjust=False)

data['SMA5'] = data['Close'].rolling(5).mean()
data['SMA20'] = data['Close'].rolling(20).mean()

data['Signal'] = np.where(data['SMA5'] > data['SMA20'], 1, 0)
data['Position'] = data['Signal'].diff()

fig, ax = plt.subplots(figsize=(14, 8), dpi=100)

ax.plot(data.index, data['Close'], label='Close Price', linewidth=1.5, alpha=0.8)
ax.plot(data.index, data['SMA5'], label='5‑Day SMA', linewidth=2)
ax.plot(data.index, data['SMA20'], label='20‑Day SMA', linewidth=2)

buys  = data[data['Position'] == 1]
sells = data[data['Position'] == -1]

for idx in buys.index:
    ax.axvspan(idx - pd.Timedelta(days=0.5),
               idx + pd.Timedelta(days=0.5),
               color='#2ca02c', alpha=0.1, zorder=1)
for idx in sells.index:
    ax.axvspan(idx - pd.Timedelta(days=0.5),
               idx + pd.Timedelta(days=0.5),
               color='#d62728', alpha=0.1, zorder=1)

ax.scatter(buys.index, buys['SMA5'],
           marker='^', s=200,
           facecolors='#2ca02c', edgecolors='black',
           linewidths=1.5,
           label='Buy Signal', zorder=5)  

ax.scatter(sells.index, sells['SMA5'],
           marker='v', s=200,
           facecolors='#d62728', edgecolors='black',
           linewidths=1.5,
           label='Sell Signal', zorder=5)   


for idx, row in buys.iterrows():
    ax.annotate('BUY',
                xy=(idx, row['SMA5']),
                xytext=(0, 20),
                textcoords='offset points',
                ha='center', va='bottom',
                fontsize=12, fontweight='bold',
                color='#2ca02c',
                arrowprops=dict(arrowstyle='-|>', lw=1.5, color='#2ca02c'),
                zorder=6) 
    
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




ax.set_title(f'{ticker} SMA Crossover Strategy', fontsize=20, fontweight='bold')
ax.set_xlabel('Date', fontsize=16)
ax.set_ylabel('Price (USD)', fontsize=16)
ax.legend(loc='upper left', framealpha=0.8, fontsize=14)

manager = plt.get_current_fig_manager()
try:
    manager.window.showMaximized()  
except AttributeError:
    manager.full_screen_toggle()     
    
plt.tight_layout()
plt.show()
