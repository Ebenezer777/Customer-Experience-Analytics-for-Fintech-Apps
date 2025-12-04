# -----------------------------
# Task 4: Insights & Recommendations
# -----------------------------

import pandas as pd
from collections import Counter
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import seaborn as sns

# -----------------------------
# 1. Load sentiment CSV
# -----------------------------
csv_file = "./data/all_banks_sentiment.csv"
df = pd.read_csv(csv_file)

# -----------------------------
# 2. Define drivers, pain points, and generate recommendations
# -----------------------------
banks = df['bank'].unique()
drivers_pain_points = {}
recommendations = {}

for bank in banks:
    bank_df = df[df['bank'] == bank]
    
    # Drivers: positive reviews
    positive_texts = bank_df[bank_df['distilbert_label'] == 'positive']['review_text'].dropna().tolist()
    # Pain points: negative reviews
    negative_texts = bank_df[bank_df['distilbert_label'] == 'negative']['review_text'].dropna().tolist()
    
    # Split into words
    positive_words = [word.lower() for text in positive_texts for word in text.split()]
    negative_words = [word.lower() for text in negative_texts for word in text.split()]
    
    # Count top words
    top_drivers = [word for word, count in Counter(positive_words).most_common(50)]
    top_pain_points = [word for word, count in Counter(negative_words).most_common(50)]
    
    drivers_pain_points[bank] = {
        'drivers': top_drivers,
        'pain_points': top_pain_points
    }
    
    # Generate simple recommendations
    recs = []
    if top_drivers:
        recs.append(f"Leverage strengths like: {', '.join(top_drivers[:5])}")
    if top_pain_points:
        recs.append(f"Address key issues like: {', '.join(top_pain_points[:5])}")
    recommendations[bank] = recs

# -----------------------------
# 3. Function to generate word clouds
# -----------------------------
def generate_wordcloud(words, title):
    if len(words) == 0:
        print(f"No words to show for {title}")
        return
    text = " ".join(words)
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate(text)
    plt.figure(figsize=(10,5))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    plt.title(title, fontsize=16)
    plt.show()

# -----------------------------
# 4. Generate word clouds per bank
# -----------------------------
for bank in banks:
    info = drivers_pain_points[bank]
    generate_wordcloud(info['drivers'], f"{bank} - Drivers (Positive Reviews)")
    generate_wordcloud(info['pain_points'], f"{bank} - Pain Points (Negative Reviews)")

# -----------------------------
# 5. Sentiment distribution bar plot
# -----------------------------
plt.figure(figsize=(10,6))
sns.countplot(data=df, x='bank', hue='distilbert_label')
plt.title("Sentiment Distribution per Bank")
plt.xlabel("Bank")
plt.ylabel("Number of Reviews")
plt.legend(title='Sentiment')
plt.show()

# -----------------------------
# 6. Print top recommendations per bank
# -----------------------------
print("\n✅ Recommendations per Bank:")
for bank in banks:
    print(f"\n--- {bank} ---")
    for rec in recommendations[bank]:
        print(f"- {rec}")

print("\n✅ Task 4 complete: Drivers, Pain Points, Sentiment Distribution, and Recommendations generated!")