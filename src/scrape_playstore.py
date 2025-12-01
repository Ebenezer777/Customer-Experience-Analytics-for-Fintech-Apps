from google_play_scraper import reviews, Sort
import pandas as pd

if __name__ == "__main__":
    app_id = "com.combanketh.mobilebanking"
    
    # Fetch 10 reviews
    result, _ = reviews(
        app_id,
        count=10,
        lang='en',
        sort=Sort.NEWEST
    )

    # -------------------------
    # 1. Print reviews to check
    # -------------------------
    for i, review in enumerate(result, start=1):
        print(f"Review {i}:")
        print(f"Rating: {review['score']}")
        print(f"Text: {review['content']}")
        print("-" * 40)

    # -------------------------
    # 2. Save to CSV
    # -------------------------
    df = pd.DataFrame(result)
    df = df[['content', 'score', 'at']]
    df.rename(columns={'content': 'review_text', 'score': 'rating', 'at': 'review_date'}, inplace=True)
    df.to_csv('./data/cbe_reviews.csv', index=False)
    print("Saved 10 reviews to data/cbe_reviews.csv")
