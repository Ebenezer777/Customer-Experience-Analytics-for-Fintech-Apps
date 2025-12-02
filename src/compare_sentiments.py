import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# List of banks
banks = ["cbe", "boa", "dashen"]

# Ensure output folder exists
os.makedirs("data/plots", exist_ok=True)

for bank in banks:
    # Load CSVs
    vader_csv = f"data/{bank}_reviews_sentiment.csv"
    bert_csv = f"data/{bank}_reviews_distilbert.csv"

    vader = pd.read_csv(vader_csv)
    bert = pd.read_csv(bert_csv)

    # Merge on review text
    merged = vader.merge(bert[['review_text','distilbert_label']], on='review_text')
    merged['agree'] = merged['sentiment_label'] == merged['distilbert_label']

    # Numerical comparison
    agreement_pct = merged['agree'].mean()*100
    print(f"\nBank: {bank.upper()}")
    print(f"Agreement %: {agreement_pct:.2f}%")
    print("VADER distribution:")
    print(merged['sentiment_label'].value_counts(normalize=True)*100)
    print("DistilBERT distribution:")
    print(merged['distilbert_label'].value_counts(normalize=True)*100)

    # Save merged CSV
    merged.to_csv(f"data/{bank}_reviews_comparison.csv", index=False)

    # Visualization 1: Bar chart of sentiment distribution
    plt.figure(figsize=(8,5))
    sns.countplot(x='sentiment_label', data=merged, color='blue', label='VADER')
    sns.countplot(x='distilbert_label', data=merged, color='orange', alpha=0.5, label='DistilBERT')
    plt.title(f"Sentiment Distribution: {bank.upper()} (VADER vs DistilBERT)")
    plt.legend()
    plt.savefig(f"data/plots/{bank}_sentiment_distribution.png")
    plt.close()

    # Visualization 2: Agreement pie chart
    agree_counts = merged['agree'].value_counts()
    plt.figure(figsize=(5,5))
    plt.pie(agree_counts, labels=['Agree','Disagree'], autopct='%1.1f%%', colors=['green','red'])
    plt.title(f"Agreement Between VADER and DistilBERT: {bank.upper()}")
    plt.savefig(f"data/plots/{bank}_agreement_pie.png")
    plt.close()

print("\nAll comparisons completed. Plots saved in data/plots/")
