import numpy as np
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout
from tensorflow.keras.callbacks import ModelCheckpoint

def main():
    X = np.load('X.npy')
    y = np.load('y.npy')

    print("X shape:", X.shape)
    print("y shape:", y.shape)

    model = Sequential([
        LSTM(64, return_sequences=True, activation='relu', input_shape=(X.shape[1], X.shape[2])),
        Dropout(0.5),
        LSTM(32, activation='relu'),
        Dropout(0.5),
        Dense(y.shape[1], activation='softmax')
    ])

    model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

    checkpoint = ModelCheckpoint('sign_model.h5', monitor='val_accuracy', save_best_only=True, verbose=1)

    model.fit(X, y, epochs=30, batch_size=8, validation_split=0.2, callbacks=[checkpoint])

if __name__ == "__main__":
    main()
