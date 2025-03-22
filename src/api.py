from fastapi import FastAPI, HTTPException, BackgroundTasks
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import logging
from src.utils import run_pipeline
from fastapi.responses import FileResponse
import os
import json

AUDIO_DIR = os.path.join(os.path.dirname(__file__), "../output")

# ============================
# Initialize FastAPI App
# ============================
app = FastAPI()

# ============================
# Enable CORS for Frontend
# ============================
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============================
# Set Up Logging
# ============================
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ============================
# Define Pydantic Model
# ============================
class CompanyRequest(BaseModel):
    company_name: str

# ============================
# Helper Function to Process Request
# ============================

import json
import math

def process_request(company_name: str):
    """Run pipeline and log results."""
    try:
        report_path, audio_file = run_pipeline(company_name)

        # Read JSON data from the file
        with open(report_path, "r", encoding="utf-8") as f:
            report_data = json.load(f)

        # Check for NaN or Infinity values
        def validate_json(obj):
            if isinstance(obj, dict):
                for key, value in obj.items():
                    obj[key] = validate_json(value)
            elif isinstance(obj, list):
                obj = [validate_json(item) for item in obj]
            elif isinstance(obj, float):
                # Handle NaN and Infinity values
                if math.isnan(obj) or math.isinf(obj):
                    return str(obj)  # Convert to string for JSON safety
            return obj

        # Clean data before sending as response
        cleaned_report = validate_json(report_data)

        audio_filename = audio_file.split("/")[-1]
        audio_url = f"http://127.0.0.1:8000/download/{audio_filename}"

        logger.info(f"Analysis completed successfully for {company_name}")
        return {"report": cleaned_report, "audio_file_url": audio_url}

    except Exception as e:
        logger.error(f"Exception occurred: {str(e)}")
        return {"error": f"Internal server error: {str(e)}"}

# ============================
# API Endpoint to Analyze News
# ============================
@app.post("/analyze/")
async def analyze_news(request: CompanyRequest):
    company_name = request.company_name.strip()

    if not company_name:
        raise HTTPException(status_code=400, detail="Invalid company name provided.")

    # Run the pipeline to get report and audio file path
    result = process_request(company_name)

    if "error" in result:
        raise HTTPException(status_code=404, detail=result["error"])

    audio_filename = result["audio_file_url"].split("/")[-1]
    return {
        "report": result["report"], 
        "audio_file_url": result["audio_file_url"]
}

AUDIO_DIR = os.path.join(os.path.dirname(__file__), "../output")

@app.get("/download/{filename}")
def download_file(filename: str):
    """Endpoint to serve audio files dynamically."""
    file_path = os.path.join(AUDIO_DIR, filename)
    if os.path.exists(file_path):
        return FileResponse(file_path, media_type="audio/mp3", filename=filename)
    else:
        raise HTTPException(status_code=404, detail="Audio file not found.")



# ============================
# Root Endpoint
# ============================
@app.get("/")
def read_root():
    return {"message": "News Summarization & Sentiment Analysis API is running! 🚀"}
