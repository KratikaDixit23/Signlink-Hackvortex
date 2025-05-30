import os
import numpy as np
from sklearn.preprocessing import LabelEncoder
from tensorflow.keras.utils import to_categorical

KEYPOINTS_PATH = r"D:\speech_to_sign\signlink-module1\keypoints"
MAX_SEQ_LENGTH = 30  # Number of frames to consider

def pad_sequences(seq, max_len=MAX_SEQ_LENGTH):
    if len(seq) > max_len:
        return seq[:max_len]
    else:
        pad_width = max_len - len(seq)
        padding = np.zeros((pad_width, seq.shape[1]))
        return np.vstack((seq, padding))

def main():
    sequences = []
    labels = []

    classes = sorted(os.listdir(KEYPOINTS_PATH))
    print("Classes:", classes)

    for label in classes:
        class_path = os.path.join(KEYPOINTS_PATH, label)
        for npy_file in os.listdir(class_path):
            npy_path = os.path.join(class_path, npy_file)
            seq = np.load(npy_path)
            seq_padded = pad_sequences(seq)
            sequences.append(seq_padded)
            labels.append(label)

    sequences = np.array(sequences)
    print("Sequences shape:", sequences.shape)  # (num_samples, max_seq_length, features)

    # Encode labels
    le = LabelEncoder()
    labels_encoded = le.fit_transform(labels)
    labels_categorical = to_categorical(labels_encoded).astype(np.float32)

    print("Labels shape:", labels_categorical.shape)

    # Save processed data
    np.save('X.npy', sequences)
    np.save('y.npy', labels_categorical)
    np.save('label_classes.npy', le.classes_)

if __name__ == "__main__":
    main()
