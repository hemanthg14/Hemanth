import cv2
import mediapipe as mp
import numpy as np

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7)
mp_draw = mp.solutions.drawing_utils

def is_grabbing(landmarks):
    """
    Checks if the distance between the thumb tip and the index finger tip is below a threshold.
    """
    thumb_tip = landmarks[4]
    index_tip = landmarks[8]
    distance = np.linalg.norm(np.array(thumb_tip) - np.array(index_tip))
    return distance < 0.05  # Adjust threshold for "grab" detection

object_position = (200, 200)  # Initial object position
object_radius = 30  # Radius of the draggable object

cap = cv2.VideoCapture(0)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break
    frame = cv2.flip(frame, 1)
    height, width, _ = frame.shape
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb_frame)

    # Check for hand landmarks and process them within the loop
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            # This is where the code from the last cell should be placed
            landmarks = [(lm.x, lm.y) for lm in hand_landmarks.landmark]

            # Detect "grabbing" gesture
            if is_grabbing(landmarks):
                # Update object position to follow the index fingertip
                index_finger = landmarks[8]
                object_position = (int(index_finger[0] * width), int(index_finger[1] * height))

            # Draw hand landmarks
            mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

    # Draw draggable object
    cv2.circle(frame, object_position, object_radius, (255, 0, 0), -1)

    # Display the frame
    cv2.imshow("Virtual Drag and Drop", frame)

    # Exit the application when 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()