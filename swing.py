import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

# 1. Download raw (auto_adjust=False) daily data
ticker = "AAPL"
data = yf.download(
    ticker,
    start="2020-01-01",
    end="2025-05-20",
    auto_adjust=False
)

# 2. Compute EMAs, MACD, Signal as Series
ema_short = data['Close'].ewm(span=12, adjust=False).mean()
ema_long  = data['Close'].ewm(span=26, adjust=False).mean()
macd      = (ema_short - ema_long).squeeze()            # ensure Series
signal    = macd.ewm(span=9, adjust=False).mean().squeeze()

# 3. Generate strictly alternating buy/sell signals
signals = []
position = 0  # 0 = flat, 1 = long

close = data['Close']

# generate strictly alternating buy/sell signals, storing Python floats
signals = []
position = 0  # 0 = flat, 1 = long

for i in range(1, len(data)):
    prev_macd = float(macd.iat[i-1])
    prev_sig  = float(signal.iat[i-1])
    curr_macd = float(macd.iat[i])
    curr_sig  = float(signal.iat[i])
    price     = float(close.iat[i])
    date      = data.index[i]

    # Buy when MACD crosses above Signal (flat → long)
    if position == 0 and prev_macd < prev_sig and curr_macd > curr_sig:
        signals.append(('buy', date, price))
        position = 1

    # Sell when MACD crosses below Signal (long → flat)
    elif position == 1 and prev_macd > prev_sig and curr_macd < curr_sig:
        signals.append(('sell', date, price))
        position = 0

# plotting remains unchanged…
# make sure you’re plotting the float prices in `buys` / `sells`

# --- total P/L calculation ---
def calculate_total_pl(signals):
    """
    Given a list of signals [('buy' or 'sell', date, price:float), ...]
    that strictly alternate buy → sell → buy → sell,
    compute total profit (sell − buy) across all completed trades.
    """
    total_pl = 0.0
    for i in range(0, len(signals), 2):
        if i+1 < len(signals) and signals[i][0]=='buy' and signals[i+1][0]=='sell':
            buy_price  = signals[i][2]
            sell_price = signals[i+1][2]
            total_pl  += (sell_price - buy_price)
    return float(total_pl)

pl = calculate_total_pl(signals)
print(f"Total P/L from {ticker} MACD strategy: {pl:.2f}")
plt.title(f"{ticker} Price with MACD Signals")
plt.xlabel("Date")
plt.ylabel("Price")
plt.legend()
plt.grid(True)

# 5. Plot MACD indicator
plt.figure(figsize=(12, 4))
plt.plot(macd,   label='MACD')
plt.plot(signal, label='Signal')
plt.title("MACD Indicator")
plt.xlabel("Date")
plt.ylabel("Value")
plt.legend()
plt.grid(True)

plt.tight_layout()
plt.show()
