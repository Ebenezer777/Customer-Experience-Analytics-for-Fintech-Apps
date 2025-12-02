import os
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer

# Banks you processed
BANKS = ["cbe", "boa", "dashen"]

INPUT_TEMPLATE = "data/{bank}_reviews_preprocessed.csv"
OUTPUT_TEMPLATE = "data/{bank}_tfidf_keywords.csv"

TOP_K = 30  # number of keywords to extract


def extract_keywords_for_bank(bank):
    input_path = INPUT_TEMPLATE.format(bank=bank)
    
    if not os.path.exists(input_path):
        print(f"[SKIP] File not found for {bank}: {input_path}")
        return
    
    print(f"\nProcessing TF-IDF for: {bank.upper()}")
    
    df = pd.read_csv(input_path)

    # Use processed text; if not found, fallback to raw review
    if "processed_text" in df.columns:
        corpus = df["processed_text"].astype(str).tolist()
    else:
        corpus = df["review_text"].astype(str).tolist()

    # Build TF-IDF model (unigram + bigram)
    vectorizer = TfidfVectorizer(
        max_df=0.85,       # ignore extremely common terms
        min_df=2,          # keep terms appearing in at least 2 reviews
        ngram_range=(1, 2),  # unigrams and bigrams
        stop_words="english"
    )
    
    X = vectorizer.fit_transform(corpus)
    terms = vectorizer.get_feature_names_out()
    
    # Compute total score for each term
    scores = np.asarray(X.sum(axis=0)).ravel()
    
    # Sort and keep top K
    top_indices = scores.argsort()[::-1][:TOP_K]
    
    top_terms = [(terms[i], float(scores[i])) for i in top_indices]

    # Output CSV
    out_df = pd.DataFrame(top_terms, columns=["term", "tfidf_score"])
    out_path = OUTPUT_TEMPLATE.format(bank=bank)
    out_df.to_csv(out_path, index=False)

    print(f"Saved top {TOP_K} keywords → {out_path}")
    print("Top keywords preview:", out_df.head(10).term.tolist())


def main():
    for bank in BANKS:
        extract_keywords_for_bank(bank)

    print("\nTF-IDF keyword extraction completed.")


if __name__ == "__main__":
    main()
