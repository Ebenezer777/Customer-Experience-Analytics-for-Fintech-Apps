import pandas as pd
from transformers import pipeline
import os

# List of banks
banks = ["cbe", "boa", "dashen"]

# Load DistilBERT SST-2 pipeline
classifier = pipeline("sentiment-analysis", model="distilbert-base-uncased-finetuned-sst-2-english")

# Ensure output folder exists
os.makedirs("data", exist_ok=True)

for bank in banks:
    input_csv = f"data/{bank}_reviews_cleaned.csv"
    output_csv = f"data/{bank}_reviews_distilbert.csv"

    df = pd.read_csv(input_csv)

    def get_label(text):
        # Truncate to 512 tokens to avoid errors
        result = classifier(str(text)[:512])[0]
        return result['label'].lower()  # "POSITIVE" -> "positive"

    df['distilbert_label'] = df['review_text'].apply(get_label)

    df.to_csv(output_csv, index=False)
    print(f"{bank.upper()} DistilBERT analysis done. Saved to {output_csv}")
