import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
tickers = [
    "TCS.NS", "INFY.NS", "HDFCBANK.NS", "RELIANCE.NS", "ICICIBANK.NS",
    "HINDUNILVR.NS", "ITC.NS", "KOTAKBANK.NS", "LT.NS", "SBIN.NS",
    "M&M.NS", "HDFCLIFE.NS", "AXISBANK.NS", "HCLTECH.NS", "BAJFINANCE.NS",
    "ASIANPAINT.NS", "ULTRACEMCO.NS", "BHARTIARTL.NS", "MARUTI.NS", "TITAN.NS"
]

percent_changes = {}
for ticker in tickers:
    try:
        data = yf.download(ticker, period="1mo", interval="1d",
                           auto_adjust=True, progress=False)
    except Exception as e:
        print(f"Warning: Could not download data for {ticker}: {e}")
        continue
    if data is None or data.empty or "Close" not in data.columns:
        print(f"Warning: No data for {ticker}, skipping.")
        continue
    if isinstance(data.columns, pd.MultiIndex):
        data.columns = data.columns.get_level_values(0)

    if "Close" not in data.columns:
      print(f"Warning: 'Close' column not found for {ticker}, skipping.")
      continue

    data = data.dropna(subset=["Close"])
    if data.empty:
        print(f"Warning: Missing prices for {ticker}, skipping.")
        continue
    first_price = data["Close"].iloc[0]
    last_price = data["Close"].iloc[-1]
    if first_price == 0:
        continue
    pct_change = (last_price - first_price) / first_price * 100
    percent_changes[ticker] = pct_change

changes_series = pd.Series(percent_changes)

top_gainers = changes_series.nlargest(5)
top_losers = changes_series[changes_series < 0].nsmallest(5)

print("Top 5 Gainers:\n", top_gainers)
print("\nTop 5 Losers:\n", top_losers)

plot_tickers = list(top_gainers.index) + list(top_losers.index)
plot_changes = list(top_gainers.values) + list(top_losers.values)
colors = ['green'] * len(top_gainers) + ['red'] * len(top_losers)

plt.figure(figsize=(10, 6))
bars = plt.bar(plot_tickers, plot_changes, color=colors)
plt.axhline(0, color='black', linewidth=0.8)
plt.title("Top 5 Gainers and Losers (Past Month)")
plt.ylabel("Percentage Change (%)")
plt.xticks(rotation=45)
plt.tight_layout()

for bar in bars:
    yval = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2.0,
             yval + (1 if yval > 0 else -3),
             f"{yval:.2f}%", ha='center',
             va='bottom' if yval > 0 else 'top')


plt.show()

output_df = pd.DataFrame({
    "Symbol": plot_tickers,
    "Percent Change": plot_changes
})
output_df.to_csv("gainers_losers.csv", index=False)
