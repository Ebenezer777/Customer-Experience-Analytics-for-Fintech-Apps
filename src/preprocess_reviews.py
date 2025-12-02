# src/preprocess_reviews.py

import pandas as pd
import re
import spacy
import argparse
import os

nlp = spacy.load("en_core_web_sm", disable=["parser", "ner"])

def preprocess_text(text):
    text = str(text).lower()
    text = re.sub(r"http\S+|www\S+|https\S+", "", text)  # remove urls
    text = re.sub(r"[^a-z\s]", "", text)  # remove non-alphabetic
    tokens = [token.lemma_ for token in nlp(text) if not token.is_stop]
    return " ".join(tokens)

def main(input_csv, output_csv):
    df = pd.read_csv(input_csv)
    print(f"Loaded {len(df)} reviews from {input_csv}")

    df['clean_text'] = df['review_text'].apply(preprocess_text)

    # Basic check for empty reviews
    empty_count = df['clean_text'].isna().sum() + (df['clean_text'] == "").sum()
    print(f"Found {empty_count} empty reviews after preprocessing")

    os.makedirs(os.path.dirname(output_csv), exist_ok=True)
    df.to_csv(output_csv, index=False)
    print(f"Saved preprocessed reviews to {output_csv}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Preprocess reviews for NLP")
    parser.add_argument("--input", type=str, required=True, help="Input CSV file path")
    parser.add_argument("--output", type=str, required=True, help="Output CSV file path")
    args = parser.parse_args()
    main(args.input, args.output)