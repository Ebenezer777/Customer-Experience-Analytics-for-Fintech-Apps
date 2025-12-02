# I chose VADER for sentiment analysis due to its effectiveness on social media texts and short reviews.

import pandas as pd
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

analyzer = SentimentIntensityAnalyzer()

def get_sentiment_label(text):
    score = analyzer.polarity_scores(text)['compound']
    if score >= 0.05:
        return 'positive'
    elif score <= -0.05:
        return 'negative'
    else:
        return 'neutral'

def analyze_sentiment(input_csv, output_csv):
    # Load cleaned CSV
    df = pd.read_csv(input_csv)
    
    # Apply sentiment label
    df['sentiment_label'] = df['review_text'].apply(get_sentiment_label)
    
    # Also save compound score
    df['sentiment_score'] = df['review_text'].apply(lambda x: analyzer.polarity_scores(x)['compound'])
    
    # Save new CSV
    df.to_csv(output_csv, index=False)
    print(f"Saved sentiment results to {output_csv}")

if __name__ == "__main__":
    analyze_sentiment('data/cbe_reviews_cleaned.csv', 'data/cbe_reviews_sentiment.csv')
    analyze_sentiment('data/boa_reviews_cleaned.csv', 'data/boa_reviews_sentiment.csv')
    analyze_sentiment('data/dashen_reviews_cleaned.csv', 'data/dashen_reviews_sentiment.csv')
