import pandas as pd

# Load CSV
df = pd.read_csv("data/all_banks_sentiment.csv", encoding='utf-8')

# Strip any whitespace from column names
df.columns = df.columns.str.strip().str.replace('\ufeff','')

# Prepare summary table without themes
summary_list = []

for bank in df['bank'].unique():
    bank_df = df[df['bank'] == bank]
    
    total_reviews = len(bank_df)
    positive = len(bank_df[bank_df['distilbert_label'] == 'positive'])
    neutral = len(bank_df[bank_df['distilbert_label'] == 'neutral'])
    negative = len(bank_df[bank_df['distilbert_label'] == 'negative'])
    
    summary_list.append({
        'Bank': bank,
        'Total Reviews': total_reviews,
        'Positive': positive,
        'Neutral': neutral,
        'Negative': negative,
    })

summary_df = pd.DataFrame(summary_list)
print(summary_df)
summary_df.to_csv("data/bank_summary_table_no_themes.csv", index=False)
