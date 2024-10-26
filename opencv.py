import cv2
import numpy as np

def detect_laser():
    # Open the first webcam connected to the device
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Error: Could not open video stream.")
        return

    # Define the range of the red color in HSV
    # Adjust these values according to your need
    lower_red = np.array([0, 120, 70])
    upper_red = np.array([10, 255, 255])
    
    try:
        while True:
            # Capture frame-by-frame
            ret, frame = cap.read()
            if not ret:
                print("Error: Could not read frame.")
                break

            # Convert the frame to HSV (hue, saturation, value)
            hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

            # Create a binary mask where red colors are white and the rest is black
            mask = cv2.inRange(hsv, lower_red, upper_red)

            # Find contours in the mask
            contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

            for contour in contours:
                # Calculate area and remove small elements
                area = cv2.contourArea(contour)
                if area > 50:  # Minimum area threshold
                    # Find the center of the contour
                    M = cv2.moments(contour)
                    if M["m00"] != 0:
                        cX = int(M["m10"] / M["m00"])
                        cY = int(M["m01"] / M["m00"])
                    else:
                        cX, cY = 0, 0

                    # Draw the contour and center of the shape on the original frame
                    cv2.drawContours(frame, [contour], -1, (0, 255, 0), 2)
                    cv2.circle(frame, (cX, cY), 5, (255, 255, 255), -1)
                    # Print the location of the laser dot
                    print(f"Laser detected at: {cX}, {cY}")

            # Display the resulting frame
            cv2.imshow('Laser Pointer Detection', frame)

            # Break the loop on 'q' key press
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    finally:
        # Release the capture and close any OpenCV windows
        cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    detect_laser()
