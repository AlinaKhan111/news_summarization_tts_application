# Use the official slim version of Python 3.9
FROM python:3.9-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Set the working directory
WORKDIR /app

# Copy the requirements file from src/ to /app/
COPY src/requirement.txt /app/requirement.txt

# Install dependencies from requirements
RUN pip install --no-cache-dir -r /app/requirement.txt

# Download required NLTK data
RUN python -m nltk.downloader punkt stopwords

# Download Spacy model
RUN python -m spacy download en_core_web_sm

# Copy the application code
COPY src/ /app/src/

# Copy run.sh script to /app/
COPY run.sh /app/run.sh

# Grant execute permissions to run.sh
RUN chmod +x /app/run.sh

# Expose necessary ports for FastAPI and Streamlit
EXPOSE 8000 8501

# Run the shell script to start FastAPI and Streamlit
CMD ["sh", "/app/run.sh"]
