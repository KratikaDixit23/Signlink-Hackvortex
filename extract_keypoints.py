import os
import cv2
import numpy as np
import mediapipe as mp

# Paths
DATASET_PATH = r"D:\speech_to_sign\signlink-module1\dataset"
KEYPOINTS_PATH = r"D:\speech_to_sign\signlink-module1\keypoints"

# Make sure keypoints folder exists
os.makedirs(KEYPOINTS_PATH, exist_ok=True)

mp_holistic = mp.solutions.holistic
mp_hands = mp.solutions.hands

def extract_keypoints_from_frame(results):
    # Pose landmarks (33*3)
    pose = np.array([[res.x, res.y, res.z] for res in results.pose_landmarks.landmark]).flatten() if results.pose_landmarks else np.zeros(33*3)
    # Left hand landmarks (21*3)
    lh = np.array([[res.x, res.y, res.z] for res in results.left_hand_landmarks.landmark]).flatten() if results.left_hand_landmarks else np.zeros(21*3)
    # Right hand landmarks (21*3)
    rh = np.array([[res.x, res.y, res.z] for res in results.right_hand_landmarks.landmark]).flatten() if results.right_hand_landmarks else np.zeros(21*3)

    return np.concatenate([pose, lh, rh])

def process_video(video_path):
    cap = cv2.VideoCapture(video_path)
    keypoints_all = []

    with mp_holistic.Holistic(static_image_mode=False, min_detection_confidence=0.5, min_tracking_confidence=0.5) as holistic:
        while True:
            ret, frame = cap.read()
            if not ret:
                break

            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = holistic.process(image)

            keypoints = extract_keypoints_from_frame(results)
            keypoints_all.append(keypoints)

    cap.release()
    return np.array(keypoints_all)

def main():
    for sign_class in os.listdir(DATASET_PATH):
        class_path = os.path.join(DATASET_PATH, sign_class)
        if not os.path.isdir(class_path):
            continue

        print(f"Processing sign: {sign_class}")
        save_class_path = os.path.join(KEYPOINTS_PATH, sign_class)
        os.makedirs(save_class_path, exist_ok=True)

        for video_file in os.listdir(class_path):
            video_path = os.path.join(class_path, video_file)
            print(f"  Extracting keypoints from {video_file} ...")
            keypoints_seq = process_video(video_path)

            # Save keypoints
            np.save(os.path.join(save_class_path, video_file.replace('.mp4', '.npy')), keypoints_seq)

if __name__ == "__main__":
    main()
