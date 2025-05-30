import React, { useState, useEffect, useRef } from "react";

function VoiceToText() {
  const [listening, setListening] = useState(false);
  const [transcript, setTranscript] = useState("");
  const [bubbles, setBubbles] = useState([]);
  const recognitionRef = useRef(null);

  useEffect(() => {
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    if (!SpeechRecognition) {
      alert("Your browser does not support Speech Recognition.");
      return;
    }

    const recognition = new SpeechRecognition();
    recognition.continuous = false;
    recognition.interimResults = true;
    recognition.lang = "en-US";

    recognition.onstart = () => setListening(true);
    recognition.onend = () => setListening(false);

    recognition.onresult = (event) => {
      let interimTranscript = "";
      for (let i = event.resultIndex; i < event.results.length; i++) {
        const transcriptSegment = event.results[i][0].transcript;
        if (event.results[i].isFinal) {
          setTranscript(prev => prev + transcriptSegment + " ");
        } else {
          interimTranscript += transcriptSegment;
        }
        createBubble();
        createBubble();
      }
    };

    recognitionRef.current = recognition;
  }, []);

  const toggleListening = () => {
    if (listening) {
      recognitionRef.current.stop();
    } else {
      recognitionRef.current.start();
    }
  };

  const createBubble = () => {
    const id = Date.now() + Math.random();
    const left = Math.random() * 90;
    const size = Math.random() * 60 + 40;
    setBubbles(prev => [...prev, { id, left, size }]);
    setTimeout(() => {
      setBubbles(prev => prev.filter(b => b.id !== id));
    }, 2000);
  };

  return (
    <div
      className="min-h-screen bg-cover bg-center relative flex flex-col items-center justify-center p-6 overflow-hidden"
      style={{ backgroundImage: "url('/bg-voicetotext.png')" }} // <-- set your background image path
    >
      {/* Optional: semi-transparent overlay */}
      <div className="absolute inset-0 bg-white bg-opacity-20 backdrop-blur-md"></div>

      {/* Bubbles */}
      {bubbles.map(bubble => (
        <div
          key={bubble.id}
          className="bubble"
          style={{
            left: `${bubble.left}%`,
            width: `${bubble.size}px`,
            height: `${bubble.size}px`
          }}
        />
      ))}

      {/* Main content */}
      <div className="relative z-10 text-center">
        <h1
          className="text-5xl font-extrabold text-purple-800 mb-10 drop-shadow-lg"
          style={{ fontFamily: "'Dancing Script', cursive" }}
        >
          Voice to Text Converter
        </h1>

        <button
          onClick={toggleListening}
          className={`px-10 py-4 rounded-full font-bold text-lg shadow-2xl transition-all duration-300 ${
            listening
              ? "bg-red-500 hover:bg-red-600 text-white animate-pulse"
              : "bg-green-600 hover:bg-green-700 text-white"
          }`}
        >
          {listening ? "🎙️ Listening... Tap to Stop" : "🟢 Start Listening"}
        </button>

        <div className="mt-10 w-full max-w-3xl bg-white/70 backdrop-blur-lg p-6 rounded-xl shadow-2xl text-gray-800 text-lg min-h-[200px] border border-purple-300 transition duration-500">
          <span className="whitespace-pre-line animate-fade-in">
            {transcript || "🎧 Waiting for your voice..."}
          </span>
        </div>
      </div>
    </div>
  );
}

export default VoiceToText;
