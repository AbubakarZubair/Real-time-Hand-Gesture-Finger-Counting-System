import cv2
import mediapipe as mp

# Initialize MediaPipe hands model
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7)
mp_drawing = mp.solutions.drawing_utils

# Function to count fingers
def count_fingers(hand_landmarks):
    if hand_landmarks:
        landmarks = hand_landmarks.landmark

        # Tips of the fingers
        finger_tips = [8, 12, 16, 20]

        # Base of the fingers
        finger_bases = [6, 10, 14, 18]

        # List to hold whether a finger is up or not
        fingers = []

        # Thumb
        if landmarks[4].x < landmarks[3].x:  # Thumb is different due to its position
            fingers.append(1)
        else:
            fingers.append(0)

        # Other fingers
        for tip, base in zip(finger_tips, finger_bases):
            if landmarks[tip].y < landmarks[base].y:  # If the tip is higher than the base, finger is up
                fingers.append(1)
            else:
                fingers.append(0)

        return fingers.count(1)
    return 0

# Capture video from webcam
cap = cv2.VideoCapture(0)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Convert the BGR image to RGB
    image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Process the image and find hands
    results = hands.process(image)

    finger_count = 0

    # Draw hand landmarks on the frame
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            # Count fingers
            finger_count += count_fingers(hand_landmarks)

        # Display the finger count
        cv2.putText(frame, f'Total Fingers: {finger_count}', (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    # Display the frame
    cv2.imshow('Finger Counting', frame)

    # Break the loop on 'q' key press
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
