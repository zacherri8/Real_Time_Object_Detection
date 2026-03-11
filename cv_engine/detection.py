from ultralytics import YOLO
import cv2
import requests
from camera import start_camera
from tracker import track_objects

model = YOLO("../models/yolov8n.pt")

API_URL = "http://127.0.0.1:8000/detection"

cap = start_camera()

while True:
    ret, frame = cap.read()
    if not ret:
        break

    results = model(frame)
    annotated = results[0].plot()

    detections = []
    for box in results[0].boxes:
        x1, y1, x2, y2 = box.xyxy[0].tolist()
        conf = float(box.conf)
        cls = int(box.cls)
        detections.append([[x1, y1, x2, y2], conf, cls])

    tracks = track_objects(detections, frame)

    for track in tracks:
        track_id = track.track_id
        bbox = track.to_ltrb().tolist()
        det_class = track.det_class
        det_conf = track.det_conf
        name = model.names[det_class]

        data = {
            "object_type": name,
            "confidence": det_conf,
            "track_id": track_id,
            "bbox": bbox
        }
        try:
            response = requests.post(API_URL, json=data)
            print("POST status:", response.status_code, response.text)
        except Exception as e:
            print("Error sending detection:", e)

    cv2.imshow("Detection", annotated)

    if cv2.waitKey(1) == 27:
        break

cap.release()
cv2.destroyAllWindows()