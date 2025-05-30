import cv2
import numpy as np
import mediapipe as mp
from tensorflow.keras.models import load_model
from collections import deque, Counter

# Load model and labels
model = load_model('sign_model.h5')
label_classes = np.load('label_classes.npy')

# MediaPipe setup
mp_holistic = mp.solutions.holistic
mp_drawing = mp.solutions.drawing_utils

# Settings
MAX_SEQ_LENGTH = 30
PREDICTION_BUFFER = 10
CONFIDENCE_THRESHOLD = 0.2  # lowered to make it less strict

# Extract keypoints from frame
def extract_keypoints_from_frame(results):
    pose = np.array([[res.x, res.y, res.z] for res in results.pose_landmarks.landmark]).flatten() if results.pose_landmarks else np.zeros(33 * 3)
    lh = np.array([[res.x, res.y, res.z] for res in results.left_hand_landmarks.landmark]).flatten() if results.left_hand_landmarks else np.zeros(21 * 3)
    rh = np.array([[res.x, res.y, res.z] for res in results.right_hand_landmarks.landmark]).flatten() if results.right_hand_landmarks else np.zeros(21 * 3)
    return np.concatenate([pose, lh, rh])

# Draw keypoints
def draw_landmarks(image, results):
    if results.pose_landmarks:
        mp_drawing.draw_landmarks(image, results.pose_landmarks, mp.solutions.holistic.POSE_CONNECTIONS)
    if results.left_hand_landmarks:
        mp_drawing.draw_landmarks(image, results.left_hand_landmarks, mp.solutions.holistic.HAND_CONNECTIONS)
    if results.right_hand_landmarks:
        mp_drawing.draw_landmarks(image, results.right_hand_landmarks, mp.solutions.holistic.HAND_CONNECTIONS)

def main():
    cap = cv2.VideoCapture(0)
    seq = []
    pred_buffer = deque(maxlen=PREDICTION_BUFFER)

    print("Labels loaded:", label_classes)

    with mp_holistic.Holistic(min_detection_confidence=0.5, min_tracking_confidence=0.5) as holistic:
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                print("Camera not working.")
                break

            frame = cv2.flip(frame, 1)
            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image.flags.writeable = False
            results = holistic.process(image)
            image.flags.writeable = True

            # Draw keypoints
            draw_landmarks(frame, results)

            # Extract keypoints
            keypoints = extract_keypoints_from_frame(results)
            seq.append(keypoints)
            if len(seq) > MAX_SEQ_LENGTH:
                seq.pop(0)

            # Predict when sequence is full
            if len(seq) == MAX_SEQ_LENGTH:
                input_data = np.expand_dims(seq, axis=0)
                pred = model.predict(input_data, verbose=0)[0]
                class_id = np.argmax(pred)
                confidence = pred[class_id]
                label = label_classes[class_id]

                print(f"[DEBUG] Prediction: {label} | Confidence: {confidence:.2f} | Raw: {pred}")

                if confidence > CONFIDENCE_THRESHOLD:
                    pred_buffer.append(label)
                else:
                    pred_buffer.append("Detecting")

                # Use majority vote from buffer
                most_common_label, count = Counter(pred_buffer).most_common(1)[0]
                display_text = most_common_label if most_common_label != "Detecting" and count > (PREDICTION_BUFFER // 2) else "Detecting..."
                cv2.putText(frame, display_text, (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 255, 0), 3, cv2.LINE_AA)
            else:
                cv2.putText(frame, "Waiting for sequence...", (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (100, 100, 255), 2, cv2.LINE_AA)

            cv2.imshow("Real-time Sign Recognition", frame)

            if cv2.waitKey(10) & 0xFF == ord('q'):
                break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()