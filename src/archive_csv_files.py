import os
import shutil

archive_dir = "data/archive"
os.makedirs(archive_dir, exist_ok=True)

# List of intermediate CSVs to archive
intermediate_files = [
    "boa_reviews.csv", "cbe_reviews.csv", "dashen_reviews.csv",
    "boa_reviews_clean.csv", "cbe_reviews_clean.csv", "dashen_reviews_clean.csv",
    "boa_reviews_sentiment.csv", "cbe_reviews_sentiment.csv", "dashen_reviews_sentiment.csv",
    "preprocess_for_keywords.csv"
]

for f in intermediate_files:
    path = os.path.join("data", f)
    if os.path.exists(path):
        shutil.move(path, archive_dir)
        print(f"Moved {f} to archive/")
