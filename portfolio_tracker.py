import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

# Portfolio configuration
portfolio = {
    "INFY.NS": 15,
    "TCS.NS": 10,
    "RELIANCE.NS": 12
}

# Download adjusted close prices for the last 30 days
tickers = list(portfolio.keys())
data = yf.download(tickers, period='30d', interval='1d', auto_adjust=True)['Close']

# Drop rows with any missing data
data.dropna(inplace=True)

# Calculate portfolio value per day
portfolio_value = pd.Series(0, index=data.index)
for stock, shares in portfolio.items():
    portfolio_value += data[stock] * shares
print(portfolio_value , '\n' ,portfolio )

# Print latest total portfolio value
latest_value = portfolio_value.iloc[-1]
print(f"Latest Total Portfolio Value (INR): ₹{latest_value:,.2f}")

# Plot portfolio value
plt.figure(figsize=(12, 6))
plt.plot(portfolio_value.index, portfolio_value.values, marker='o', linewidth=2)
plt.title("Total Portfolio Value Over Last 30 Days")
plt.xlabel("Date")
plt.ylabel("Portfolio Value (INR)")
plt.grid(True)
plt.tight_layout()
plt.xticks(rotation=45)
plt.show()


