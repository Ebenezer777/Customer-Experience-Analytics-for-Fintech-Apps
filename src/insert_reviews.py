import psycopg2
import pandas as pd

# -----------------------------
# 1. Load the cleaned CSV
# -----------------------------
csv_file = "./data/all_banks_reviews.csv"
df = pd.read_csv(csv_file)

# -----------------------------
# 2. Connect to PostgreSQL
# -----------------------------
conn = psycopg2.connect(
    host="localhost",
    database="bank_reviews",
    user="postgres",
    password="G/JxAgnei*3754*"
)
cur = conn.cursor()

# -----------------------------
# 3. Insert unique banks first
# -----------------------------
banks = df[['bank']].drop_duplicates()

for _, row in banks.iterrows():
    cur.execute("""
        INSERT INTO banks (bank_name, app_name)
        VALUES (%s, %s)
        ON CONFLICT (bank_name) DO NOTHING
    """, (row['bank'], row['bank']))  # using bank name as app_name

conn.commit()

# -----------------------------
# 4. Fetch bank_ids to map reviews
# -----------------------------
cur.execute("SELECT bank_id, bank_name FROM banks")
bank_map = {name: id for id, name in cur.fetchall()}

# -----------------------------
# 5. Insert reviews
# -----------------------------
for _, row in df.iterrows():
    bank_id = bank_map[row['bank']]
    cur.execute("""
        INSERT INTO reviews (bank_id, review_text, rating, review_date, sentiment_label, sentiment_score, source)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """, (
        bank_id,
        row['review_text'],
        row['rating'],
        row['review_date'].split(" ")[0],  # keep only YYYY-MM-DD
        row.get('sentiment_label', None),
        row.get('sentiment_score', None),
        row['source']
    ))

conn.commit()

# -----------------------------
# 6. Close connection
# -----------------------------
cur.close()
conn.close()

print("✅ All reviews inserted successfully!")
