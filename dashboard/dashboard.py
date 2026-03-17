import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import numpy as np
import ast
import cv2
import time
import os
import base64

# -------------------- PAGE CONFIG --------------------
st.set_page_config(
    page_title="AI Surveillance System",
    layout="wide"
)

# -------------------- CUSTOM CSS --------------------
st.markdown("""
<style>
body {
    background: linear-gradient(135deg, #0f172a, #020617);
    color: white;
}
.block-container {
    padding-top: 1rem;
}
.card {
    background: rgba(255,255,255,0.05);
    backdrop-filter: blur(12px);
    border-radius: 15px;
    padding: 15px;
    box-shadow: 0px 0px 20px rgba(0,0,0,0.3);
}
.alert {
    animation: pulse 1s infinite;
    background: rgba(255, 0, 0, 0.2);
    padding: 15px;
    border-radius: 10px;
    border: 1px solid red;
}
@keyframes pulse {
    0% {opacity: 1;}
    50% {opacity: 0.5;}
    100% {opacity: 1;}
}
</style>
""", unsafe_allow_html=True)

# -------------------- SIDEBAR --------------------
st.sidebar.title("⚙️ Controls")
refresh_rate = st.sidebar.slider("Refresh Rate (sec)", 1, 5, 2)

# -------------------- HEATMAP --------------------
def get_points(df):
    pts = []
    for _, row in df.iterrows():
        try:
            x1, y1, x2, y2 = ast.literal_eval(str(row["bbox"]))
            pts.append((int((x1+x2)/2), int((y1+y2)/2)))
        except:
            continue
    return pts

def generate_heatmap(points):
    heatmap = np.zeros((480, 640), dtype=np.float32)
    for x, y in points:
        if 0 <= x < 640 and 0 <= y < 480:
            heatmap[y, x] += 1

    if np.max(heatmap) == 0:
        return np.zeros((480, 640, 3), dtype=np.uint8)

    heatmap = cv2.GaussianBlur(heatmap, (51,51), 0)
    heatmap = heatmap / np.max(heatmap)
    heatmap = np.uint8(255 * heatmap)
    heatmap = cv2.applyColorMap(heatmap, cv2.COLORMAP_JET)

    return heatmap

# -------------------- FETCH DATA --------------------
API = "http://127.0.0.1:8000/detections"

st.title("🚀 AI Surveillance System")

try:
    res = requests.get(API)
    data = res.json() if res.status_code == 200 else []
except:
    st.error("Backend not running")
    data = []

df = pd.DataFrame(data)

# -------------------- MAIN --------------------
if len(df) > 0:

    latest = df.iloc[-1]

    # -------------------- METRICS --------------------
    st.markdown("### 📊 Overview")
    c1, c2, c3, c4 = st.columns(4)

    c1.metric("👥 People", df[df["object"]=="person"].shape[0])
    c2.metric("📦 Total", len(df))
    c3.metric("🚨 Alerts", df[df["zone"]=="restricted"].shape[0])
    c4.metric("🚶 Entries", int(latest.get("entry_count",0)))

    st.markdown("---")

    # -------------------- CHARTS --------------------
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### 📊 Object Distribution")
        fig = px.pie(df, names="object")
        st.plotly_chart(fig, width="stretch")

    with col2:
        st.markdown("### 📍 Zone Distribution")
        fig2 = px.bar(df["zone"].value_counts())
        st.plotly_chart(fig2, width="stretch")

    st.markdown("---")

    # -------------------- HEATMAP + VIDEO --------------------
    col3, col4 = st.columns(2)

    with col3:
        st.markdown("### 🔥 Heatmap")
        heatmap = generate_heatmap(get_points(df))
        st.image(heatmap, channels="BGR", width="stretch")

    with col4:
        st.markdown("### 🎥 Live Feed")
        frame_path = "stream/frame.jpg"
        if os.path.exists(frame_path):
            frame = cv2.imread(frame_path)
            if frame is not None:
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                st.image(frame, width="stretch")

    st.markdown("---")

    # -------------------- ALERT --------------------
    st.markdown("### 🚨 Alerts")

    violations = df[df["zone"]=="restricted"]

    if len(violations) > 0:
        st.markdown('<div class="alert">⚠️ RESTRICTED ZONE BREACH DETECTED</div>', unsafe_allow_html=True)

        # 🔊 Browser sound
        audio_file = open("cv_engine/ma-ka-bhosda-aag.wav", "rb")
        audio_bytes = audio_file.read()
        st.audio(audio_bytes, format="audio/wav")

        st.dataframe(violations.tail(10), width="stretch")
    else:
        st.success("✅ All clear")

    st.markdown("---")

    # -------------------- DOWNLOAD --------------------
    st.markdown("### 📥 Export Data")
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button("Download CSV", csv, "detections.csv")

    # -------------------- TABLE --------------------
    st.markdown("### 📋 Full Logs")
    st.dataframe(df, width="stretch")

else:
    st.info("No detections yet.")

# -------------------- AUTO REFRESH --------------------
time.sleep(refresh_rate)
st.rerun()