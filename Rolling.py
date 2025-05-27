import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt


data = yf.download('TCS.NS', period='3mo', interval='1d')

data['Daily Return (%)'] = data['Close'].pct_change() * 100
data['7D Rolling Avg Return (%)'] = data['Daily Return (%)'].rolling(7).mean()
data['7D Rolling Std Dev (%)'] = data['Daily Return (%)'].rolling(7).std()

data_cleaned = data.dropna()

plt.figure(figsize=(14, 7))
plt.plot(data_cleaned.index, data_cleaned['Daily Return (%)'], alpha=0.5, label='Daily Return (%)')
plt.plot(data_cleaned.index, data_cleaned['7D Rolling Avg Return (%)'], linewidth=2, label='7D Rolling Avg Return (%)')
plt.plot(data_cleaned.index, data_cleaned['7D Rolling Std Dev (%)'], linewidth=2, label='7D Rolling Std Dev (%)')

plt.title("AAPL Daily Returns & 7-Day Rolling Stats (Last 6 Months)")
plt.xlabel("Date")
plt.ylabel("Percentage (%)")
plt.legend()
plt.grid(True)
plt.xticks(rotation=45)
manager = plt.get_current_fig_manager()
try:
    manager.window.showMaximized()   
except AttributeError:
    manager.full_screen_toggle()   
plt.tight_layout()
plt.show()
