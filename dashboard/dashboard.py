import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import numpy as np

API = "http://127.0.0.1:8000/detections"

st.title("Real-Time Object Detection Dashboard")

data = requests.get(API).json()

df = pd.DataFrame(data)

if len(df) > 0:

    st.subheader("Recent Detections")
    st.write(df)

    count = df["object"].value_counts()
    st.subheader("Object Frequency")
    fig = px.bar(
        x=count.index,
        y=count.values,
        labels={"x":"Object","y":"Count"}
    )
    st.plotly_chart(fig)

    st.subheader("Detection Timeline")
    if 'id' in df.columns:
        df['timestamp'] = df['id']  # Placeholder for timestamp
        fig2 = px.line(df, x='timestamp', y='confidence', color='object', title='Detection Confidence Over Time')
        st.plotly_chart(fig2)

    st.subheader("Detection Heatmap (Advanced)")
    if 'bbox' in df.columns:
        # Heatmap: visualize spatial distribution of detections
        heatmap = np.zeros((480, 640))  # Adjustable to frame size
        for bbox_str in df['bbox']:
            try:
                bbox = eval(bbox_str)
                x1, y1, x2, y2 = map(int, bbox)
                heatmap[y1:y2, x1:x2] += 1
            except:
                pass
        st.image(heatmap, caption="Detection Heatmap", use_column_width=True)

    st.subheader("Alerts & People Counting")
    if 'object' in df.columns:
        people_count = df[df['object'] == 'person'].shape[0]
        st.metric("People Count", people_count)
        if people_count > 10:
            st.warning("Alert: High number of people detected!")

    st.subheader("Performance Metrics")
    if 'confidence' in df.columns:
        avg_conf = df['confidence'].mean()
        st.metric("Average Confidence", f"{avg_conf:.2f}")

else:
    st.write("No detections yet.")