import pandas as pd

def preprocess_reviews(csv_path, cleaned_csv_path):
    # Load CSV
    df = pd.read_csv(csv_path)

    print(f"Original reviews: {len(df)}")

    # Drop duplicates
    df.drop_duplicates(subset='review_text', inplace=True)

    # Drop missing or empty reviews
    df.dropna(subset=['review_text'], inplace=True)
    df = df[df['review_text'].str.strip() != '']

    # Normalize dates
    df['review_date'] = pd.to_datetime(df['review_date']).dt.strftime('%Y-%m-%d')

    # Optional: lowercase text
    df['review_text'] = df['review_text'].str.lower()

    # Save cleaned CSV
    df.to_csv(cleaned_csv_path, index=False)
    print(f"Cleaned reviews: {len(df)}")
    print(f"Saved cleaned CSV to {cleaned_csv_path}")

if __name__ == "__main__":
    preprocess_reviews('data/cbe_reviews.csv', 'data/cbe_reviews_cleaned.csv')
    preprocess_reviews('data/boa_reviews.csv', 'data/boa_reviews_cleaned.csv')
    preprocess_reviews('data/dashen_reviews.csv', 'data/dashen_reviews_cleaned.csv')