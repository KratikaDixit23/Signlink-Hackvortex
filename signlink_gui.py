import cv2
import numpy as np
import mediapipe as mp
from tensorflow.keras.models import load_model
from collections import deque, Counter
import tkinter as tk
import pyttsx3
import threading

# Load model and labels
model = load_model('sign_model.h5')
label_classes = np.load('label_classes.npy')

# MediaPipe setup
mp_holistic = mp.solutions.holistic
mp_drawing = mp.solutions.drawing_utils

# Settings
MAX_SEQ_LENGTH = 30
PREDICTION_BUFFER = 10
CONFIDENCE_THRESHOLD = 0.2

# TTS setup
engine = pyttsx3.init()

def extract_keypoints_from_frame(results):
    pose = np.array([[res.x, res.y, res.z] for res in results.pose_landmarks.landmark]).flatten() if results.pose_landmarks else np.zeros(33 * 3)
    lh = np.array([[res.x, res.y, res.z] for res in results.left_hand_landmarks.landmark]).flatten() if results.left_hand_landmarks else np.zeros(21 * 3)
    rh = np.array([[res.x, res.y, res.z] for res in results.right_hand_landmarks.landmark]).flatten() if results.right_hand_landmarks else np.zeros(21 * 3)
    return np.concatenate([pose, lh, rh])

def draw_landmarks(image, results):
    if results.pose_landmarks:
        mp_drawing.draw_landmarks(image, results.pose_landmarks, mp.solutions.holistic.POSE_CONNECTIONS)
    if results.left_hand_landmarks:
        mp_drawing.draw_landmarks(image, results.left_hand_landmarks, mp.solutions.holistic.HAND_CONNECTIONS)
    if results.right_hand_landmarks:
        mp_drawing.draw_landmarks(image, results.right_hand_landmarks, mp.solutions.holistic.HAND_CONNECTIONS)

def speak(text):
    engine.say(text)
    engine.runAndWait()

def run_recognition(show_text=True, speak_text=False):
    cap = cv2.VideoCapture(0)
    seq = []
    pred_buffer = deque(maxlen=PREDICTION_BUFFER)
    last_output = ""

    with mp_holistic.Holistic(min_detection_confidence=0.5, min_tracking_confidence=0.5) as holistic:
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            frame = cv2.flip(frame, 1)
            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image.flags.writeable = False
            results = holistic.process(image)
            image.flags.writeable = True

            draw_landmarks(frame, results)
            keypoints = extract_keypoints_from_frame(results)
            seq.append(keypoints)
            if len(seq) > MAX_SEQ_LENGTH:
                seq.pop(0)

            if len(seq) == MAX_SEQ_LENGTH:
                input_data = np.expand_dims(seq, axis=0)
                pred = model.predict(input_data, verbose=0)[0]
                class_id = np.argmax(pred)
                confidence = pred[class_id]
                label = label_classes[class_id]

                if confidence > CONFIDENCE_THRESHOLD:
                    pred_buffer.append(label)
                else:
                    pred_buffer.append("Detecting")

                most_common_label, count = Counter(pred_buffer).most_common(1)[0]
                display_text = most_common_label if most_common_label != "Detecting" and count > (PREDICTION_BUFFER // 2) else "Detecting..."

                if display_text != "Detecting..." and display_text != last_output:
                    if show_text:
                        text_label.config(text=f"Recognized Sign: {display_text}")
                    if speak_text:
                        threading.Thread(target=speak, args=(display_text,)).start()
                    last_output = display_text

                cv2.putText(frame, display_text, (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 255, 0), 3, cv2.LINE_AA)
            else:
                cv2.putText(frame, "Waiting for sequence...", (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (100, 100, 255), 2, cv2.LINE_AA)

            cv2.imshow("Sign Recognition", frame)

            if cv2.waitKey(10) & 0xFF == ord('q'):
                break

    cap.release()
    cv2.destroyAllWindows()

def start_sign_to_text():
    threading.Thread(target=run_recognition, kwargs={"show_text": True, "speak_text": False}).start()

def start_sign_to_speech():
    threading.Thread(target=run_recognition, kwargs={"show_text": False, "speak_text": True}).start()

# GUI Setup
root = tk.Tk()
root.title("SignLink: Sign to Text & Speech")
root.geometry("400x220")
root.resizable(False, False)

title = tk.Label(root, text="Sign Language Recognition", font=("Arial", 18))
title.pack(pady=10)

text_label = tk.Label(root, text="Recognized Sign: ", font=("Arial", 14))
text_label.pack(pady=10)

btn_text = tk.Button(root, text="Sign to Text", font=("Arial", 12), command=start_sign_to_text)
btn_text.pack(pady=5)

btn_speech = tk.Button(root, text="Sign to Speech", font=("Arial", 12), command=start_sign_to_speech)
btn_speech.pack(pady=5)

quit_button = tk.Button(root, text="Quit", font=("Arial", 12), command=root.quit)
quit_button.pack(pady=10)

root.mainloop()
