import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
data = {
    "Movie Name": [
        "Inception", "Avengers Endgame", "Titanic",
        "Joker", "Interstellar", "Avatar",
        "The Batman", "Frozen", "Top Gun Maverick",
        "Oppenheimer"
    ],
    
    "Rating": [8.8, 8.4, 7.9, 8.5, 8.7, 7.8, 7.9, 7.5, 8.3, 8.6],
    
    "Genre": [
        "Sci-Fi", "Action", "Romance",
        "Drama", "Sci-Fi", "Sci-Fi",
        "Action", "Animation", "Action",
        "Biography"
    ],
    
    "Revenue": [
        829, 2798, 2187,
        1074, 701, 2923,
        770, 1450, 1495,
        975
    ]
}

df = pd.DataFrame(data)

print(df)
highest_rated = df.sort_values(by="Rating", ascending=False)

print("Highest Rated Movies:")
print(highest_rated[["Movie Name", "Rating"]])
genre_profit = df.groupby("Genre")["Revenue"].sum().sort_values(ascending=False)

print("\nMost Profitable Genres:")
print(genre_profit)
plt.figure(figsize=(8,5))

sns.barplot(
    x=genre_profit.index,
    y=genre_profit.values
)

plt.title("Genre vs Revenue")
plt.xlabel("Genre")
plt.ylabel("Total Revenue (Millions)")
plt.xticks(rotation=45)

plt.show()
plt.figure(figsize=(7,5))

sns.histplot(df["Rating"], bins=5, kde=True)

plt.title("Rating Distribution")
plt.xlabel("Ratings")
plt.ylabel("Frequency")

plt.show()
correlation = df["Rating"].corr(df["Revenue"])

print("\nCorrelation Between Rating and Revenue:")
print(correlation)
top5 = df.sort_values(by="Revenue", ascending=False).head(5)

print("\nTop 5 Movies by Revenue:")
print(top5[["Movie Name", "Revenue"]])
plt.figure(figsize=(7,5))

sns.scatterplot(
    x="Rating",
    y="Revenue",
    hue="Genre",
    s=150,
    data=df
)

plt.title("Rating vs Revenue")
plt.xlabel("Rating")
plt.ylabel("Revenue")

plt.show()
