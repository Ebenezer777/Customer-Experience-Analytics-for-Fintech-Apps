import os
import time
import pandas as pd
from google_play_scraper import reviews, Sort

def scrape_and_save(app_id, bank_name, num_reviews=450):
    print(f"Scraping {num_reviews} reviews for {bank_name}...")
    
    # Fetch reviews
    result, _ = reviews(
        app_id,
        count=num_reviews,
        lang='en',
        sort=Sort.NEWEST
    )
    
    # Print first 5 reviews as a sanity check
    print(f"First 5 reviews for {bank_name}:")
    for i, review in enumerate(result[:5], start=1):
        print(f"Review {i}: Rating={review['score']}, Text={review['content']}")
    print("-" * 40)
    
    # Ensure data folder exists
    os.makedirs('data', exist_ok=True)
    
    # Convert to DataFrame
    df = pd.DataFrame(result)
    df = df[['content', 'score', 'at']]
    df.rename(columns={'content': 'review_text', 'score': 'rating', 'at': 'review_date'}, inplace=True)
    
    # Save CSV
    csv_path = f"data/{bank_name}_reviews.csv"
    df.to_csv(csv_path, index=False)
    print(f"Saved {len(df)} reviews to {csv_path}\n")
    
    # Optional: small delay between banks
    time.sleep(5)

if __name__ == "__main__":
    scrape_and_save("com.combanketh.mobilebanking", "cbe", num_reviews=450)
    scrape_and_save("com.boa.boaMobileBanking", "boa", num_reviews=450)
    scrape_and_save("com.dashen.dashensuperapp", "dashen", num_reviews=450)
