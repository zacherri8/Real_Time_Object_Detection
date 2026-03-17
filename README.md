**Project Title: Real Time Object Detection Dashboard**

This project performs real-time object detection and displays detections in a dashboard.

## Installation

1. Clone the repository

git clone https://github.com/zacherri8/Real_Time_Object_Detection.git

cd real-time-object-detection

2. Install dependencies

pip install -r requirements.txt

## Running the Project

Open **3 terminals**

Terminal 1 – Start Backend API

Run this: python -m uvicorn backend.main:app --reload

Terminal 2 – Start Computer Vision Engine

Run this: python -m cv_engine.detection

Terminal 3 – Start Dashboard

Run this: streamlit run dashboard/dashboard.py

