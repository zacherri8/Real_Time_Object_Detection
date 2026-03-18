import cv2

def start_camera():
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)  

    if not cap.isOpened():
        print("Camera not detected")
        exit()


    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)

    
    cap.set(cv2.CAP_PROP_FPS, 30)

    
    cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)

    return cap