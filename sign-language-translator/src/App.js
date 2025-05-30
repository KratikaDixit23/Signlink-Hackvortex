import React from "react";
import { BrowserRouter as Router, Routes, Route, Link } from "react-router-dom";
import Communication from "./pages/Communication";
import VoiceToText from "./pages/VoiceToText";
import TextToVoice from "./pages/TextToVoice";
import VoiceToSign from "./pages/VoiceToSign";
import TextToSign from "./pages/TextToSign";
import SignToVoice from "./pages/SignToVoice";
import SignToText from "./pages/SignToText";

function Home() {
  return (
    <div
      className="min-h-screen bg-cover bg-center relative"
      style={{ backgroundImage: "url('/bg3.jpg')" }}
    >
      {/* Dark overlay */}
      <div className="absolute inset-0 bg-black bg-opacity-10"></div>

      {/* Content Layer */}
      <div className="relative z-10 flex flex-col md:flex-row items-center justify-center px-4 py-16">
        {/* Left: Title + Button */}
        <div className="flex flex-col items-center md:items-start text-center md:text-left md:mr-12">
          <h1
            className="text-5xl md:text-6xl font-extrabold text-purple-800 mb-16"
            style={{ fontFamily: "'Dancing Script', cursive", marginTop: '2in' }}
          >
            Hear the Silence
          </h1>

          <div className="bg-white bg-opacity-80 p-2 rounded-2xl shadow-2xl text-center w-full max-w-md">
            <div className="space-y-6">
              <Link to="/communication">
                <button className="bg-green-600 hover:bg-green-700 text-white font-bold px-6 py-3 rounded-2xl shadow-lg w-full">
                  🎙️ Start Communication 🖐️
                </button>
              </Link>
            </div>
          </div>
        </div>

        {/* Right: GIF */}
        <div className="hidden md:flex items-center justify-center" style={{ marginTop: "120px" }}>
          <img
            src="/am.gif"
            alt="Animated illustration"
            className="w-80 h-auto rounded-xl shadow-xl"
          />
        </div>
      </div>
    </div>
  );
}

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/communication" element={<Communication />} /> 
        <Route path="/voice-to-text" element={<VoiceToText />} />
        <Route path="/text-to-voice" element={<TextToVoice />} />
        <Route path="/voice-to-sign" element={<VoiceToSign />} />
        <Route path="/text-to-sign" element={<TextToSign />} />
        <Route path="/sign-to-voice" element={<SignToVoice />} />
        <Route path="/sign-to-text" element={<SignToText />} />
      </Routes>
    </Router>
  );
}

export default App;
