"""
assign_themes.py

Reads each bank's cleaned/sentiment CSV, assigns one or more themes to each review
based on keyword matching (uses processed_text if available, else review_text),
and writes out data/{bank}_reviews_with_themes.csv.

Run from project root:
    python src\assign_themes.py
"""

import os
import re
import json
import pandas as pd

# --- Config: banks and input/output file templates ---
BANKS = ["cbe", "boa", "dashen"]
INPUT_TEMPLATE_CLEANED = "data/{bank}_reviews_cleaned.csv"      # prefer cleaned file
INPUT_TEMPLATE_SENTIMENT = "data/{bank}_reviews_sentiment.csv"  # fallback (has sentiment columns)
OUTPUT_TEMPLATE = "data/{bank}_reviews_with_themes.csv"

os.makedirs("data", exist_ok=True)

# --- Theme definitions (universal 5 themes) ---
THEME_KEYWORDS = {
    "App Performance & Reliability": [
        "slow", "lag", "freeze", "crash", "loading", "delay", "timeout",
        "stuck", "not responding", "bug", "error", "failed", "fail", "down", "open problem", "not open"
    ],
    "Transactions & Banking Operations": [
        "transfer", "transaction", "send", "deposit", "withdraw", "payment",
        "balance", "fund", "transfer failed", "transfer slow", "money"
    ],
    "User Experience (UX/UI)": [
        "easy to use", "easy", "use", "ui", "interface", "navigation", "design",
        "layout", "confusing", "user friendly", "user-friendly", "nice", "simple"
    ],
    "Sentiment": [
        "good", "great", "amazing", "excellent", "love", "happy",
        "bad", "terrible", "awful", "hate", "worst", "disappoint"
    ],
    "Bank-Specific Identity & Brand": [
        "dashen", "dashen super", "cbe", "commercial bank", "bank of abyssinia", "boa", "ethiopia"
    ]
}

# Compile regex patterns for each theme for efficient matching
THEME_PATTERNS = {}
for theme, kws in THEME_KEYWORDS.items():
    # sort keywords by length desc so multi-word phrases match first (e.g., "dashen super")
    kws_sorted = sorted(set(kws), key=lambda x: -len(x))
    # escape and join using alternation; use word-boundary for single words, allow phrases
    parts = []
    for kw in kws_sorted:
        if " " in kw:
            parts.append(re.escape(kw))
        else:
            parts.append(r"\b" + re.escape(kw) + r"\b")
    pattern = re.compile("|".join(parts), flags=re.IGNORECASE)
    THEME_PATTERNS[theme] = pattern

def choose_text_column(df):
    """Return name of column to use for matching: prefer 'processed_text', then 'clean_text', then 'review_text'."""
    for c in ("processed_text", "clean_text", "review_text", "review"):
        if c in df.columns:
            return c
    raise ValueError("No usable text column found (expected one of processed_text/clean_text/review_text).")

def assign_themes_to_text(text):
    """Return a list of matched themes for the given text (may be empty)."""
    if not isinstance(text, str) or text.strip() == "":
        return []
    matched = []
    t = text.lower()
    for theme, pat in THEME_PATTERNS.items():
        if pat.search(t):
            matched.append(theme)
    return matched

def process_bank(bank):
    # pick input file: prefer cleaned CSV, else sentiment CSV
    cleaned_path = INPUT_TEMPLATE_CLEANED.format(bank=bank)
    sentiment_path = INPUT_TEMPLATE_SENTIMENT.format(bank=bank)

    if os.path.exists(cleaned_path):
        input_path = cleaned_path
    elif os.path.exists(sentiment_path):
        input_path = sentiment_path
    else:
        print(f"[SKIP] No input CSV found for {bank}. Checked:\n  {cleaned_path}\n  {sentiment_path}")
        return

    print(f"\nProcessing {bank} -> {input_path}")
    df = pd.read_csv(input_path)

    # Ensure there's an ID column; if not, create one from index
    if "review_id" not in df.columns:
        df.insert(0, "review_id", df.index.astype(str))

    text_col = choose_text_column(df)
    print(f" Using text column: {text_col} (rows={len(df)})")

    # Assign themes
    df["identified_themes"] = df[text_col].astype(str).apply(assign_themes_to_text)

    # If no theme matched, keep assigned_themes as empty list (we'll fill fallback later)
    # Also create a human-friendly string column
    df["identified_themes_str"] = df["identified_themes"].apply(lambda lst: "|".join(lst) if isinstance(lst, (list, tuple)) and lst else "")

    # Save result
    out_path = OUTPUT_TEMPLATE.format(bank=bank)
    # Keep commonly useful columns but write everything by default
    df.to_csv(out_path, index=False)
    print(f" Saved themed CSV → {out_path}")
    # Print KPI summary
    total = len(df)
    with_theme = df["identified_themes"].apply(bool).sum()
    print(f" Themes assigned to {with_theme}/{total} reviews ({with_theme/total*100:.1f}%)")

def main():
    for bank in BANKS:
        process_bank(bank)
    print("\nDone. Inspect the generated CSVs in the data/ folder.")

if __name__ == "__main__":
    main()
