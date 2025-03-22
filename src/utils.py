import os
import feedparser
import csv
import glob
import json
import requests
import pandas as pd
import re
import nltk
import spacy
from bs4 import BeautifulSoup
from gtts import gTTS
from nltk.sentiment import SentimentIntensityAnalyzer


#Global Paths & Config
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "../data")
OUTPUT_DIR = os.path.join(BASE_DIR, "../output")

# Create directories if they don't exist
os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Load spaCy NER model
nlp = spacy.load("en_core_web_sm")

# Initialize NLTK VADER Sentiment Analyzer
nltk.download('vader_lexicon')
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')
sia = SentimentIntensityAnalyzer()


# ============================
#  Predefined Company Keywords
# ============================
company_keywords = {
    "tesla": ["tesla", "elon musk", "tesla model", "tesla stock", "gigafactory"],
    "apple": ["apple", "tim cook", "iphone", "apple stock", "macbook"],
    "microsoft": ["microsoft", "satya nadella", "windows", "microsoft azure", "msft stock"],
    "google": ["google", "sundar pichai", "google search", "google stock", "android"],
    "amazon": ["amazon", "jeff bezos", "aws", "amazon prime", "amazon stock"],
    "nvidia": ["nvidia", "gpu", "rtx", "nvidia stock", "ai chips"]
}

def generate_search_keywords(company_name):
    """Generate search keywords for known or unknown companies."""
    company_name_lower = company_name.lower()

    # Use predefined keywords if company is known
    if company_name_lower in company_keywords:
        search_keywords = company_keywords[company_name_lower]
        print(f" Using predefined keywords for '{company_name}': {search_keywords}")
    else:
        # Generate dynamic keywords if company is unknown
        search_keywords = [
            company_name,
            f"{company_name} CEO",
            f"{company_name} news",
            f"{company_name} updates",
            f"{company_name} stock",
            f"{company_name} model",
            f"{company_name} launch"
        ]
        print(f" Using dynamically generated keywords for '{company_name}'.")
    
    return search_keywords

def extract_news(company_name, max_articles=30):
    """Extract news articles related to the company."""
    rss_feeds = [
        "https://rss.nytimes.com/services/xml/rss/nyt/Business.xml",
    "https://feeds.bbci.co.uk/news/business/rss.xml",
    "https://www.theverge.com/rss/index.xml",
    "https://feeds.marketwatch.com/marketwatch/topstories/",
    "https://feeds.reuters.com/reuters/businessNews",
    "https://www.cnbc.com/id/10001147/device/rss/rss.html",
    "https://arstechnica.com/feed/",
    "https://www.techradar.com/rss",
    "https://www.wired.com/feed/rss",
    "https://mashable.com/feeds/rss",
    "https://venturebeat.com/feed/",
    "https://finance.yahoo.com/rss/topstories",
    "https://www.investopedia.com/feedbuilder/feed/getfeed/?feedName=rss_articles",
    "https://www.autoblog.com/rss.xml",
    "https://www.carscoops.com/feed/",
    "https://www.motortrend.com/feed/",
    "https://news.crunchbase.com/feed/",
    "https://venturebeat.com/category/startups/feed/",
    "https://www.saastr.com/feed/",
    "https://www.artificialintelligence-news.com/feed/",
    "https://openai.com/feed/"
        ]
    
    google_news_url = f"https://news.google.com/rss/search?q={company_name.replace(' ', '+')}&hl=en-US&gl=US&ceid=US:en"
    rss_feeds.append(google_news_url)

    search_keywords = generate_search_keywords(company_name)
    keyword_patterns = [re.compile(rf'\b{re.escape(keyword.lower())}\b') for keyword in search_keywords]

    articles = []
    seen_titles = set()

    for rss_url in rss_feeds:
        if len(articles) >= max_articles:
            break
        try:
            feed = feedparser.parse(rss_url)
            for entry in feed.entries:
                title = entry.get('title', '').strip()
                if title in seen_titles or len(articles) >= max_articles:
                    continue
                
                summary = entry.get('summary', '').strip()
                link = entry.get('link', '').strip()
                published = entry.get('published', '').strip()

                summary_cleaned = BeautifulSoup(summary, "html.parser").get_text()
                if any(pattern.search(title.lower()) for pattern in keyword_patterns) or \
                   any(pattern.search(summary_cleaned.lower()) for pattern in keyword_patterns):
                    articles.append({
                        'Title': title,
                        'Summary': summary_cleaned,
                        'Link': link,
                        'Published': published,
                        'Source': rss_url
                    })
                    seen_titles.add(title)

        except Exception as e:
            print(f"⚠️ Error parsing feed {rss_url}. Skipping...")

    csv_file_path = os.path.join(DATA_DIR, f"{company_name}_news.csv")
    if articles:
        pd.DataFrame(articles).to_csv(csv_file_path, index=False)
        print(f"✅ Successfully saved {len(articles)} articles in '{csv_file_path}'.")
    else:
        print(f"⚠️ No articles found for '{company_name}'.")
    
    return csv_file_path


# Initialize stopwords and lemmatizer globally for efficiency
stop_words = set(nltk.corpus.stopwords.words('english'))
lemmatizer = nltk.WordNetLemmatizer()

# Cleaning and Preprocessing Functions
def clean_and_preprocess(text):
    """Clean text by removing HTML tags, special characters, and stopwords."""
    # Handle NaN or invalid values
    if pd.isnull(text) or not isinstance(text, str) or text.strip() == "":
        return ""
    
    # 1. Remove HTML tags
    text = BeautifulSoup(text, "html.parser").get_text()
    
    # 2. Remove special characters, numbers, and punctuation
    text = re.sub(r"[^a-zA-Z\s]", "", text).lower().strip()
    
    # 3. Tokenize
    tokens = nltk.word_tokenize(text)
    
    # 4. Remove stopwords and apply lemmatization
    filtered_tokens = [lemmatizer.lemmatize(word) for word in tokens if word not in stop_words]
    
    # 5. Join tokens back to string
    return " ".join(filtered_tokens)


#  Perform Sentiment Analysis
def get_sentiment(text):
    """Perform sentiment analysis on a given text."""
    if pd.isnull(text) or text == "":
        return "Neutral"
    sentiment_score = sia.polarity_scores(text)
    if sentiment_score['compound'] >= 0.05:
        return "Positive"
    elif sentiment_score['compound'] <= -0.05:
        return "Negative"
    else:
        return "Neutral"

# Extract Topics using NER
def extract_topics_ner(text):
    """Extract relevant topics using spaCy NER."""
    if pd.isnull(text) or text.strip() == "":
        return []
    
    doc = nlp(text)
    topics = set()

    # Extract entities related to organizations, products, locations, and events
    for ent in doc.ents:
        if ent.label_ in ["ORG", "PRODUCT", "GPE", "EVENT"]:
            topics.add(ent.text)

    return list(topics)

# Generate Hindi Text-to-Speech (TTS) Summary
def generate_tts(summary_text, output_file="sentiment_summary_hindi.mp3"):
    """Generate a Hindi TTS audio from the summary text."""
    tts = gTTS(text=summary_text, lang='hi')
    output_path = os.path.join(OUTPUT_DIR, output_file)
    tts.save(output_path)
    return output_path

# Generate Topic Overlap and Coverage Differences
def get_topic_overlap(articles):
    """Identify common and unique topics across articles."""
    all_topics = [set(article['Topics']) for article in articles]

    # Find common topics
    common_topics = set.intersection(*all_topics) if all_topics else set()

    # Find unique topics per article
    unique_topics = [
        list(topics - common_topics) for topics in all_topics
    ]

    return {
        "Common Topics": list(common_topics),
        "Unique Topics": unique_topics
    }

def generate_coverage_differences(articles):
    """Generate coverage differences between articles."""
    differences = []
    if len(articles) > 1:
        for i in range(len(articles) - 1):
            if not isinstance(articles[i]['Summary'], str) or not isinstance(articles[i+1]['Summary'], str):
                continue
            comparison = {
                "Comparison": f"Article {i+1} highlights {articles[i]['Summary'][:50]}... while Article {i+2} discusses {articles[i+1]['Summary'][:50]}...",
                "Impact": f"The first article emphasizes {articles[i]['Sentiment'].lower()} sentiment, while the second article reflects {articles[i+1]['Sentiment'].lower()} sentiment."
            }
            differences.append(comparison)
    return differences

# Generate Final Sentiment Analysis Summary
def generate_sentiment_summary(df, company_name):
    """Generate sentiment summary from analyzed articles."""
    # Count sentiment distribution
    title_sentiment_counts = df['Title_Sentiment'].value_counts().to_dict()
    positive_count = title_sentiment_counts.get('Positive', 0)
    negative_count = title_sentiment_counts.get('Negative', 0)

    # Determine overall sentiment
    if positive_count > negative_count:
        final_summary = f"{company_name} की नवीनतम समाचार कवरेज मुख्यतः सकारात्मक है। स्टॉक वृद्धि की संभावना है।"
    elif negative_count > positive_count:
        final_summary = f"{company_name} की नवीनतम समाचार कवरेज में कुछ नकारात्मक संकेत मिले हैं। निवेशकों को सतर्क रहना चाहिए।"
    else:
        final_summary = f"{company_name} की समाचार कवरेज में मिश्रित संकेत हैं। सकारात्मक और नकारात्मक दोनों पक्षों पर ध्यान दें।"

    # Generate TTS summary in Hindi
    summary_text = f"""
    नमस्ते, यह {company_name} के नवीनतम समाचार की भावना विश्लेषण रिपोर्ट है।
    कुल सकारात्मक लेख: {positive_count}
    कुल नकारात्मक लेख: {negative_count}
    तटस्थ लेख: {title_sentiment_counts.get('Neutral', 0)}
    अंतिम विश्लेषण: {final_summary}
    """
    audio_file_path = generate_tts(summary_text)

    return final_summary, audio_file_path

def save_final_report(company_name, articles_data, topic_overlap, coverage_differences, final_summary, audio_file_path):
    """Save the final sentiment report in JSON format."""
    report = {
        "Company": company_name,
        "Articles": articles_data,
        "Comparative Sentiment Score": {
            "Sentiment Distribution": {
                "Positive": sum(article['Sentiment'] == "Positive" for article in articles_data),
                "Negative": sum(article['Sentiment'] == "Negative" for article in articles_data),
                "Neutral": sum(article['Sentiment'] == "Neutral" for article in articles_data),
            },
            "Coverage Differences": coverage_differences,
            "Topic Overlap": topic_overlap
        },
        "Final Sentiment Analysis": final_summary,
        "Audio": audio_file_path
    }

    json_file_path = os.path.join(OUTPUT_DIR, f"{company_name}_comparative_sentiment_report.json")
    with open(json_file_path, "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=4)
    
    print(f"✅ Final report saved to '{json_file_path}'.")
    return json_file_path


# Main Pipeline Function
def run_pipeline(company_name):
    """Main function to orchestrate the news extraction, sentiment analysis, and TTS."""
    # Step 1: Extract news articles
    csv_file_path = extract_news(company_name)
    df = pd.read_csv(csv_file_path)

    # Step 2: Preprocess and clean the data
    df['Cleaned_Title'] = df['Title'].apply(clean_and_preprocess)
    df['Cleaned_Summary'] = df['Summary'].apply(clean_and_preprocess)

    # Step 3: Sentiment Analysis
    df['Title_Sentiment'] = df['Cleaned_Title'].apply(get_sentiment)
    df['Summary_Sentiment'] = df['Cleaned_Summary'].apply(get_sentiment)

    # Step 4: Extract Topics and Prepare Articles
    articles_data = []
    for idx, row in df.iterrows():
        title_topics = extract_topics_ner(row['Title'])
        summary_topics = extract_topics_ner(row['Summary'])
        combined_topics = list(set(title_topics + summary_topics))

        article_info = {
            "Title": row['Title'],
            "Summary": row['Summary'],
            "Sentiment": row['Title_Sentiment'],
            "Topics": combined_topics
        }
        articles_data.append(article_info)

    # Step 5: Generate Topic Overlap and Coverage Differences
    topic_overlap = get_topic_overlap(articles_data)
    coverage_differences = generate_coverage_differences(articles_data)

    # Step 6: Generate Final Sentiment Summary and TTS
    final_summary, audio_file_path = generate_sentiment_summary(df, company_name)

    # Step 7: Save Final Report in JSON
    json_file_path = save_final_report(company_name, articles_data, topic_overlap, coverage_differences, final_summary, audio_file_path)

    return json_file_path, audio_file_path


# if __name__ == "__main__":
#     Take company name dynamically as user input
#     company_name = input("🏢 Enter the company name for analysis: ").strip()

#     Check if input is valid
#     if not company_name:
#         print("⚠️ Company name cannot be empty. Please provide a valid name.")
#     else:
#         Run the pipeline for the given company
#         print(f"🚀 Running pipeline for '{company_name}'...")
#         report_path, audio_path = run_pipeline(company_name)

#         Confirm the output
#         print(f"✅ Report saved at: {report_path}")
#         print(f"✅ Hindi TTS audio saved at: {audio_path}")