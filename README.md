**🎥 VisionGuard AI: Smart Surveillance System**

An advanced AI-powered surveillance system built with Python, OpenCV, YOLOv8, FastAPI, and Streamlit that performs real-time object detection, zone monitoring, intrusion alerts, and analytics through an interactive dashboard.

**📌 Features:**

**🧠 Real-Time Object Detection**

Uses YOLOv8 for live detection via webcam

Tracks objects with unique IDs

Filters important objects (e.g., person)

**📍 Multi-Zone Monitoring**

Define multiple zones:

🔴 Restricted Zone (alerts)

🟢 Safe Zone

🟡 Monitoring Zone

Detects when a person enters/exits zones

**🚶 Entry / Exit Tracking**

Tracks movement of individuals across zones

Counts:

Entries

Exits

Works using object tracking IDs

**🔥 Heatmap Analytics**

Visualizes activity distribution across frame

Shows high-traffic areas using color gradients

**🚨 Smart Alert System**

Detects intrusion in restricted zones

Displays on-screen alert

Plays custom alarm sound

Cooldown system prevents alert spam

**🎥 Live Video Streaming**

Real-time annotated video feed

Overlay includes:

Bounding boxes

Zones

Heatmap

**📊 Interactive Dashboard**

Live analytics dashboard with:

Object frequency

Zone distribution

Entry/Exit metrics

Heatmap visualization

Live camera feed embedded

Download detection logs as CSV

**📡 Backend API**

Stores detection data in database

Provides endpoints for dashboard

Handles real-time updates

**🗂️ Project Structure**

VisionGuard_AI/

├── backend/

│   ├── main.py              
│   ├── models.py            
│   └── database.py
│

├── cv_engine/

│   ├── detection.py         
│   ├── camera.py           
│   ├── tracker.py           
│   └── alert.wav            
│

├── dashboard/

│   └── dashboard.py       
│

├── stream/

│   └── frame.jpg          
│

├── run_all.py               
└── requirements.txt
└── test_camera.py
└── test_sound.py

**⚙️ Requirements**

Python 3.10 / 3.11

Webcam

Windows / Linux

**📦 Installation**

Install dependencies:

pip install ultralytics

pip install opencv-python

pip install fastapi uvicorn

pip install streamlit

pip install sqlalchemy

pip install numpy pandas plotly

pip install pygame

**▶️ Running the Project**

**🚀 One Terminal (Recommended)**

Run this command: python run_all.py

**🧪 Three Terminals**

**Terminal 1**

Run this command: python -m uvicorn backend.main:app --reload

**Terminal 2**

Run this command: python -m cv_engine.detection

**Terminal 3**

Run this command: streamlit run dashboard/dashboard.py

**🎯 System Flow**

Camera starts detection

Objects are tracked and classified

Zone logic determines entry/exit

Alerts triggered for restricted zones

Data sent to backend

Dashboard updates in real-time

**📊 Detection Data Format**

Object, Confidence, Track ID, Zone, Entry Count, Exit Count

**🚨 Alert Behavior**

Triggered when a person enters restricted zone

Plays custom alarm sound

Displays warning on screen

Logged in dashboard

**🔥 Built With**

YOLOv8 (Ultralytics) — Object Detection

OpenCV — Video Processing

FastAPI — Backend API

Streamlit — Dashboard UI

SQLAlchemy — Database ORM

NumPy / Pandas — Data Processing

**🧠 Key Highlights**

Real-time AI surveillance system

Multi-zone intelligence

Entry/exit tracking

Heatmap analytics

Dashboard visualization

Scalable architecture

**🚀 Future Enhancements**

Face recognition integration

Mobile / Telegram alerts

Cloud deployment

Behavior detection (loitering, crowding)

Video recording on intrusion

**👨‍💻 Author**

Satyam Chattopadhyay

BTech | Computer Vision & AI Enthusiast

