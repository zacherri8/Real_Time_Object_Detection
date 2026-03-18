from ultralytics import YOLO
import cv2
import requests
import os
import numpy as np
import time
import threading
from playsound import playsound
from cv_engine.camera import start_camera
from cv_engine.tracker import track_objects

# -------------------- MODEL --------------------
model = YOLO("yolov8m.pt")
API_URL = "http://127.0.0.1:8000/detection"

# -------------------- MULTI ZONES --------------------
ZONES = {
    "restricted": (200, 100, 450, 350),
    "safe": (0, 0, 200, 200),
    "monitor": (450, 0, 640, 200)
}

# 🎨 Zone colors
ZONE_COLORS = {
    "restricted": (0, 0, 255),
    "safe": (0, 255, 0),
    "monitor": (0, 255, 255)
}

# -------------------- HEATMAP --------------------
heatmap_accumulator = None

def check_zones(points):
    alerts = []
    for name, (zx1, zy1, zx2, zy2) in ZONES.items():
        for (x, y) in points:
            if zx1 <= x <= zx2 and zy1 <= y <= zy2:
                alerts.append(name)
    return alerts


# ---------------- ENTRY / EXIT TRACKING ----------------
zone_history = {}
entry_count = 0
exit_count = 0

# ---------------- SMART ALERT ----------------
last_alert_time = 0

# 🔊 SOUND FUNCTION (NON-BLOCKING)
def play_alert_sound():
    try:
        playsound("cv_engine/ma-ka-bhosda-aag.wav")
    except Exception as e:
        print("Sound error:", e)


# -------------------- CAMERA --------------------
cap = start_camera()
frame_count = 0

# -------------------- MAIN LOOP --------------------
while True:
    ret, frame = cap.read()

    if not ret:
        print("⚠️ Camera failed, restarting...")
        cap.release()
        cap = start_camera()
        continue

    frame_count += 1

    if frame_count % 2 != 0:
        continue

    frame = cv2.resize(frame, (640, 480))

    # -------------------- DETECTION --------------------
    results = model(frame)
    annotated = results[0].plot()

    # -------------------- DRAW MULTI-ZONES --------------------
    for name, (x1, y1, x2, y2) in ZONES.items():
        color = ZONE_COLORS.get(name, (255, 255, 255))

        cv2.rectangle(annotated, (x1, y1), (x2, y2), color, 2)
        cv2.putText(
            annotated,
            name.upper(),
            (x1, y1 - 10),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            color,
            2
        )

    # -------------------- DETECTIONS --------------------
    points = []
    detections = []

    for box in results[0].boxes:
        x1, y1, x2, y2 = box.xyxy[0].tolist()
        conf = float(box.conf)
        cls = int(box.cls)

        if conf < 0.7:
            continue

        cx = int((x1 + x2) / 2)
        cy = int((y1 + y2) / 2)

        points.append((cx, cy))
        detections.append([[x1, y1, x2, y2], conf, cls])

    # -------------------- ZONE ALERT (WITH SOUND) --------------------
    zone_alerts = check_zones(points)
    current_time = time.time()

    if "restricted" in zone_alerts and current_time - last_alert_time > 3:
        cv2.putText(
            annotated,
            "ALERT: RESTRICTED ZONE!",
            (50, 50),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 0, 255),
            3
        )

        # 🔊 play sound without blocking
        threading.Thread(target=play_alert_sound, daemon=True).start()

        last_alert_time = current_time

    # -------------------- HEATMAP --------------------
    if heatmap_accumulator is None:
        heatmap_accumulator = np.zeros((480, 640), dtype=np.float32)

    for x, y in points:
        if 0 <= x < 640 and 0 <= y < 480:
            heatmap_accumulator[y, x] += 1

    heatmap_accumulator *= 0.92
    heatmap_accumulator = np.clip(heatmap_accumulator, 0, 50)

    heatmap = cv2.GaussianBlur(heatmap_accumulator, (51, 51), 0)

    if np.max(heatmap) > 0:
        heatmap = heatmap / np.max(heatmap)
        heatmap = np.uint8(255 * heatmap)
        heatmap = cv2.applyColorMap(heatmap, cv2.COLORMAP_JET)
        annotated = cv2.addWeighted(annotated, 0.7, heatmap, 0.3, 0)

    # -------------------- STREAM FRAME --------------------
    os.makedirs("stream", exist_ok=True)
    final_path = "stream/frame.jpg"

    try:
        cv2.imwrite(final_path, annotated)
    except Exception as e:
        print("Frame write error:", e)

    # -------------------- TRACKING --------------------
    tracks = track_objects(detections, frame)

    for track in tracks:
        try:
            track_id = int(track.track_id) if track.track_id is not None else -1
            bbox = track.to_ltrb().tolist()
            det_class = int(track.det_class)
            det_conf = float(track.det_conf)
            name = model.names[det_class]
            if name not in ["person", "cell phone", "lighter"]:
                continue

            x1, y1, x2, y2 = bbox
            cx = int((x1 + x2) / 2)
            cy = int((y1 + y2) / 2)

            current_zone = "none"

            for zone_name, (zx1, zy1, zx2, zy2) in ZONES.items():
                if zx1 <= cx <= zx2 and zy1 <= cy <= zy2:
                    current_zone = zone_name

            # ---------------- ENTRY / EXIT ----------------
            prev_zone = zone_history.get(track_id, "none")

            if prev_zone == "none" and current_zone != "none":
                entry_count += 1
                print(f"ENTRY: {track_id} → {current_zone}")

            elif prev_zone != "none" and current_zone == "none":
                exit_count += 1
                print(f"EXIT: {track_id}")

            zone_history[track_id] = current_zone

            # ---------------- SEND DATA ----------------
            data = {
                "object": name,
                "confidence": det_conf,
                "track_id": track_id,
                "bbox": bbox,
                "zone": current_zone,
                "entry_count": entry_count,
                "exit_count": exit_count
            }

            if frame_count % 5 == 0:
                try:
                    requests.post(API_URL, json=data, timeout=0.5)
                except:
                    pass

        except Exception as e:
            print("Tracking error:", e)

    # -------------------- DISPLAY --------------------
    cv2.imshow("Detection", annotated)

    if cv2.waitKey(1) == 27:
        break

# -------------------- CLEANUP --------------------
cap.release()
cv2.destroyAllWindows()