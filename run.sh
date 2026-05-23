#!/bin/bash

echo " Starting FastAPI Backend..."
uvicorn src.api:app --host 0.0.0.0 --port 8000 --reload &
sleep 5
echo " FastAPI Backend is running!"

echo " Starting Streamlit Frontend..."
streamlit run src/app.py
echo " Streamlit is running!"
