# **NEWS_SUMMARIZATION_TTS_APPLICATION**

### This project extracts news articles, performs sentiment analysis, identifies key topics, and generates a Hindi Text-to-Speech (TTS) summary. The final report includes comparative sentiment scores, coverage differences, and topic overlap.


# **🎯 Objective**

### This application extracts news articles, key details from multiple news articles about a given company, performs sentiment analysis, conducts a comparative analysis, and generates a text-to-speech (TTS) output in Hindi.The final report includes comparative sentiment scores, coverage differences, and topic overlap. Users can enter a company name, receive a structured sentiment report, and listen to the audio output.

# **🚀 Features**

### ✅ Extracts title, summary, and relevant metadata from at least 10 news articles.
### ✅ Performs sentiment analysis to classify articles as Positive, Negative, or Neutral.
### ✅ Conducts comparative sentiment analysis to highlight differences in coverage.
### ✅ Generates Hindi audio output using Text-to-Speech (TTS) models.
### ✅ Provides a user-friendly interface using Streamlit.
### ✅ API communication between frontend and backend for seamless integration.



# **📚 Table of Contents**
### 1. ***🚀 Project Setup***

### 2. ***🧠 Model Details***

### 3. ***🌐 API Development***

### 4. ***🔗 API Usage***

   

# **🚀 Project Setup**
Follow these steps to install and run the application:

1. **Clone the Repository:**
```bash
git clone https://github.com/AlinaKhan111/news_summarization_tts_application.git
cd news_summarization_tts_application
```

2. **Build the Docker Image:**
```bash
# Build the Docker image
sudo docker build -t my-app .
```  
The Dockerfile installs required dependencies, downloads necessary NLTK and SpaCy models, and sets up the environment.

The final Docker image will be tagged as my-app.

3. **Run the Docker Container:**
```bash
# Run the Docker container
sudo docker run -p 8000:8000 -p 8501:8501 my-app
```
* -p 8000:8000 – Exposes FastAPI on port 8000.

* -p 8501:8501 – Exposes Streamlit on port 8501.

✅ Application is now running and accessible at:

* FastAPI (API Endpoints): http://localhost:8000

* Streamlit (User Interface): http://localhost:8501




### 🔥 **Docker Management Commands**
---

1. Stop the Container
```bash
docker stop <container_id>
```

2. View Running Containers
```bash
docker ps
```

3. Remove Container
```bash
docker rm <container_id>
```

## **🐳 Docker Workflow Overview**

The application is containerized using Docker, allowing for easy deployment and ensuring a consistent runtime environment.

**📦 Dockerfile Breakdown**
1. **Base Image**

`FROM python:3.9-slim`
* Uses the lightweight version of Python 3.9 as the base image.
  

2. **Set Environment Variables**

`ENV PYTHONUNBUFFERED=1`
* Prevents Python from buffering outputs, useful for real-time logging.


3. **Set Working Directory**

`WORKDIR /app`
* Sets the working directory to /app where the application files will reside.


4. **Install Dependencies**

`COPY src/requirement.txt /app/requirement.txt`  
`RUN pip install --no-cache-dir -r /app/requirement.txt`
* Copies requirement.txt and installs dependencies inside the container.


5. **Download NLP Models**

`RUN python -m nltk.downloader punkt stopwords`  
`RUN python -m spacy download en_core_web_sm`
* Downloads necessary NLTK and SpaCy models used for text processing and analysis.


6. **Copy Application Code**

`COPY src/ /app/src/`  
* Copies all application source files into the /app/src/ directory.


7. **Copy and Set Permissions for Run Script**

`COPY run.sh /app/run.sh`  
`RUN chmod +x /app/run.sh`  
* Copies run.sh to /app/ and grants execute permissions.


8. **Expose Ports**

`EXPOSE 8000 8501`
* Port 8000: Exposes FastAPI for backend APIs.

* Port 8501: Exposes Streamlit for the user interface.


9. **Run Application Using run.sh**

`CMD ["sh", "/app/run.sh"]`
* Runs the run.sh script to start both FastAPI and Streamlit services.


# **🧠 Model Details**

### The core functionality of this project is powered by multiple models that work together to extract, process, analyze, and generate meaningful insights from news articles. Below is a detailed explanation of the models and approaches used in the application.

### 1. *****📚 RSS Feed Parsing and News Extraction*****
---

**Library Used:** feedparser + BeautifulSoup

**Function Name:** `extract_news(company_name, max_articles=30)`

**Purpose:**

- Parses RSS feeds from multiple sources to retrieve news articles.

- Cleans and extracts summaries using BeautifulSoup.

- Filters articles based on relevant keywords.

**Approach:**

- Defines a list of RSS feeds from different sources.

- Dynamically generates company-specific search keywords.

- Iterates through RSS feeds, parses them, and filters relevant articles.

- Saves extracted articles as a CSV file in the /data/ directory.

**Model/Tool Used:**

- feedparser to parse RSS feeds.

- BeautifulSoup for cleaning HTML content.


### *****2. 💡 Sentiment Analysis*****
---
**Library Used:**  NLTK (VADER Sentiment Analyzer)

**Function Name:** `get_sentiment(text)`

**Purpose:**

- Analyzes sentiment of article titles and summaries.

- Classifies sentiment as Positive, Negative, or Neutral.

**Approach:**

- Initializes SentimentIntensityAnalyzer from NLTK.

- Computes polarity scores for the text.

- Classifies sentiment based on the compound score:

`>= 0.05 → Positive`

`<= -0.05 → Negative`

`Otherwise → Neutral`

**Model/Tool Used:**

-VADER (Valence Aware Dictionary and sEntiment Reasoner) – Pre-trained sentiment analysis model optimized for short social media-style texts.


### *****3. 🕵️‍♂️ Named Entity Recognition (NER) and Topic Extraction*****
---
**Library Used:** spaCy (en_core_web_sm)

**Function Name:** `extract_topics_ner(text)`

**Purpose:**

- Extracts key topics and entities from article titles and summaries.

- Identifies entities such as Organizations, Products, Locations, and Events.

**Approach:**

- Loads the en_core_web_sm model.

- Uses spaCy’s Named Entity Recognition (NER) pipeline.

- Extracts relevant entities and returns them as a list of topics.

**Model/Tool Used:**

- Pre-trained spaCy model (en_core_web_sm).

- Recognizes entities with labels like ORG, PRODUCT, GPE, and EVENT.


### *****4. 📝 Data Cleaning and Preprocessing*****
---
**Library Used:** NLTK, BeautifulSoup

**Function Name:** `clean_and_preprocess(text)`

**Purpose:**

- Cleans article summaries by removing HTML tags and special characters.

- Tokenizes, removes stopwords, and applies lemmatization.

**Approach:**

- Uses BeautifulSoup to extract clean text from HTML.

- Removes special characters and converts text to lowercase.

- Tokenizes and filters stopwords using NLTK.

- Applies lemmatization to standardize words.

**Model/Tool Used:**

- BeautifulSoup for HTML parsing.

- NLTK for tokenization, stopword removal, and lemmatization.


### *****5. 🔥 Topic Overlap and Comparative Analysis*****
---
**Function Names:**

- `get_topic_overlap(articles)` → Finds common and unique topics.

- `generate_coverage_differences(articles)` → Identifies coverage differences.

**Purpose:**

- Compares topics across different articles.

- Identifies differences in coverage and sentiment.

**Approach:**

- Compares topics extracted from multiple articles.

- Highlights differences in article coverage and sentiment.

- Provides insights into how different articles cover similar or unique topics.

### *****6. 🗣️ Hindi Text-to-Speech (TTS) Generation*****
---
**Library Used:** gTTS (Google Text-to-Speech)

**Function Name:** `generate_tts(summary_text, output_file="sentiment_summary_hindi.mp3")`

**Purpose:**

- Converts the sentiment analysis summary into Hindi audio.

- Generates an MP3 audio file with the final report.

**Approach:**

- Takes the generated summary text.

- Converts the text to speech in Hindi using gTTS.

- Saves the audio file to the /output/ directory.

**Model/Tool Used:**

- gTTS (Google Text-to-Speech API) for converting text into Hindi speech.
  

### *****7. 🎯 Sentiment Summary and Report Generation*****
---
**Function Names:**

- `generate_sentiment_summary(df, company_name)` → Generates sentiment summary.

- `save_final_report(company_name, articles_data, topic_overlap, coverage_differences, final_summary, audio_file_path)` → Saves the final report in JSON.

**Purpose:**

- Summarizes the sentiment analysis results.

- Creates a structured JSON report with all extracted data.

**Approach:**

- Generates a summary in Hindi with sentiment insights.

- Saves the final report in a structured JSON format in the /output/ directory.


### **🛠️ Pipeline Flow in utils.py**
***

**The following steps explain the complete pipeline flow in utils.py:**

**News Extraction:** Fetches and parses news articles from RSS feeds.

**Data Preprocessing:** Cleans the extracted text using BeautifulSoup and NLTK.

**Sentiment Analysis:** Analyzes sentiment using VADER.

**Topic Extraction:** Identifies topics using spaCy NER.

**Comparative Analysis:** Identifies differences in topic coverage and sentiment.

**Summary and TTS:** Generates a sentiment summary and converts it to Hindi audio.

**Report Generation:** Saves the analysis results as a JSON file.


# **🎨 Frontend Interface - app.py**
The frontend is built using Streamlit, allowing users to:

**✅ Input a company name.**
**✅ Fetch and analyze news related to the company.**
**✅ Generate a sentiment analysis report.**
**✅ Produce an audio summary in Hindi using TTS.**

### *****⚡️ 1. Streamlit UI Setup*****
---
**Library Used:** streamlit

**Purpose:** Set up the web interface with a custom layout and dark theme.

**Key Features:**

- Custom CSS for dark mode and improved UI.

- Centered input box and button styling.

- Responsive layout with column-based structure.

### *****📚 2. Company Name Input and API Setup*****
---
Accepts the company name as input using st.text_input().

**API Endpoint:**

`API_URL = "http://127.0.0.1:8000/analyze/"`
The API handles:

- News extraction

- Sentiment analysis

- Topic extraction

- Hindi TTS summary generation

### *****🔎 3. Analyze News and API Communication*****
---
**API Request Flow:**

- Sends a POST request with the company name.

- Displays the sentiment analysis report and audio summary.

- Handles errors such as:

    - Invalid company name.

    - API connectivity issues.

    - Unexpected server errors.

### *****📊 4. Sentiment Report and Audio Summary*****
---
Displays a JSON-formatted sentiment analysis report using st.json().

Plays the generated Hindi audio summary using st.audio().

### *****📡 5. API Communication Flow*****
---
**Endpoint:** http://127.0.0.1:8000/analyze/

**Method:** `POST`

**Payload:**
```bash
{
  "company_name": "Tesla"
}
```
**Success Response:**

- Sentiment analysis report with article details.

- URL of the Hindi audio file for playback.


### **📊 Workflow of app.py**
*** 

1. **Input Company Name:** User enters the company name.

2. **Analyze News:** Button click triggers the API call.

3. **API Request Handling:** Sends a POST request and processes the response.

4. **Display Results:** Shows the report and plays the audio.

5. **Error Handling:** Displays relevant error messages.


# **🌐 Backend API - api.py**

- The backend is powered by FastAPI and manages the core functionality, including:

- Processing news and generating sentiment analysis reports.

- Handling API requests and responses.

- Serving audio files dynamically.

### *****🚀 1. FastAPI Initialization and CORS Setup*****
---
**Library Used:** FastAPI, CORSMiddleware

**Purpose:**

- Initializes the FastAPI application.

- Enables CORS to allow requests from the frontend.

**CORS Configuration:**

`allow_origins=["*"]` – Allows all origins.

- Supports all methods and headers.

### *****📝 2. API Endpoints Overview*****
---
**🔎 1. `/analyze/`**
**Method:** `POST`

**Purpose:** Analyze news, perform sentiment analysis, and generate a Hindi TTS summary.

**Payload:**
`
{
  "company_name": "Tesla"
}`

**🎧 2. /download/{filename}**
**Method:** `GET`

**Purpose:** Serve the generated Hindi audio summary dynamically.

**Parameter:** `filename` in the URL.

**🚀 3. /**
**Method:** `GET`

**Purpose:** Health check endpoint to confirm that the API is running.

**No Payload Required.**


### *****🧠 3. Pydantic Model for Input Validation*****
---
**Model Name:** `CompanyRequest`

**Purpose:** Validates incoming request data.

**Fields:**

`company_name` – Name of the company to analyze.

### *****📚 4. Request Processing and Pipeline Execution*****
---
**Function Name:** `process_request(company_name)`

**Purpose:**

- Runs the complete news analysis pipeline.

- Validates and cleans the JSON report.

- Generates a URL for the audio file.

- Error Handling:

- Catches exceptions and logs errors.

- Converts NaN or Infinity values to string format for JSON safety.

### *****🔎 5. News Analysis API (`/analyze/`)*****
---
**Method:** `POST`

**Purpose:**

- Triggers the sentiment analysis pipeline.

- Returns the sentiment report and Hindi audio summary.

**Request Payload:**
```bash
{
  "company_name": "Tesla"
}
```
**Response (Success):**
```bash
{
  "report": {
    "Company": "Tesla",
    "Articles": [
      {"Title": "Tesla's New Model Breaks Sales Records", "Summary": "...", "Sentiment": "Positive"},
      {"Title": "Regulatory Scrutiny on Tesla's Self-Driving Tech", "Summary": "...", "Sentiment": "Negative"}
    ],
    "Final Sentiment Analysis": "Tesla’s latest news coverage is mostly positive."
  },
  "audio_file_url": "http://127.0.0.1:8000/download/sentiment_summary_hindi.mp3"
}
```
**Error Handling:**

- Invalid or empty company name.

- Internal server errors during processing.

### *****🎧 6. Audio File Download API (`/download/{filename}`)*****
---
**Method:** `GET`

**Purpose:**

- Dynamically serves audio files generated during analysis.

- Returns the Hindi summary as an MP3 file.

**URL Example:**

`http://127.0.0.1:8000/download/sentiment_summary_hindi.mp3`

**Response (Success):**

- Returns the audio file with audio/mp3 media type.

**Error Handling:**

- File not found returns 404 error.


### *****🌐 7. Root Endpoint (`/`)*****
---
**Method:** `GET`

**Purpose:**

- Health check endpoint to confirm that the API is running.

**Response:**
```bash
{
  "message": "News Summarization & Sentiment Analysis API is running! 🚀"
}
```

### **📡 API Workflow of `api.py`**
---

1. **Input Request:** User sends a POST request with the company name.

2. **Pipeline Execution:** `run_pipeline()` processes the request and generates:

- Sentiment analysis report.

- Hindi audio summary (MP3).

3. **Report Generation:**

- Validates the JSON data.

- Converts any NaN or Infinity values to string.

4. **Audio File Handling:**

- Audio file URL is returned dynamically using the /download/ endpoint.

5. **Error Handling:**

- Handles exceptions and returns appropriate error messages.


# **🔥 Application Workflow Overview**
The complete application workflow is initiated using `run.sh`, which performs the following tasks:

### **🎯 1. Start FastAPI Backend**
---
**Command:**

```bash
uvicorn src.api:app --host 0.0.0.0 --port 8000 --reload &
```
**Purpose:**

- Starts the FastAPI backend (api.py).

- Serves APIs for news extraction, sentiment analysis, and TTS generation.

- Serves audio files dynamically via /download/ endpoint. ✅ Status:

```bash
🚀 Starting FastAPI Backend...
✅ FastAPI Backend is running!
📚 2. Start Streamlit Frontend
```

### **📚 2. Start Streamlit Frontend**
---
**Command:**

```bash
streamlit run src/app.py
```
**Purpose:**

- Launches the Streamlit frontend (app.py).

- Accepts the company name and triggers news analysis.

- Displays sentiment reports and audio summaries. ✅ Status:

```bash
📚 Starting Streamlit Frontend...
✅ Streamlit is running!
```

### *****📡 Application Flow: Frontend → Backend → Middleware*****
---

**🏢 Step 1: User Input via app.py**
---
- User inputs the company name and clicks "🔎 Analyze News".

- Sends a POST request to FastAPI:

`URL: http://127.0.0.1:8000/analyze/`

**🔎 Step 2: Backend Processing in `api.py`**
---
**Route Triggered:** `/analyze/`

**Action:**

- Receives request and calls `process_request(company_name)`.

- process_request() runs run_pipeline(company_name) from utils.py.

**⚙️ Step 3: Core Processing in utils.py**
---
**Function Triggered:** `run_pipeline(company_name)`

**Pipeline Flow:**

- Extracts and cleans news.

- Performs sentiment analysis.

- Identifies topics with NER.

- Generates Hindi TTS summary.

- Saves and returns the report and audio path.

**📡 Step 4: API Response to Frontend**
---
**Response Sent:**

```bash
{
  "report": { ... },
  "audio_file_url": "http://127.0.0.1:8000/download/sentiment_summary_hindi.mp3"
}
```

**📚 Step 5: Display Results in `app.py`**
---
**Streamlit Actions:**

- Displays sentiment report using `st.json()`.

- Plays the Hindi audio summary using `st.audio()`.

**🎧 Step 6: Audio File Retrieval**
---
**URL Triggered:**

```bash
http://127.0.0.1:8000/download/sentiment_summary_hindi.mp3
```
**Route:** `/download/{filename}`

**Purpose:** Dynamically serves the generated MP3 audio file.

## **🤔 Assumptions & Limitations**
### **🎯 Assumptions**
**RSS Feeds Used:**

- News articles are extracted from RSS feeds instead of raw HTML websites.

- This simplifies extraction and reduces parsing complexity.

**Predefined Keywords:**

- Predefined company-specific keywords are used to filter relevant articles.

- Dynamic keyword generation is used for unknown companies.

**Pretrained Models for NLP Tasks:**

- Sentiment analysis uses a pre-trained VADER model from NLTK.

- Named Entity Recognition (NER) uses the pre-trained en_core_web_sm model from SpaCy.

### **⚡️ Limitations**
**RSS Feed Dependency:**

- The application relies on RSS feeds for extracting news.

- Any changes to RSS structure may affect the accuracy of extraction.

**Limited Language Support:**

- Hindi is the only supported language for TTS.

- No multilingual support for other languages yet.

**Model Limitations:**

- Sentiment and NER models may not capture domain-specific nuances accurately.

- VADER works best with short texts and may not handle complex narratives perfectly.


## **🚀 Hugging Face Deployment**
The application has been successfully deployed on Hugging Face Spaces and is accessible at the following URL:

🌐 Live Application URL
➡️ Click Here to Access the Application:
[Link Text](https://huggingface.co/spaces/AlinaaaKhannn/news-summarization-tts)










