import pandas as pd
from datetime import datetime

df = pd.read_csv("netflix.csv")

print("\n===== 5 premières lignes =====")
print(df.head())
print("\n===== Dimensions =====")
print(df.shape)
print("\n===== Types de colonnes =====")
print(df.dtypes)
print("\n===== Valeurs manquantes =====")
print(df.isnull().sum())

#supprimmer les lignes vides
df= df.dropna(how="all")

df["director"] = df["director"].fillna("Unknown")
df["cast"] = df["cast"].fillna("Not specified")
df["country"] = df["country"].fillna("Unknown")

#supprimer les doublons
df = df.drop_duplicates()

#mettre les colones en majiscule
df["type"] = df["type"].str.upper()

for col in df.select_dtypes(include=["object", "string"]):
    df[col] = df[col].str.strip() 

print("\n===================================")
print("FEATURE ENGINEERING")
print("===================================")

current_year = datetime.now().year

df["release_year"] = current_year  - df["release_year"]

df["is_recent"] = (df["release_year"] >= 2018).astype(int)

def categorize_length(row):
    if row["type"] == "Movie":
        try:
            minutes = int(row["duration"].split()[0])
        except:
            return "Unknown"
    else:
        try:
            minutes = int(row["duration"].split()[0])
        except:
            return "Unknown"
    if minutes < 60:
        return "Short"
    elif minutes <= 120:
        return "Medium"
    else:
        return "Long"


df["content_length_category"] = df.apply(categorize_length, axis=1)            
print(df.head())

print("\n===================================")
print("ANALYSE METIER")
print("===================================")

num_movies = (df["type"] == "MOVIE").sum()
num_series = (df["type"] == "TV SHOW").sum()

print("Nombre de films :", num_movies)
print("Nombre de séries :", num_series)

print(df["country"].value_counts().head())

print(df["release_year"].value_counts().sort_index())

#durée moyenne du filme
movies_df = df[df["type"] == "MOVIE"].copy()
movies_df["duration_min"] = movies_df["duration"].str.extract("(\d+)").astype(float)

print("\nDurée moyenne des films :")
print(movies_df["duration_min"].mean())

recent_percent = df['is_recent'].mean() * 100
print(f"\nPourcentage de contenus récents : {recent_percent:.2f}%")