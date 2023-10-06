import cv2
import dlib
import numpy as np
from scipy.spatial import distance as dist

# Load the pre-trained facial landmark detection model and face detector
predictor_path = "shape_predictor_68_face_landmarks.dat"
face_detector = dlib.get_frontal_face_detector()
landmark_predictor = dlib.shape_predictor(predictor_path)

# Initialize the video capture
cap = cv2.VideoCapture(0)  # Use the default webcam (change as needed)
cap.set(3, 640)  # Set the frame width
cap.set(4, 480)  # Set the frame height

# Initialize variables for eye state detection
left_eye_closed = False
right_eye_closed = False

# Constants for eye aspect ratio (EAR) threshold
EAR_THRESHOLD = 0.2

# Initialize variables for closed eye detection
closed_eye_frames = 0
CLOSED_EYE_FRAMES_THRESHOLD = 3  # Number of consecutive frames for closed eyes detection

while True:
    ret, frame = cap.read()
    if not ret:
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect faces in the frame
    faces = face_detector(gray)

    for face in faces:
        # Detect facial landmarks
        landmarks = landmark_predictor(gray, face)
        landmarks = [(p.x, p.y) for p in landmarks.parts()]

        # Extract eye landmarks (assuming landmarks 36-41 for left eye and 42-47 for right eye)
        left_eye_landmarks = landmarks[36:42]
        right_eye_landmarks = landmarks[42:48]

        # Calculate eye aspect ratio to determine if the eyes are open or closed
        def eye_aspect_ratio(eye_landmarks):
            a = dist.euclidean(eye_landmarks[1], eye_landmarks[5])
            b = dist.euclidean(eye_landmarks[2], eye_landmarks[4])
            c = dist.euclidean(eye_landmarks[0], eye_landmarks[3])
            return (a + b) / (2.0 * c)

        left_ear = eye_aspect_ratio(left_eye_landmarks)
        right_ear = eye_aspect_ratio(right_eye_landmarks)

        # Average the eye aspect ratio for both eyes
        ear = (left_ear + right_ear) / 2.0

        # Detect closed eyes based on eye aspect ratio
        if ear < EAR_THRESHOLD:
            closed_eye_frames += 1
        else:
            closed_eye_frames = 0

        # Determine face movement based on eye states
        if closed_eye_frames >= CLOSED_EYE_FRAMES_THRESHOLD:
            movement = "Stop"
        else:
            # Detect head orientation based on nose position relative to eyes
            nose_x = landmarks[30][0]
            left_eye_x = left_eye_landmarks[3][0]
            right_eye_x = right_eye_landmarks[0][0]

            if nose_x < left_eye_x:
                movement = "Left"
            elif nose_x > right_eye_x:
                movement = "Right"
            else:
                movement = "Forward"

        # Display the movement on the frame
        cv2.putText(frame, f"Movement: {movement}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

    # Display the frame
    cv2.imshow("Face Movement Detection", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the video capture and close OpenCV windows
cap.release()
cv2.destroyAllWindows()