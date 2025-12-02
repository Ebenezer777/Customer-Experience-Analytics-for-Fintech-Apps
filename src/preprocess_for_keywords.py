import pandas as pd
import spacy
import re

# Load English tokenizer, lemmatizer, stop words
nlp = spacy.load("en_core_web_sm")

# Extra stopwords specific to our data
extra_stopwords = set(["app", "mobile", "bank"])
stopwords = nlp.Defaults.stop_words.union(extra_stopwords)

def clean_text(text):
    # Remove URLs
    text = re.sub(r"http\S+|www\S+|https\S+", "", text)
    # Remove non-alphabetic characters
    text = re.sub(r"[^a-zA-Z\s]", "", text)
    # Lowercase
    text = text.lower()
    # Tokenize and lemmatize
    doc = nlp(text)
    tokens = [token.lemma_ for token in doc if token.is_alpha and token.text not in stopwords]
    return " ".join(tokens)

def preprocess_for_keywords(input_csv, output_csv):
    df = pd.read_csv(input_csv)
    df['processed_text'] = df['review_text'].astype(str).apply(clean_text)
    df.to_csv(output_csv, index=False)
    print(f"Saved preprocessed text to {output_csv}")

if __name__ == "__main__":
    preprocess_for_keywords('data/cbe_reviews_sentiment.csv', 'data/cbe_reviews_preprocessed.csv')
    preprocess_for_keywords('data/boa_reviews_sentiment.csv', 'data/boa_reviews_preprocessed.csv')
    preprocess_for_keywords('data/dashen_reviews_sentiment.csv', 'data/dashen_reviews_preprocessed.csv')
