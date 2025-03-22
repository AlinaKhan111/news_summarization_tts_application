import streamlit as st
import requests
import json

# ============================
# Streamlit Web App Setup
# ============================
st.set_page_config(page_title="📊 News Summarization & Sentiment Analysis", layout="wide")

st.markdown(
    """
    <style>
    /* Full Background Color */
    html, body, [class*="stApp"] {
        background: #0d1117; 
        color: #d1d1d1;
    }
    /* Main Container */
    .report-container {
        width: 80%;
        margin: 0 auto;
        padding-top: 30px;
    }
    /* Input Box Styling */
    .stTextInput>div>div>input {
        background-color: #1e1e1e;
        color: white !important;
        border-radius: 12px;
        padding: 12px;
        border: 1px solid #444;
    }
    /* Placeholder Text Color */
    .stTextInput>div>div>input::placeholder {
        color: #cccccc !important;
        opacity: 1;
    }
    /* Icon Color */
    .stTextInput>div>div>svg {
        fill: #cccccc !important;
    }
    /* Centering Button */
    div.stButton > button {
        display: block;
        margin: 0 auto;
        background-color: #4CAF50; 
        color: white;
        padding: 12px 24px;
        border-radius: 12px;
        font-size: 16px;
        transition: 0.3s;
    }
    div.stButton > button:hover {
        background-color: #45a049; 
        transform: scale(1.05);
    }
    /* Section Headers */
    .stMarkdown h1, .stMarkdown h2, .stMarkdown h3, .stSubheader {
        color: #ffdd57; 
    }
    /* JSON and Audio Sections */
    .stJson {
        background-color: #1e1e1e;
        border-radius: 12px;
        padding: 12px;
        color: #d1d1d1;
        width: 100%;
        overflow-x: auto;
    }
    .stAudio audio {
        width: 100%;
        margin-top: 12px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ============================
# Title and Instructions
# ============================
st.markdown(
    "<h1 style='text-align: center; color: #ffdd57;'>📊 News Summarization & Sentiment Analysis</h1>",
    unsafe_allow_html=True,
)
st.markdown(
    "<h3 style='text-align: center; color: #d1d1d1;'>Enter a company name to fetch relevant news, analyze sentiment, and generate an audio summary in Hindi.</h3>",
    unsafe_allow_html=True,
)

# ============================
# Input and Button Layout
# ============================
col1, col2, col3 = st.columns([1, 4, 1])

with col2:
    company_name = st.text_input("🏢 Enter Company Name", placeholder="e.g., Tesla, Apple, Microsoft")

# ============================
# Define API URL
# ============================
API_URL = "http://127.0.0.1:8000/analyze/"

# ============================
# Button to Analyze News
# ============================
col1, col2, col3 = st.columns([3, 2, 3])

with col2:
    if st.button("🔎 Analyze News"):
        if company_name:
            with st.spinner("⏳ Analyzing news and generating reports..."):
                try:
                    payload = {"company_name": company_name}
                    response = requests.post(API_URL, json=payload)

                    if response.status_code == 200:
                        data = response.json()
                        st.success("✅ Analysis complete!")

                        # Sentiment Analysis Report
                        st.subheader("📚 Sentiment Analysis Report")
                        with st.container():
                            st.json(data["report"], expanded=True)

                        # Audio Summary
                        st.subheader("🔊 Hindi Summary")
                        audio_path = data["audio_file_url"]
                        st.audio(audio_path, format="audio/mp3")

                    else:
                        st.error(f"⚠️ Error: {response.json().get('detail', 'Unknown error occurred.')}")

                except Exception as e:
                    st.error(f"⚠️ API connection error: {str(e)}")

        else:
            st.warning("⚠️ Please enter a valid company name.")
