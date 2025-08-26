import cv2

# Use DirectShow for Windows
stream = cv2.VideoCapture(0, cv2.CAP_DSHOW)

if not stream.isOpened():
    print("Could not open webcam")
    exit()

while True:
    ret, frame = stream.read()
    if not ret:
        print("Failed to grab frame")
        break

    # Rotate 90 degrees clockwise
    frame = cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE)

    # Get frame dimensions
    h, w = frame.shape[:2]
    center_x, center_y = w // 2, h // 2

    # Draw crosshair (white lines, thickness 2)
    color = (255, 255, 255)
    thickness = 2
    length = 25  # pixels

    # Horizontal line (centered, 50px long)
    cv2.line(frame, (center_x - length // 2, center_y),
             (center_x + length // 2, center_y), color, thickness)

    # Vertical line (centered, 50px long)
    cv2.line(frame, (center_x, center_y - length // 2),
             (center_x, center_y + length // 2), color, thickness)


    cv2.imshow("USB Webcam with Crosshair", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

stream.release()
cv2.destroyAllWindows()
