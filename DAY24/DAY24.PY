import pandas as pd
import matplotlib.pyplot as plt

# -----------------------------------
# 1. Read Weather Data
# -----------------------------------

df = pd.read_csv("weather_data.csv")

# Convert Date column to datetime
df["Date"] = pd.to_datetime(df["Date"])

print("\n===== WEATHER DATA =====")
print(df)

# -----------------------------------
# 2. Average Temperature by City
# -----------------------------------

avg_temperature = (
    df.groupby("City")["Temperature"]
    .mean()
    .round(2)
    .sort_values(ascending=False)
)

print("\n===== AVERAGE TEMPERATURE BY CITY =====")
print(avg_temperature)

# -----------------------------------
# 3. Hottest and Coldest Cities
# -----------------------------------

hottest_city = avg_temperature.idxmax()
hottest_temp = avg_temperature.max()

coldest_city = avg_temperature.idxmin()
coldest_temp = avg_temperature.min()

print("\n===== HOTTEST CITY =====")
print(f"{hottest_city}: {hottest_temp}°C")

print("\n===== COLDEST CITY =====")
print(f"{coldest_city}: {coldest_temp}°C")

# -----------------------------------
# 4. Rainy and Sunny Days
# -----------------------------------

rainy_days = (df["Weather"].str.lower() == "rainy").sum()
sunny_days = (df["Weather"].str.lower() == "sunny").sum()

print("\n===== WEATHER DAYS =====")
print("Rainy Days:", rainy_days)
print("Sunny Days:", sunny_days)

# -----------------------------------
# 5. Weather Distribution
# -----------------------------------

weather_distribution = df["Weather"].value_counts()

print("\n===== WEATHER DISTRIBUTION =====")
print(weather_distribution)

# -----------------------------------
# 6. Temperature Trend
# -----------------------------------

daily_temperature = df.groupby("Date")["Temperature"].mean()

plt.figure(figsize=(10, 5))
plt.plot(
    daily_temperature.index,
    daily_temperature.values,
    marker="o"
)

plt.title("Temperature Trend")
plt.xlabel("Date")
plt.ylabel("Average Temperature (°C)")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("temperature_trend.png")
plt.show()

# -----------------------------------
# 7. Weather Distribution Chart
# -----------------------------------

plt.figure(figsize=(7, 7))

plt.pie(
    weather_distribution.values,
    labels=weather_distribution.index,
    autopct="%1.1f%%"
)

plt.title("Weather Distribution")
plt.tight_layout()
plt.savefig("weather_distribution.png")
plt.show()

# -----------------------------------
# 8. Average Temperature per City
# -----------------------------------

plt.figure(figsize=(10, 5))

avg_temperature.plot(kind="bar")

plt.title("Average Temperature per City")
plt.xlabel("City")
plt.ylabel("Average Temperature (°C)")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("average_temperature_city.png")
plt.show()

# -----------------------------------
# 9. Tomorrow's Temperature
#    Using Moving Average
# -----------------------------------

moving_average = (
    df.sort_values("Date")
    .groupby("Date")["Temperature"]
    .mean()
    .rolling(window=3)
    .mean()
)

predicted_temperature = moving_average.iloc[-1]

print("\n===== TOMORROW'S TEMPERATURE =====")
print(
    f"Predicted Temperature: "
    f"{predicted_temperature:.2f}°C"
)

# -----------------------------------
# 10. Create Final Report
# -----------------------------------

city_report = avg_temperature.reset_index()
city_report.columns = ["City", "Average Temperature"]

city_report["Temperature Category"] = city_report[
    "Average Temperature"
].apply(
    lambda x: (
        "Hot"
        if x >= 35
        else "Moderate"
        if x >= 25
        else "Cool"
    )
)

city_report.to_csv(
    "weather_final_report.csv",
    index=False
)

print("\nFinal report exported as weather_final_report.csv")