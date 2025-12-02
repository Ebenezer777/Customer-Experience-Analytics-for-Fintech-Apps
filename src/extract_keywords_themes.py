import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
import argparse
import os

def extract_keywords(df, text_col='review_text', top_n=30):
    # Remove missing or empty review texts
    df = df.dropna(subset=[text_col])
    df = df[df[text_col].str.strip() != ""]

    vectorizer = TfidfVectorizer(
        max_features=top_n,
        ngram_range=(1, 2),  # unigrams and bigrams
        stop_words='english'
    )
    X = vectorizer.fit_transform(df[text_col])
    feature_names = vectorizer.get_feature_names_out()
    scores = X.sum(axis=0).A1
    tfidf_df = pd.DataFrame({'term': feature_names, 'tfidf_score': scores})
    tfidf_df = tfidf_df.sort_values(by='tfidf_score', ascending=False)
    return tfidf_df

def generate_themes(tfidf_df, df):
    # Simple example: assign theme based on keyword groups (customize as needed)
    theme_mapping = {
        'app_performance': ['work', 'crash', 'slow', 'fix', 'update', 'time', 'application', 'open'],
        'transaction': ['transfer', 'money', 'banking', 'transaction', 'account'],
        'ux_ui': ['easy', 'nice', 'use', 'experience', 'app', 'user', 'feature'],
        'sentiment': ['good', 'great', 'amazing', 'love', 'thank', 'bad'],
        'brand': ['dashen', 'super', 'wow']
    }

    # Assign themes for each review based on keywords it contains
    def assign_theme(text):
        text_lower = str(text).lower()
        themes = []
        for theme, keywords in theme_mapping.items():
            if any(k in text_lower for k in keywords):
                themes.append(theme)
        return ', '.join(themes) if themes else 'other'

    df['identified_themes'] = df['review_text'].apply(assign_theme)
    return df

def main(input_csv, output_keywords_csv, output_themes_csv):
    df = pd.read_csv(input_csv)
    print(f"Loaded {len(df)} reviews from {input_csv}")

    # Extract TF-IDF keywords
    tfidf_df = extract_keywords(df)
    os.makedirs(os.path.dirname(output_keywords_csv), exist_ok=True)
    tfidf_df.to_csv(output_keywords_csv, index=False)
    print(f"Saved top keywords to {output_keywords_csv}")

    # Generate themes for each review
    df_with_themes = generate_themes(tfidf_df, df)
    os.makedirs(os.path.dirname(output_themes_csv), exist_ok=True)
    df_with_themes.to_csv(output_themes_csv, index=False)
    print(f"Saved review themes to {output_themes_csv}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Extract keywords and assign themes")
    parser.add_argument("--input", type=str, required=True, help="Input CSV file path")
    parser.add_argument("--output_keywords", type=str, required=True, help="Output CSV file for TF-IDF keywords")
    parser.add_argument("--output_themes", type=str, required=True, help="Output CSV file for review themes")
    args = parser.parse_args()

    main(args.input, args.output_keywords, args.output_themes)
