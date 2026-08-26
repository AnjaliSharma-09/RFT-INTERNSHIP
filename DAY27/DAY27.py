import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import re
from collections import Counter

# -----------------------------
# Page Configuration
# -----------------------------
st.set_page_config(
    page_title="Social Media Trend Analyzer",
    page_icon="📱",
    layout="wide"
)

st.title("📱 Social Media Trend Analyzer")
st.write("Analyze hashtags, users, engagement, posting times and sentiment.")

# -----------------------------
# Load Data
# -----------------------------
uploaded_file = st.sidebar.file_uploader(
    "Upload Social Media CSV",
    type=["csv"]
)

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
else:
    try:
        df = pd.read_csv("social_media_data.csv")
    except FileNotFoundError:
        st.error("social_media_data.csv not found.")
        st.stop()

# -----------------------------
# Data Cleaning
# -----------------------------
df.columns = df.columns.str.strip()

required_columns = [
    "Post_ID", "User", "Date", "Time",
    "Hashtags", "Category", "Likes",
    "Comments", "Shares", "Text"
]

missing_columns = [
    col for col in required_columns if col not in df.columns
]

if missing_columns:
    st.error(f"Missing columns: {missing_columns}")
    st.stop()

df["Date"] = pd.to_datetime(df["Date"], errors="coerce")

df["Likes"] = pd.to_numeric(df["Likes"], errors="coerce").fillna(0)
df["Comments"] = pd.to_numeric(df["Comments"], errors="coerce").fillna(0)
df["Shares"] = pd.to_numeric(df["Shares"], errors="coerce").fillna(0)

df["Engagement"] = (
    df["Likes"] +
    df["Comments"] +
    df["Shares"]
)

# -----------------------------
# Sentiment Analysis
# -----------------------------
positive_words = {
    "good", "great", "amazing", "excellent",
    "love", "happy", "awesome", "exciting",
    "beautiful", "fun", "best", "wonderful"
}

negative_words = {
    "bad", "poor", "hate", "sad",
    "terrible", "worst", "angry",
    "boring", "awful", "disappointing"
}


def sentiment_analysis(text):
    words = re.findall(r"\b\w+\b", str(text).lower())

    positive = sum(word in positive_words for word in words)
    negative = sum(word in negative_words for word in words)

    if positive > negative:
        return "Positive"
    elif negative > positive:
        return "Negative"
    else:
        return "Neutral"


df["Sentiment"] = df["Text"].apply(sentiment_analysis)

# -----------------------------
# Sidebar Filters
# -----------------------------
st.sidebar.header("🔎 Filters")

categories = sorted(df["Category"].dropna().unique())

selected_categories = st.sidebar.multiselect(
    "Select Category",
    categories,
    default=categories
)

users = sorted(df["User"].dropna().unique())

selected_users = st.sidebar.multiselect(
    "Select Users",
    users,
    default=users
)

search_text = st.sidebar.text_input(
    "Search Post Text"
)

filtered_df = df[
    df["Category"].isin(selected_categories) &
    df["User"].isin(selected_users)
]

if search_text:
    filtered_df = filtered_df[
        filtered_df["Text"].str.contains(
            search_text,
            case=False,
            na=False
        )
    ]

# -----------------------------
# KPI Section
# -----------------------------
st.subheader("📊 Key Statistics")

col1, col2, col3, col4, col5 = st.columns(5)

col1.metric(
    "Total Posts",
    len(filtered_df)
)

col2.metric(
    "Total Likes",
    int(filtered_df["Likes"].sum())
)

col3.metric(
    "Total Comments",
    int(filtered_df["Comments"].sum())
)

col4.metric(
    "Total Shares",
    int(filtered_df["Shares"].sum())
)

col5.metric(
    "Total Engagement",
    int(filtered_df["Engagement"].sum())
)

# -----------------------------
# Hashtag Analysis
# -----------------------------
st.header("🔥 Top Trending Hashtags")

hashtags = []

for value in filtered_df["Hashtags"].dropna():
    tags = re.findall(r"#\w+", str(value).lower())
    hashtags.extend(tags)

hashtag_counts = Counter(hashtags)

hashtag_df = pd.DataFrame(
    hashtag_counts.items(),
    columns=["Hashtag", "Count"]
).sort_values(
    "Count",
    ascending=False
)

if not hashtag_df.empty:

    top_hashtags = hashtag_df.head(10)

    fig, ax = plt.subplots()

    ax.bar(
        top_hashtags["Hashtag"],
        top_hashtags["Count"]
    )

    ax.set_title("Top Trending Hashtags")
    ax.set_xlabel("Hashtag")
    ax.set_ylabel("Number of Posts")

    plt.xticks(rotation=45)

    st.pyplot(fig)

    st.dataframe(
        top_hashtags,
        use_container_width=True
    )

# -----------------------------
# Most Active Users
# -----------------------------
st.header("👥 Most Active Users")

active_users = (
    filtered_df["User"]
    .value_counts()
    .reset_index()
)

active_users.columns = ["User", "Posts"]

st.dataframe(
    active_users.head(10),
    use_container_width=True
)

# -----------------------------
# Engagement Analysis
# -----------------------------
st.header("💬 User Engagement")

user_engagement = (
    filtered_df
    .groupby("User")[[
        "Likes",
        "Comments",
        "Shares",
        "Engagement"
    ]]
    .sum()
    .sort_values(
        "Engagement",
        ascending=False
    )
)

st.dataframe(
    user_engagement,
    use_container_width=True
)

# -----------------------------
# Daily Engagement Trend
# -----------------------------
st.header("📈 Daily Engagement Trend")

daily_engagement = (
    filtered_df
    .groupby("Date")["Engagement"]
    .sum()
    .reset_index()
)

fig, ax = plt.subplots()

ax.plot(
    daily_engagement["Date"],
    daily_engagement["Engagement"],
    marker="o"
)

ax.set_title("Daily Engagement Trend")
ax.set_xlabel("Date")
ax.set_ylabel("Total Engagement")

plt.xticks(rotation=45)

st.pyplot(fig)

# -----------------------------
# Content Category Distribution
# -----------------------------
st.header("🥧 Content Category Distribution")

category_counts = (
    filtered_df["Category"]
    .value_counts()
)

fig, ax = plt.subplots()

ax.pie(
    category_counts.values,
    labels=category_counts.index,
    autopct="%1.1f%%"
)

ax.set_title("Content Category Distribution")

st.pyplot(fig)

# -----------------------------
# Popular Posting Time
# -----------------------------
st.header("⏰ Most Popular Posting Time")

filtered_df["Hour"] = pd.to_datetime(
    filtered_df["Time"],
    format="%H:%M",
    errors="coerce"
).dt.hour

hourly_posts = (
    filtered_df["Hour"]
    .value_counts()
    .sort_index()
)

if not hourly_posts.empty:

    popular_hour = hourly_posts.idxmax()

    st.success(
        f"Most popular posting time: "
        f"{popular_hour:02d}:00 - {popular_hour:02d}:59"
    )

    fig, ax = plt.subplots()

    ax.bar(
        hourly_posts.index,
        hourly_posts.values
    )

    ax.set_title("Posts by Hour")
    ax.set_xlabel("Hour")
    ax.set_ylabel("Number of Posts")

    st.pyplot(fig)

# -----------------------------
# Sentiment Analysis
# -----------------------------
st.header("😊 Sentiment Analysis")

sentiment_counts = (
    filtered_df["Sentiment"]
    .value_counts()
)

col1, col2, col3 = st.columns(3)

col1.metric(
    "😊 Positive",
    int(sentiment_counts.get("Positive", 0))
)

col2.metric(
    "😐 Neutral",
    int(sentiment_counts.get("Neutral", 0))
)

col3.metric(
    "😞 Negative",
    int(sentiment_counts.get("Negative", 0))
)

fig, ax = plt.subplots()

ax.pie(
    sentiment_counts.values,
    labels=sentiment_counts.index,
    autopct="%1.1f%%"
)

ax.set_title("Sentiment Distribution")

st.pyplot(fig)

# -----------------------------
# Analytics Report
# -----------------------------
st.header("📁 Export Analytics Report")

report = filtered_df[
    [
        "Post_ID",
        "User",
        "Date",
        "Time",
        "Category",
        "Likes",
        "Comments",
        "Shares",
        "Engagement",
        "Sentiment"
    ]
]

csv_data = report.to_csv(index=False)

st.download_button(
    label="⬇️ Download Analytics Report",
    data=csv_data,
    file_name="analytics_report.csv",
    mime="text/csv"
)

# -----------------------------
# Display Filtered Data
# -----------------------------
st.header("📋 Filtered Social Media Data")

st.dataframe(
    filtered_df,
    use_container_width=True
)