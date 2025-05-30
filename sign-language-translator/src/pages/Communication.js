import React from "react";
import { Link } from "react-router-dom";

const features = [
  { name: "Text to Sign", image: "/icons/text-to-sign.png", route: "/text-to-sign" },
  { name: "Voice to Sign", image: "/icons/voice-to-sign.png", route: "/voice-to-sign" },
  { name: "Sign to Voice", image: "/icons/sign-to-voice.png", route: "/sign-to-voice" },
  { name: "Sign to Text", image: "/icons/sign-to-text.png", route: "/sign-to-text" },
  { name: "Voice to Text", image: "/icons/voice-to-text.png", route: "/voice-to-text" },
  { name: "Text to Voice", image: "/icons/text-to-voice.png", route: "/text-to-voice" },
];

function Communication() {
  return (
    <div className="min-h-screen bg-gradient-to-r from-purple-100 to-indigo-200 p-10">
      <h1
        className="text-5xl font-extrabold text-center text-purple-800 mb-14"
        style={{ fontFamily: "'Dancing Script', cursive" }}
      >
        Select a Communication Mode
      </h1>

      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-12 max-w-7xl mx-auto">
        {features.map((feature, index) => (
          <div
            key={index}
            className="bg-white rounded-3xl shadow-2xl p-1 flex flex-col items-center transition-all duration-300 transform hover:scale-105 hover:bg-purple-100 hover:shadow-purple-400"
          >
            <img
              src={feature.image}
              alt={feature.name}
              className="w-40 h-40 object-contain mb-6"
            />
            <Link to={feature.route}>
              <button className="mt-2 bg-purple-600 hover:bg-purple-700 text-white text-lg px-8 py-3 rounded-2xl font-semibold shadow-md">
                {feature.name}
              </button>
            </Link>
          </div>
        ))}
      </div>
    </div>
  );
}

export default Communication;
