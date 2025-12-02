from google_play_scraper import reviews
import pandas as pd
import os

# ==========================
# Parameters (easily configurable)
# ==========================
OUTPUT_DIR = "data"
COMBINED_CSV = "all_banks_reviews.csv"
REVIEWS_PER_BANK = 450

BANK_APPS = {
    "BOA": "com.boa.boaMobileBanking",
    "CBE": "com.combanketh.mobilebanking",
    "Dashen": "com.dashen.dashensuperapp"
}

# ==========================
# Function to scrape reviews for a given app
# ==========================
def scrape_reviews(app_id, bank_name, count=REVIEWS_PER_BANK, output_dir=OUTPUT_DIR):
    try:
        print(f"\nScraping reviews for {bank_name}...")
        result, _ = reviews(app_id, count=count)
        df = pd.DataFrame(result)

        # Add explicit bank and source columns
        df["bank"] = bank_name
        df["source"] = "Google Play Store"

        # Select relevant columns and rename
        df = df[["content", "score", "at", "bank", "source"]]
        df.rename(columns={"content": "review_text", "score": "rating", "at": "review_date"}, inplace=True)

        # Basic missing/empty review checks
        missing_reviews = df['review_text'].isna().sum()
        empty_reviews = (df['review_text'].str.strip() == "").sum()
        print(f"{missing_reviews} missing and {empty_reviews} empty reviews found for {bank_name}")

        # Rating distribution & date range
        print(f"Total reviews scraped for {bank_name}: {len(df)}")
        print("Rating distribution:")
        print(df['rating'].value_counts().sort_index())
        print(f"Date range: {df['review_date'].min().date()} to {df['review_date'].max().date()}")

        # Ensure output directory exists
        os.makedirs(output_dir, exist_ok=True)

        # Save individual CSV per bank
        csv_path = os.path.join(output_dir, f"{bank_name.lower()}_reviews.csv")
        df.to_csv(csv_path, index=False)
        print(f"Saved {len(df)} reviews to {csv_path}")

        return df

    except Exception as e:
        print(f"Error scraping {bank_name}: {e}")
        return pd.DataFrame()  # Return empty DataFrame on failure

# ==========================
# Scrape reviews for all banks
# ==========================
all_dfs = []
for bank_name, app_id in BANK_APPS.items():
    df = scrape_reviews(app_id, bank_name)
    all_dfs.append(df)

# ==========================
# Combine all dataframes and remove duplicates
# ==========================
combined_df = pd.concat(all_dfs, ignore_index=True)
duplicates = combined_df.duplicated(subset=['review_text', 'bank'])
print(f"\nFound {duplicates.sum()} duplicate reviews across banks")
combined_df = combined_df.drop_duplicates(subset=['review_text', 'bank'])

# ==========================
# Combined data quality report
# ==========================
print("\n=== Combined Data Quality Report ===")
print(f"Total combined reviews: {len(combined_df)}")
print("Missing review_text entries:", combined_df['review_text'].isna().sum())
print("Empty review_text entries:", (combined_df['review_text'].str.strip() == "").sum())
print("Review counts per bank:")
print(combined_df['bank'].value_counts())
print("Rating distribution across all banks:")
print(combined_df['rating'].value_counts().sort_index())

# ==========================
# Save combined CSV
# ==========================
combined_csv_path = os.path.join(OUTPUT_DIR, COMBINED_CSV)
combined_df.to_csv(combined_csv_path, index=False)
print(f"\nSaved consolidated CSV with {len(combined_df)} reviews to {combined_csv_path}")
