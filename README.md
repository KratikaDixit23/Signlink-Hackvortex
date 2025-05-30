# SignLink: Real-Time Sign Language and Speech Translator

---

## 🧠 Description

**SignLink** is a complete, bi-directional communication system that bridges the gap between hearing/speech-impaired individuals and the wider community. It performs real-time translation between **spoken language, text, and Indian Sign Language (ISL)** using machine learning, computer vision, and browser-based voice technologies.

With a clean and responsive **React + Tailwind CSS frontend** and a powerful **Python Flask backend**, SignLink is designed to be inclusive, intelligent, and production-ready.

---

## 🔁 Key Modules

### ✅ Module 1 – Voice to Sign Language
- Transcribes speech to text using **OpenAI Whisper**.
- Plays the corresponding **Indian Sign Language gesture video**.
- Integrated into the React UI for seamless experience.

### ✅ Module 2 – Text to Sign Language
- Converts **typed text input** into **ISL gesture videos**.
- Provides a visual sign translation for non-verbal communication.

### ✅ Module 3 – Sign Language to Text
- Uses **MediaPipe** for keypoint extraction and a trained ML model to recognize **dynamic signs** via webcam.
- Displays **real-time text output** for recognized gestures.

### ✅ Module 4 – Sign Language to Voice
- Extends Module 3 by converting the recognized signs into **spoken output** using **pyttsx3**.
- Enables fully hands-free sign-to-voice communication.

### ✅ Module 5 – Voice to Text (React + JavaScript)
- Captures voice input in-browser using the **Web Speech API**.
- Displays real-time **text transcription** in the React UI.

### ✅ Module 6 – Text to Voice (React + JavaScript)
- Uses the browser’s **SpeechSynthesis API** to convert typed input into **spoken words**.
- Allows non-verbal users to “speak” via text instantly.

---

## 🌐 Fullstack Integration

- All modules are fully integrated with **React frontend** and **Flask backend**.
- Routes like `/communication`, `/voice-to-text`, and `/text-to-voice` are properly linked with backend logic.
- Flask API endpoints handle voice/sign input, and React components communicate using `fetch` or `axios`.

---

## ⚙️ Tech Stack

- **Frontend:** React.js, Tailwind CSS, JavaScript
- **Backend:** Python, Flask
- **ML & Vision:** TensorFlow/Keras, MediaPipe
- **Speech Tools:** OpenAI Whisper, Web Speech API, pyttsx3, SpeechSynthesis API
- **Dataset:** Indian Sign Language Video Dataset (Kaggle)

---

## 🎯 Use Cases

- Assistive communication for the deaf, hard-of-hearing, and non-verbal individuals
- Real-time translation in classrooms, hospitals, public services
- Inclusive digital platforms that support multi-modal communication

---

## ✅ Project Status

✔️ All modules (1–6) fully completed  
✔️ All backend and frontend components integrated  
✔️ Fully functional system tested end-to-end  
🎉 **SignLink is production-ready**

---

## 📂 Dataset Link

[Indian Sign Language Video Dataset on Kaggle](https://www.kaggle.com/datasets/prasadshet/indian-sign-language-video-dataset?resource=download)

---

## 🎥 Demo Video

[SignLink Demo Video](https://drive.google.com/file/d/1jdrBztRx63q4HsFcvoGdza0xVyADGD_3/view?usp=sharing)

---

## 🚀 Future Scopes

- Expand vocabulary by adding more sign language gestures and phrases  
- Add multilingual support for other spoken languages and their respective sign languages  
- Implement a mobile app for accessibility on smartphones and tablets  
- Enhance model accuracy and speed using state-of-the-art ML architectures  
- Integrate with video conferencing platforms for live communication assistance  
- Build a user-friendly dashboard for personalizing sign language learning and usage  

---

*Thank you for checking out SignLink! Feel free to contribute or raise issues.*
