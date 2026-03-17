import cv2

cap = cv2.VideoCapture(0)

resolutions = [
    (640, 480),
    (1280, 720),
    (1920, 1080)
]

for w, h in resolutions:
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, w)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, h)

    actual_w = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
    actual_h = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)

    print(f"Requested: {w}x{h} -> Got: {int(actual_w)}x{int(actual_h)}")

cap.release()