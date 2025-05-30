import React, { useState } from "react";

function TextToVoice() {
  const [text, setText] = useState("");
  const [speaking, setSpeaking] = useState(false);

  const speakText = () => {
    if (!text.trim()) return;

    const utterance = new SpeechSynthesisUtterance(text);
    utterance.onstart = () => setSpeaking(true);
    utterance.onend = () => setSpeaking(false);
    window.speechSynthesis.speak(utterance);
  };

  return (
    <div
      className="min-h-screen bg-cover bg-center relative flex items-center justify-center p-6"
      style={{ backgroundImage: "url('/bg-text-voice.png')" }} // <-- Use your image path
    >
      {/* Optional yellow overlay */}
      <div className="absolute inset-0 bg-yellow-100 bg-opacity-30 backdrop-blur-sm"></div>

      {/* Left animated lines */}
      <div className="absolute left-6 top-1/2 transform -translate-y-1/2 space-y-6 z-10">
        {[...Array(4)].map((_, i) => (
          <div key={i} className="animated-line"></div>
        ))}
      </div>

      {/* Right animated lines */}
      <div className="absolute right-6 top-1/2 transform -translate-y-1/2 space-y-6 z-10">
        {[...Array(4)].map((_, i) => (
          <div key={i} className="animated-line"></div>
        ))}
      </div>

      {/* Content */}
      <div className="relative z-20 w-full max-w-3xl bg-[#fff7dd]/80 backdrop-blur-xl border border-yellow-900 rounded-3xl p-10 shadow-2xl text-center animate-fade-in">
        <h1
          className="text-5xl font-bold text-yellow-600 mb-6"
          style={{ fontFamily: "'Dancing Script', cursive" }}
        >
          Text to Voice
        </h1>

        <textarea
          rows="5"
          placeholder="Type your message here..."
          className="w-full p-5 rounded-xl border border-yellow-300 text-gray-800 focus:outline-none focus:ring-2 focus:ring-yellow-500 shadow-inner resize-none transition"
          value={text}
          onChange={(e) => setText(e.target.value)}
        ></textarea>

        <button
          onClick={speakText}
          className="mt-6 bg-yellow-400 hover:bg-yellow-500 text-white font-bold px-10 py-3 rounded-full shadow-xl transition-transform duration-300 hover:scale-105"
        >
          🔊 Speak Now
        </button>

        {speaking && (
          <div className="mt-6 animate-pulse text-yellow-700 text-2xl font-semibold tracking-wide">
            🗣️ Speaking...
          </div>
        )}
      </div>
    </div>
  );
}

export default TextToVoice;
