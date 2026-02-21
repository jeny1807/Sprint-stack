import cv2
import numpy as np
import tkinter as tk
from tkinter import filedialog

def run_auto_follower():
    # 1. Select the video file from your computer
    root = tk.Tk()
    root.withdraw()
    video_path = filedialog.askopenfilename(title="Select Video", 
                                           filetypes=[("Video files", "*.mp4 *.avi *.mov")])
    root.destroy()

    if not video_path:
        return

    cap = cv2.VideoCapture(video_path)
    ret, frame = cap.read()
    if not ret:
        print("Error: Could not read video.")
        return

    # 2. SELECT THE OBJECT: Draw a box around what you want to follow
    # Click and drag your mouse, then press ENTER
    print("INSTRUCTIONS: Draw a box around the object, then press ENTER.")
    bbox = cv2.selectROI("Select Object", frame, fromCenter=False, showCrosshair=True)
    cv2.destroyWindow("Select Object")

    # 3. Initialize the Tracker
    tracker = cv2.TrackerMIL_create()
    tracker.init(frame, bbox)

    radius = 130 # Size of the sharp focus area

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Update the tracker to follow the object
        success, box = tracker.update(frame)
        
        output = frame.copy()
        
        if success:
            # Get the new coordinates of the moving object
            x, y, w, h = [int(v) for v in box]
            center = (x + w // 2, y + h // 2)

            # --- FOCUS EFFECT ---
            # Create a strong blur for the background
            blurred_bg = cv2.GaussianBlur(frame, (99, 99), 0)

            # Create a circular mask centered on the moving object
            mask = np.zeros(frame.shape[:2], dtype=np.uint8)
            cv2.circle(mask, center, radius, 255, -1)

            # Combine: Keep object sharp, make everything else blurry
            sharp_part = cv2.bitwise_and(frame, frame, mask=mask)
            blur_part = cv2.bitwise_and(blurred_bg, blurred_bg, mask=cv2.bitwise_not(mask))
            output = cv2.add(sharp_part, blur_part)

            # Draw a green indicator ring
            cv2.circle(output, center, radius, (0, 255, 0), 2)
        else:
            cv2.putText(output, "Lost Object! Press ESC", (50, 50), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

        cv2.imshow("Smart Follow Focus", output)

        # Press ESC to stop
        if cv2.waitKey(20) & 0xFF == 27:
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    run_auto_follower()