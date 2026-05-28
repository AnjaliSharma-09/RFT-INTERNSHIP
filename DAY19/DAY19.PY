import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# CREATE SAMPLE DATASET

dates = pd.date_range(start='2025-01-01', periods=30)

stock_price = [
    100, 102, 101, 105, 108,
    107, 110, 115, 117, 120,
    119, 121, 125, 130, 128,
    126, 129, 135, 140, 138,
    142, 145, 143, 147, 150,
    148, 151, 155, 153, 158
]

df = pd.DataFrame({
    'Date': dates,
    'Stock Price': stock_price
})

# Save dataset to CSV
df.to_csv("stock_prices.csv", index=False)

print("Dataset Created Successfully!\n")
print(df.head())

# MOVING AVERAGE


# Calculate 5-Day Moving Average
df['Moving Average'] = df['Stock Price'].rolling(window=5).mean()

print("\nDataset with Moving Average:\n")
print(df.head(10))

# IDENTIFY PEAKS & DROPS

# Peak = Price greater than previous & next
# Drop = Price lower than previous & next

peaks = []
drops = []

for i in range(1, len(df)-1):

    # Peak Detection
    if (df['Stock Price'][i] > df['Stock Price'][i-1]) and \
       (df['Stock Price'][i] > df['Stock Price'][i+1]):
        peaks.append(i)

    # Drop Detection
    if (df['Stock Price'][i] < df['Stock Price'][i-1]) and \
       (df['Stock Price'][i] < df['Stock Price'][i+1]):
        drops.append(i)

print("\nPeak Points:")
print(df.loc[peaks, ['Date', 'Stock Price']])

print("\nDrop Points:")
print(df.loc[drops, ['Date', 'Stock Price']])

# VOLATILITY DETECTION (BONUS)

# Daily Returns
df['Daily Return'] = df['Stock Price'].pct_change()

# Volatility = Standard Deviation of Returns
volatility = df['Daily Return'].std()

print("\nStock Volatility:", volatility)

# VISUALIZATION

plt.figure(figsize=(14, 7))

# Original Stock Price
plt.plot(df['Date'],
         df['Stock Price'],
         label='Stock Price',
         linewidth=2)

# Moving Average
plt.plot(df['Date'],
         df['Moving Average'],
         label='5-Day Moving Average',
         linestyle='--',
         linewidth=2)

# Peaks
plt.scatter(df.loc[peaks, 'Date'],
            df.loc[peaks, 'Stock Price'],
            marker='^',
            s=100,
            label='Peaks')

# Drops
plt.scatter(df.loc[drops, 'Date'],
            df.loc[drops, 'Stock Price'],
            marker='v',
            s=100,
            label='Drops')

# Labels & Title
plt.title("Stock Price Time-Series Analysis", fontsize=16)
plt.xlabel("Date")
plt.ylabel("Stock Price")
plt.legend()
plt.grid(True)

plt.show()

# MULTIPLE STOCK COMPARISON (BONUS)

# Sample Additional Stocks
df['Stock B'] = df['Stock Price'] + np.random.randint(-5, 6, size=len(df))
df['Stock C'] = df['Stock Price'] + np.random.randint(-10, 11, size=len(df))

plt.figure(figsize=(14, 7))

plt.plot(df['Date'], df['Stock Price'], label='Stock A')
plt.plot(df['Date'], df['Stock B'], label='Stock B')
plt.plot(df['Date'], df['Stock C'], label='Stock C')

plt.title("Multiple Stock Comparison")
plt.xlabel("Date")
plt.ylabel("Stock Price")
plt.legend()
plt.grid(True)

plt.show()

print("\nTime-Series Analysis Completed Successfully!")