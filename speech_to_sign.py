import os
import string
import whisper
import cv2
import sounddevice as sd
from scipy.io.wavfile import write
import threading
import tkinter as tk
from tkinter import messagebox

# Constants
DURATION = 5
FILENAME = "audio.wav"
VIDEO_FOLDER = "sign_videos"

# Load Whisper model once
model = whisper.load_model("base")

def record_audio():
    print("🎙️ Recording... Please speak now")
    fs = 44100
    recording = sd.rec(int(DURATION * fs), samplerate=fs, channels=2)
    sd.wait()
    write(FILENAME, fs, recording)
    print("✅ Recording complete")

def transcribe_audio():
    print("🧠 Transcribing your speech...")
    result = model.transcribe(FILENAME)
    text = result["text"].strip()
    print("💬 Transcribed Text:", text)
    return text

def play_video(video_path):
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        messagebox.showerror("Error", f"Failed to open video: {video_path}")
        return
    # Get the original width and height of the video frame
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    cv2.namedWindow("Sign Language", cv2.WINDOW_NORMAL)
    cv2.resizeWindow("Sign Language", width, height)

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        cv2.imshow("Sign Language", frame)
        # Press 'q' to close the video early
        if cv2.waitKey(25) & 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()

def play_sign_language(text):
    if not text.strip():
        messagebox.showwarning("Warning", "Please provide some text to play sign language.")
        return

    # Phrase first
    phrase = text.lower().translate(str.maketrans('', '', string.punctuation)).replace(" ", "_")
    phrase_video = os.path.join(VIDEO_FOLDER, f"{phrase}.mp4")
    if os.path.exists(phrase_video):
        print(f"🎬 Showing sign for phrase: {phrase}")
        play_video(phrase_video)
        return

    # Word-by-word fallback
    words = phrase.split("_")
    for word in words:
        video_path = os.path.join(VIDEO_FOLDER, f"{word}.mp4")
        if os.path.exists(video_path):
            print(f"🎬 Showing sign for: {word}")
            play_video(video_path)
        else:
            print(f"⚠️ No sign video found for: {word}")
            fallback_video = os.path.join(VIDEO_FOLDER, "not_found.mp4")
            if os.path.exists(fallback_video):
                play_video(fallback_video)

# Thread wrapper to prevent GUI freeze during recording or video playing
def threaded(func):
    def wrapper(*args, **kwargs):
        threading.Thread(target=func, args=args, kwargs=kwargs).start()
    return wrapper

# GUI functions
@threaded
def record_and_play():
    record_audio()
    text = transcribe_audio()
    entry_text.set(text)  # update input box with transcript
    play_sign_language(text)

@threaded
def play_from_input():
    text = entry_text.get()
    play_sign_language(text)

def on_key_press(event):
    if event.char == 'r':
        record_and_play()
    elif event.char == 'p':
        play_from_input()

# Tkinter GUI setup
root = tk.Tk()
root.title("Speech to Sign Language Translator")

frame = tk.Frame(root, padx=10, pady=10)
frame.pack()

label = tk.Label(frame, text="Enter text or record speech:")
label.grid(row=0, column=0, columnspan=2, sticky="w")

entry_text = tk.StringVar()
entry = tk.Entry(frame, textvariable=entry_text, width=50)
entry.grid(row=1, column=0, columnspan=2, pady=5)

record_button = tk.Button(frame, text="🎙️ Record & Play (R)", command=record_and_play, width=20)
record_button.grid(row=2, column=0, pady=10)

play_button = tk.Button(frame, text="▶️ Play Text (P)", command=play_from_input, width=20)
play_button.grid(row=2, column=1, pady=10)

quit_button = tk.Button(frame, text="Quit", command=root.destroy, width=20)
quit_button.grid(row=3, column=0, columnspan=2, pady=10)

root.bind('<Key>', on_key_press)

root.mainloop()
