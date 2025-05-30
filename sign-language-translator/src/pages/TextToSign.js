import React, { useState } from "react";
import axios from "axios";

const TextToSign = () => {
  const [inputText, setInputText] = useState("");
  const [videoFilename, setVideoFilename] = useState(null);
  const [message, setMessage] = useState("");

  const handleTextToSign = async () => {
    if (!inputText.trim()) {
      setMessage("Please enter some text");
      return;
    }
    setMessage("Processing...");
    try {
      const res = await axios.post("http://localhost:5001/api/text-to-sign", { text: inputText });
      if (res.data && res.data.video_filename) {
        setVideoFilename(res.data.video_filename);
        setMessage("✅ Video generated");
      } else {
        setMessage("❌ No valid response from server");
      }
    } catch (err) {
      console.error("Error:", err);
      setMessage("❌ Error occurred");
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-purple-700 to-purple-400 text-white flex flex-col items-center justify-center px-4">
      <div className="w-full max-w-2xl p-8 bg-purple-800 rounded-2xl shadow-lg text-center">
        <h1 className="text-3xl font-bold mb-6">Text to Sign Language</h1>
        <input
          type="text"
          value={inputText}
          onChange={e => setInputText(e.target.value)}
          className="w-full p-2 mb-4 rounded text-purple-900"
          placeholder="Type text here"
        />
        <button
          onClick={handleTextToSign}
          className="bg-white text-purple-700 font-semibold py-2 px-6 rounded-lg hover:bg-purple-200 transition-colors duration-300"
        >
          Convert to Sign
        </button>

        {message && (
          <p className="mt-4 text-sm bg-purple-700 p-2 rounded-lg">{message}</p>
        )}

        {videoFilename && (
          <div className="mt-6">
            <video
              src={`http://localhost:5001/static/videos/${videoFilename}`}
              controls
              autoPlay
              className="rounded-xl shadow-lg w-full"
            />
          </div>
        )}
      </div>
    </div>
  );
};

export default TextToSign;
