import pandas as pd
from transformers import pipeline
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import argparse
import os
import nltk

nltk.download('vader_lexicon')

def sentiment_vader(text, analyzer):
    try:
        score = analyzer.polarity_scores(text)['compound']
        if score >= 0.05:
            label = "positive"
        elif score <= -0.05:
            label = "negative"
        else:
            label = "neutral"
        return label, score
    except:
        return "neutral", 0.0

def sentiment_distilbert(text, classifier):
    try:
        result = classifier(text[:512])[0]  # truncate if too long
        return result['label'].lower(), result['score']
    except:
        return "neutral", 0.0

def main(input_csv, output_csv):
    df = pd.read_csv(input_csv)
    print(f"Loaded {len(df)} reviews from {input_csv}")

    # VADER
    vader_analyzer = SentimentIntensityAnalyzer()
    df[['vader_label', 'vader_score']] = df['clean_text'].apply(lambda x: pd.Series(sentiment_vader(x, vader_analyzer)))

    # DistilBERT
    classifier = pipeline("sentiment-analysis", model="distilbert-base-uncased-finetuned-sst-2-english")
    df[['distilbert_label', 'distilbert_score']] = df['clean_text'].apply(lambda x: pd.Series(sentiment_distilbert(x, classifier)))

    os.makedirs(os.path.dirname(output_csv), exist_ok=True)
    df.to_csv(output_csv, index=False)
    print(f"Saved sentiment-labeled reviews to {output_csv}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Compute sentiment using VADER and DistilBERT")
    parser.add_argument("--input", type=str, required=True, help="Input CSV file path")
    parser.add_argument("--output", type=str, required=True, help="Output CSV file path")
    args = parser.parse_args()
    main(args.input, args.output)
