import cv2
import numpy as np
import serial
import threading
import time

# --- Load reference image of the bird ---
ref_img = cv2.imread(r"C:\Users\hlykk\PycharmProjects\WebcamTest\due.png", cv2.IMREAD_GRAYSCALE)  # <-- put your path here

if ref_img is None:
    print("Error: Could not load reference image!")
    exit()

orb = cv2.ORB_create(nfeatures=1000)
kp_ref, des_ref = orb.detectAndCompute(ref_img, None)

# FLANN matcher for ORB
FLANN_INDEX_LSH = 6
index_params = dict(algorithm=FLANN_INDEX_LSH,
                    table_number=6, key_size=12, multi_probe_level=1)
search_params = dict(checks=50)
flann = cv2.FlannBasedMatcher(index_params, search_params)

# --- Serial setup (Arduino) ---
ser = serial.Serial('COM4', 9600, timeout=1)  # change COM3 if needed
time.sleep(2)  # allow Arduino reset
bang_trigger = False

def serial_listener():
    global bang_trigger
    while True:
        try:
            line = ser.readline().decode('utf-8').strip()
            if line == "BANG":
                bang_trigger = True
        except:
            pass

threading.Thread(target=serial_listener, daemon=True).start()

# --- Webcam ---
stream = cv2.VideoCapture(0, cv2.CAP_DSHOW)

if not stream.isOpened():
    print("Could not open webcam")
    exit()

while True:
    ret, frame = stream.read()
    if not ret:
        break

    # Rotate frame 90° clockwise
    frame = cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE)

    # Draw crosshair
    h, w = frame.shape[:2]
    cx, cy = w // 2, h // 2
    cv2.line(frame, (cx - 12, cy), (cx + 12, cy), (255, 255, 255), 2)
    cv2.line(frame, (cx, cy - 12), (cx, cy + 12), (255, 255, 255), 2)

    # --- Bird recognition ---
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    kp_frame, des_frame = orb.detectAndCompute(gray, None)

    if des_frame is not None and len(kp_frame) > 0:
        matches = flann.knnMatch(des_ref, des_frame, k=2)
        good = []
        for m_n in matches:
            if len(m_n) == 2:  # avoid "not enough values" error
                m, n = m_n
                if m.distance < 0.7 * n.distance:
                    good.append(m)

        if len(good) > 15:
            src_pts = np.float32([kp_ref[m.queryIdx].pt for m in good]).reshape(-1, 1, 2)
            dst_pts = np.float32([kp_frame[m.trainIdx].pt for m in good]).reshape(-1, 1, 2)

            M, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, 5.0)

            if M is not None:
                h_ref, w_ref = ref_img.shape
                pts = np.float32([[0, 0], [0, h_ref - 1],
                                  [w_ref - 1, h_ref - 1], [w_ref - 1, 0]]).reshape(-1, 1, 2)
                dst = cv2.perspectiveTransform(pts, M)
                cv2.polylines(frame, [np.int32(dst)], True, (0, 255, 0), 3)

                cv2.putText(frame, "Bird detected", (50, 50),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        # --- Show BANG effect if button pressed ---
    if bang_trigger:
        cv2.putText(frame, "BANG!", (cx - 70, cy - 100),
                    cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 5)
        bang_trigger = False  # reset after showing once

    cv2.imshow("Webcam with Bird & BANG", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

stream.release()
cv2.destroyAllWindows()
