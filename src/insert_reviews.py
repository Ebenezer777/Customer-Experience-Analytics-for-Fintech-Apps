# File: src/insert_reviews_task3.py

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
try:
    conn = psycopg2.connect(
        host="localhost",
        database="bank_reviews",
        user="postgres",
        password="G/JxAgnei*3754*"
    )
    cur = conn.cursor()
    print("✅ Connected to PostgreSQL successfully.")
except Exception as e:
    print("❌ Error connecting to PostgreSQL:", e)
    exit()

# -----------------------------
# 3. Create tables if they don't exist
# -----------------------------
try:
    cur.execute("""
        CREATE TABLE IF NOT EXISTS banks (
            bank_id SERIAL PRIMARY KEY,
            bank_name TEXT UNIQUE NOT NULL,
            app_name TEXT NOT NULL
        );
    """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS reviews (
            review_id SERIAL PRIMARY KEY,
            bank_id INTEGER REFERENCES banks(bank_id),
            review_text TEXT,
            rating INTEGER,
            review_date DATE,
            sentiment_label TEXT,
            sentiment_score FLOAT,
            source TEXT
        );
    """)
    conn.commit()
    print("✅ Tables created successfully.")
except Exception as e:
    print("❌ Error creating tables:", e)
    conn.rollback()
    exit()

# -----------------------------
# 4. Insert unique banks
# -----------------------------
try:
    banks = df[['bank']].drop_duplicates()
    for _, row in banks.iterrows():
        cur.execute("""
            INSERT INTO banks (bank_name, app_name)
            VALUES (%s, %s)
            ON CONFLICT (bank_name) DO NOTHING;
        """, (row['bank'], row['bank']))  # using bank name as app_name
    conn.commit()
    print("✅ Banks inserted successfully.")
except Exception as e:
    print("❌ Error inserting banks:", e)
    conn.rollback()

# -----------------------------
# 5. Fetch bank_ids for mapping reviews
# -----------------------------
cur.execute("SELECT bank_id, bank_name FROM banks;")
bank_map = {name: id for id, name in cur.fetchall()}

# -----------------------------
# 6. Insert reviews
# -----------------------------
try:
    for _, row in df.iterrows():
        bank_id = bank_map.get(row['bank'])
        if bank_id is None:
            continue  # skip if bank not found
        cur.execute("""
            INSERT INTO reviews 
            (bank_id, review_text, rating, review_date, sentiment_label, sentiment_score, source)
            VALUES (%s, %s, %s, %s, %s, %s, %s);
        """, (
            bank_id,
            row['review_text'],
            row['rating'],
            row['review_date'].split(" ")[0],  # only YYYY-MM-DD
            row.get('sentiment_label', None),
            row.get('sentiment_score', None),
            row['source']
        ))
    conn.commit()
    print("✅ Reviews inserted successfully.")
except Exception as e:
    print("❌ Error inserting reviews:", e)
    conn.rollback()

# -----------------------------
# 7. Data verification
# -----------------------------
try:
    print("\n--- Data Verification ---")
    cur.execute("SELECT bank_name, COUNT(*) FROM reviews r JOIN banks b ON r.bank_id = b.bank_id GROUP BY bank_name;")
    print("Reviews count per bank:", cur.fetchall())

    cur.execute("SELECT bank_name, AVG(rating) FROM reviews r JOIN banks b ON r.bank_id = b.bank_id GROUP BY bank_name;")
    print("Average rating per bank:", cur.fetchall())

    cur.execute("SELECT COUNT(*) FROM reviews WHERE review_text IS NULL;")
    print("Null review_text count:", cur.fetchone()[0])
except Exception as e:
    print("❌ Error verifying data:", e)

# -----------------------------
# 8. Close connection
# -----------------------------
cur.close()
conn.close()
print("✅ PostgreSQL connection closed.")
