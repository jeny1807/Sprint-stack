import cv2
import numpy as np


# Global variables
selected_point = None
radius = 100

# Mouse click function
def click_event(event, x, y, flags, param):
    global selected_point
    if event == cv2.EVENT_LBUTTONDOWN:
        selected_point = (x, y)

# Start webcam (use "video.mp4" instead of 0 for video file)
cap = cv2.VideoCapture(0)

cv2.namedWindow("Smart Focus")
cv2.setMouseCallback("Smart Focus", click_event)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    output = frame.copy()

    if selected_point is not None:
        # Create blurred version
        blurred = cv2.GaussianBlur(frame, (51, 51), 0)

        # Create circular mask
        mask = np.zeros(frame.shape[:2], dtype=np.uint8)
        cv2.circle(mask, selected_point, radius, 255, -1)

        # Combine sharp + blurred
        sharp_area = cv2.bitwise_and(frame, frame, mask=mask)
        blurred_area = cv2.bitwise_and(blurred, blurred, mask=cv2.bitwise_not(mask))
        output = cv2.add(sharp_area, blurred_area)

        # Draw circle outline
        cv2.circle(output, selected_point, radius, (0, 255, 0), 2)

    cv2.imshow("Smart Focus", output)

    key = cv2.waitKey(1) & 0xFF

    if key == 27:  # ESC key
        break
    elif key == ord('r'):  # Reset selection
        selected_point = None

cap.release()
cv2.destroyAllWindows()

# Global variables
selected_point = None
radius = 100

# Mouse click function
def click_event(event, x, y, flags, param):
    global selected_point
    if event == cv2.EVENT_LBUTTONDOWN:
        selected_point = (x, y)

# Start webcam (use "video.mp4" instead of 0 for video file)
cap = cv2.VideoCapture(0)

cv2.namedWindow("Smart Focus")
cv2.setMouseCallback("Smart Focus", click_event)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    output = frame.copy()

    if selected_point is not None:
        # Create blurred version
        blurred = cv2.GaussianBlur(frame, (51, 51), 0)

        # Create circular mask
        mask = np.zeros(frame.shape[:2], dtype=np.uint8)
        cv2.circle(mask, selected_point, radius, 255, -1)

        # Combine sharp + blurred
        sharp_area = cv2.bitwise_and(frame, frame, mask=mask)
        blurred_area = cv2.bitwise_and(blurred, blurred, mask=cv2.bitwise_not(mask))
        output = cv2.add(sharp_area, blurred_area)

        # Draw circle outline
        cv2.circle(output, selected_point, radius, (0, 255, 0), 2)

    cv2.imshow("Smart Focus", output)

    key = cv2.waitKey(1) & 0xFF

    if key == 27:  # ESC key
        break
    elif key == ord('r'):  # Reset selection
        selected_point = None

cap.release()