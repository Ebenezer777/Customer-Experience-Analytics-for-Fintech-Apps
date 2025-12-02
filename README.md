📱 Ethiopian Banking App Review Analysis
Sentiment Analysis • TF-IDF • Theme Extraction • Insights for Digital Banking

This project analyzes Google Play Store reviews for three major Ethiopian banking applications:

Bank of Abyssinia (BOA)

Commercial Bank of Ethiopia (CBE)

Dashen Bank

The goal is to understand customer perceptions, identify pain points, and extract feature-level insights that can guide product improvement and competitive strategy for digital banking platforms.

🔍 Project Overview

The analysis pipeline includes:

1. Data Collection & Cleaning

Raw Google Play Store reviews were gathered for each bank.
The preprocessing pipeline:

removes noise (punctuation, emojis, repeated characters)

standardizes text (lowercasing, tokenizing)

lemmatizes words for consistency

filters irrelevant reviews and short texts

This creates clean datasets for downstream NLP tasks.

2. Sentiment Analysis (VADER + DistilBERT)

Two sentiment models are used:

VADER → fast, rule-based sentiment scoring

DistilBERT → transformer-based deep learning model for better context understanding

This gives a richer sentiment profile for each bank and enables comparison between classical and modern NLP techniques.

3. TF-IDF Keyword Extraction

Using TF-IDF, the most meaningful keywords for each bank are extracted.
These represent the most common topics and concerns raised by real users in their reviews.

Each bank receives its own keyword set, capturing what makes its users happiest — or most frustrated.

4. Theme Assignments

Keywords are grouped into high-level themes such as:

App performance & reliability

Transaction & banking functionality

User experience (UX/UI)

Brand identity & promoter language

Overall sentiment

Each theme is described, along with the reasoning behind the grouping and what it tells us about customer priorities.

5. Insight Report & Recommendations

A full written report summarizes:

what users like

what frustrates them

how each bank can improve

where each bank has a competitive advantage

The results provide actionable, data-driven recommendations for improving digital banking in Ethiopia.

🏗 Tech Stack

Python 3.10+

NLTK, Scikit-Learn, Pandas, NumPy

HuggingFace Transformers (DistilBERT)

Matplotlib/Seaborn (optional for visualization)

Jupyter / VS Code workspace

📁 Project Structure
project/
 ├── data/                 # cleaned CSV datasets
 ├── src/                  # preprocessing, sentiment, TF-IDF scripts
 ├── reports/              # final markdown reports
 ├── requirements.txt      # dependencies
 └── README.md             # project overview

🎯 Purpose of the Project

This project demonstrates:

✔ practical text preprocessing
✔ transformer-based NLP for real-world problems
✔ extracting meaningful themes from noisy user reviews
✔ generating actionable insights from textual data

It can be extended to:

cross-bank app benchmarking

topic modeling (LDA/BERT)

sentiment dashboards

automatic competitive analysis