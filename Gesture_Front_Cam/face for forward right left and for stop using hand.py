import cv2
import dlib
import numpy as np
from scipy.spatial import distance as dist
import mediapipe as mp

# Load the pre-trained facial landmark detection model and face detector
predictor_path = "shape_predictor_68_face_landmarks.dat"
face_detector = dlib.get_frontal_face_detector()
landmark_predictor = dlib.shape_predictor(predictor_path)

# Create a MediaPipe Hands object
mp_hands = mp.solutions.hands.Hands(max_num_hands=1, min_detection_confidence=0.5, min_tracking_confidence=0.5)

# Initialize the video capture
cap = cv2.VideoCapture(0)  # Use the default webcam (change as needed)
cap.set(3, 640)  # Set the frame width
cap.set(4, 480)  # Set the frame height

while True:
    ret, frame = cap.read()
    if not ret:
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect faces in the frame
    faces = face_detector(gray)

    # Initialize the movement variable
    movement = None

    for face in faces:
        # Detect facial landmarks
        landmarks = landmark_predictor(gray, face)
        landmarks = [(p.x, p.y) for p in landmarks.parts()]

        # Detect the palm
        hands = mp_hands.process(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))

        # If a palm is detected, set the movement to "Stop"
        if hands.multi_hand_landmarks:
            movement = "Stop"

        # Otherwise, detect head orientation based on nose position relative to eyes
        else:
            nose_x = landmarks[30][0]
            left_eye_x = landmarks[36][0]
            right_eye_x = landmarks[42][0]

            if nose_x < left_eye_x:
                movement = "Left"
            elif nose_x > right_eye_x:
                movement = "Right"
            else:
                movement = "Forward"

    # Display the movement on the frame
    if movement is not None:
        cv2.putText(frame, f"Movement: {movement}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

    # Display the frame
    cv2.imshow("Face Movement Detection", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the video capture and close OpenCV windows
cap.release()
cv2.destroyAllWindows()
