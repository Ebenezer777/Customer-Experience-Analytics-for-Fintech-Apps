# ================================
# Task 4: Insights and Visualizations
# ================================

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# -------------------------------
# 1. Load CSVs
# -------------------------------
sentiment_file = "./data/all_banks_sentiment.csv"
themes_file = "./data/all_banks_themes.csv"

df_sentiment = pd.read_csv(sentiment_file)
df_themes = pd.read_csv(themes_file)

# Merge on review_text + bank
df = pd.merge(
    df_sentiment,
    df_themes[['review_text', 'bank', 'identified_themes']],
    on=['review_text', 'bank'],
    how='left'
)

# Fill missing themes
df['identified_themes'] = df['identified_themes'].fillna("other")

# -------------------------------
# 2. Sanity check
# -------------------------------
print("Columns:", df.columns.tolist())
print("Top themes overall:")
print(df['identified_themes'].value_counts().head(10))
print("\nSentiment distribution:")
print(df['distilbert_label'].value_counts())

# -------------------------------
# 3. Aggregate insights per bank
# -------------------------------
# Top 5 themes per bank
top_themes = df.groupby('bank')['identified_themes'].value_counts().groupby(level=0).head(5)
print("\nTop 5 themes per bank:")
print(top_themes)

# Average sentiment score per bank
avg_sentiment = df.groupby('bank')['distilbert_score'].mean()
print("\nAverage DistilBERT sentiment score per bank:")
print(avg_sentiment)

# -------------------------------
# 4. Visualizations
# -------------------------------
sns.set(style="whitegrid")

# Sentiment distribution per bank
plt.figure(figsize=(8,5))
sns.countplot(data=df, x='bank', hue='distilbert_label')
plt.title("Sentiment Distribution per Bank (DistilBERT)")
plt.xlabel("Bank")
plt.ylabel("Number of Reviews")
plt.legend(title="Sentiment")
plt.tight_layout()
plt.show()

# Top themes per bank (barplots)
for bank in df['bank'].unique():
    plt.figure(figsize=(8,5))
    top_bank_themes = df[df['bank']==bank]['identified_themes'].value_counts().head(5)
    sns.barplot(x=top_bank_themes.values, y=top_bank_themes.index)
    plt.title(f"Top Themes for {bank}")
    plt.xlabel("Number of Reviews")
    plt.ylabel("Theme")
    plt.tight_layout()
    plt.show()

# Rating distribution per bank
plt.figure(figsize=(8,5))
sns.boxplot(data=df, x='bank', y='rating')
plt.title("Rating Distribution per Bank")
plt.xlabel("Bank")
plt.ylabel("Rating")
plt.tight_layout()
plt.show()

# -------------------------------
# 5. Extract drivers & pain points
# -------------------------------
print("\n--- Insights per bank ---\n")
for bank in df['bank'].unique():
    bank_df = df[df['bank']==bank]
    
    # Drivers: most frequent positive sentiment themes
    positive_themes = bank_df[bank_df['distilbert_label']=='positive']['identified_themes'].value_counts()
    drivers = positive_themes.head(2).index.tolist()
    
    # Pain points: most frequent negative sentiment themes
    negative_themes = bank_df[bank_df['distilbert_label']=='negative']['identified_themes'].value_counts()
    pain_points = negative_themes.head(2).index.tolist()
    
    print(f"{bank}:")
    print(f"  Drivers: {drivers if drivers else 'N/A'}")
    print(f"  Pain points: {pain_points if pain_points else 'N/A'}")
    print(f"  Avg Rating: {bank_df['rating'].mean():.2f}")
    print(f"  Total Reviews: {len(bank_df)}\n")

# -------------------------------
# 6. Recommendations (example)
# -------------------------------
print("--- Example Recommendations ---\n")
print("BOA: Improve app performance and UX/UI design, focus on transaction speed and stability.")
print("CBE: Maintain smooth navigation, address app crashes, optimize login & transfer features.")
print("Dashen: Enhance positive UX/UI elements, fix performance issues, ensure stability during peak hours.")
