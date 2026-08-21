import streamlit as st
import pandas as pd

# -----------------------------------
# Page Configuration
# -----------------------------------

st.set_page_config(
    page_title="Weather Analytics Dashboard",
    page_icon="🌦️",
    layout="wide"
)

st.title("🌦️ Weather Data Analytics Dashboard")
st.write("Interactive Weather Data Analysis System")

# -----------------------------------
# Load Dataset
# -----------------------------------

df = pd.read_csv("weather_data.csv")

df["Date"] = pd.to_datetime(df["Date"])

# -----------------------------------
# Sidebar Filters
# -----------------------------------

st.sidebar.header("🔎 Filters")

cities = st.sidebar.multiselect(
    "Select City",
    options=sorted(df["City"].unique()),
    default=sorted(df["City"].unique())
)

weather_types = st.sidebar.multiselect(
    "Select Weather",
    options=sorted(df["Weather"].unique()),
    default=sorted(df["Weather"].unique())
)

filtered_df = df[
    (df["City"].isin(cities)) &
    (df["Weather"].isin(weather_types))
]

# -----------------------------------
# Display Data
# -----------------------------------

st.subheader("📋 Weather Data")

st.dataframe(
    filtered_df,
    use_container_width=True
)

# -----------------------------------
# KPI Metrics
# -----------------------------------

if not filtered_df.empty:

    avg_temp = filtered_df["Temperature"].mean()

    hottest_city = (
        filtered_df.groupby("City")["Temperature"]
        .mean()
        .idxmax()
    )

    hottest_temp = (
        filtered_df.groupby("City")["Temperature"]
        .mean()
        .max()
    )

    rainy_days = (
        filtered_df["Weather"]
        .str.lower()
        .eq("rainy")
        .sum()
    )

    sunny_days = (
        filtered_df["Weather"]
        .str.lower()
        .eq("sunny")
        .sum()
    )

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "🌡 Average Temperature",
        f"{avg_temp:.2f} °C"
    )

    col2.metric(
        "🔥 Hottest City",
        hottest_city,
        f"{hottest_temp:.2f} °C"
    )

    col3.metric(
        "🌧 Rainy Days",
        rainy_days
    )

    col4.metric(
        "☀️ Sunny Days",
        sunny_days
    )

    # -----------------------------------
    # Temperature Trend
    # -----------------------------------

    st.subheader("🌡 Temperature Trend")

    daily_temp = (
        filtered_df
        .groupby("Date")["Temperature"]
        .mean()
    )

    st.line_chart(daily_temp)

    # -----------------------------------
    # Average Temperature by City
    # -----------------------------------

    st.subheader("📊 Average Temperature per City")

    city_temp = (
        filtered_df
        .groupby("City")["Temperature"]
        .mean()
        .sort_values(ascending=False)
    )

    st.bar_chart(city_temp)

    # -----------------------------------
    # Weather Distribution
    # -----------------------------------

    st.subheader("🌧️ Weather Distribution")

    weather_count = filtered_df["Weather"].value_counts()

    st.bar_chart(weather_count)

    # -----------------------------------
    # Moving Average Prediction
    # -----------------------------------

    st.subheader("🔮 Tomorrow's Temperature Prediction")

    daily_temperature = (
        filtered_df
        .groupby("Date")["Temperature"]
        .mean()
        .sort_index()
    )

    if len(daily_temperature) >= 3:

        moving_average = (
            daily_temperature
            .rolling(window=3)
            .mean()
        )

        prediction = moving_average.iloc[-1]

        st.success(
            f"Predicted temperature for tomorrow: "
            f"{prediction:.2f} °C"
        )

    else:

        st.warning(
            "At least 3 days of data are required "
            "for moving-average prediction."
        )

    # -----------------------------------
    # Final Report
    # -----------------------------------

    st.subheader("📥 Export Final Report")

    report = (
        filtered_df
        .groupby("City")["Temperature"]
        .mean()
        .reset_index()
    )

    report.columns = [
        "City",
        "Average Temperature"
    ]

    csv = report.to_csv(index=False)

    st.download_button(
        label="📥 Download Weather Report",
        data=csv,
        file_name="weather_final_report.csv",
        mime="text/csv"
    )

else:

    st.warning(
        "No data available for the selected filters."
    )