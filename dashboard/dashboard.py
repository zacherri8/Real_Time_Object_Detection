import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import numpy as np
import ast
import cv2
import time

# -------------------- PAGE CONFIG --------------------
st.set_page_config(
    page_title="AI Detection Dashboard",
    layout="wide"
)

# -------------------- HEATMAP HELPERS --------------------

def get_points(df):
    points = []

    for _, row in df.iterrows():
        try:
            bbox = ast.literal_eval(str(row["bbox"]))
            x1, y1, x2, y2 = bbox

            cx = int((x1 + x2) / 2)
            cy = int((y1 + y2) / 2)

            points.append((cx, cy))
        except:
            continue

    return points


def generate_heatmap(points, width=640, height=480):
    heatmap = np.zeros((height, width), dtype=np.float32)

    for x, y in points:
        try:
            x = int(x)
            y = int(y)

            if 0 <= x < width and 0 <= y < height:
                heatmap[y, x] += 1
        except:
            continue

    if np.max(heatmap) == 0:
        return np.zeros((height, width, 3), dtype=np.uint8)

    heatmap = cv2.GaussianBlur(heatmap, (51, 51), 0)
    heatmap = np.power(heatmap / np.max(heatmap), 0.3)
    heatmap = np.uint8(255 * heatmap)

    heatmap = cv2.applyColorMap(heatmap, cv2.COLORMAP_JET)

    return heatmap


# -------------------- MAIN DASHBOARD --------------------

API = "http://127.0.0.1:8000/detections"

st.title("🚀 Real-Time Object Detection Dashboard")

data = requests.get(API).json()
df = pd.DataFrame(data)

if len(df) > 0:

    # -------------------- TOP METRICS --------------------
    col1, col2, col3 = st.columns(3)

    if 'object' in df.columns and 'id' in df.columns:
        latest_id = df['id'].max()
        latest_df = df[df['id'] == latest_id]

        people_count = latest_df[latest_df['object'] == 'person'].shape[0]
        col1.metric("👥 People (Live)", people_count)

    if 'confidence' in df.columns:
        avg_conf = df['confidence'].mean()
        col2.metric("📊 Avg Confidence", f"{avg_conf:.2f}")

    col3.metric("📦 Total Detections", len(df))

    st.markdown("---")

    # -------------------- CHARTS --------------------
    col4, col5 = st.columns(2)

    if "object" in df.columns:
        count = df["object"].value_counts()

        with col4:
            st.subheader("📊 Object Frequency")
            fig = px.bar(
                x=count.index,
                y=count.values,
                labels={"x": "Object", "y": "Count"}
            )
            st.plotly_chart(fig, width="stretch")

    if 'id' in df.columns and 'confidence' in df.columns and 'object' in df.columns:
        with col5:
            st.subheader("📈 Detection Timeline")
            df['timestamp'] = df['id']
            fig2 = px.line(
                df,
                x='timestamp',
                y='confidence',
                color='object'
            )
            st.plotly_chart(fig2, width="stretch")

    st.markdown("---")

    # -------------------- HEATMAP --------------------
    st.subheader("🔥 Detection Heatmap")

    if 'bbox' in df.columns:
        points = get_points(df)

        if len(points) > 0:
            heatmap = generate_heatmap(points)

            col6, col7 = st.columns([2, 1])

            with col6:
                st.image(heatmap, channels="BGR", width=700)

            with col7:
                st.markdown("### 📌 Heatmap Info")
                st.write(f"Total Points: {len(points)}")
                st.write("🔴 High activity")
                st.write("🟡 Medium activity")
                st.write("🔵 Low activity")

        else:
            st.info("Not enough data for heatmap yet.")

    st.markdown("---")

    # -------------------- TABLE --------------------
    st.subheader("📋 Recent Detections")
    st.dataframe(df, width="stretch")

else:
    st.write("No detections yet.")

# -------------------- AUTO REFRESH --------------------
time.sleep(2)
st.rerun()