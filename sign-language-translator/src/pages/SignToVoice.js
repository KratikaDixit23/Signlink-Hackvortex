import React, { useState } from "react";
import axios from "axios";

const SignToVoice = () => {
  const [output, setOutput] = useState("");

  const handleStart = async () => {
    try {
      const response = await axios.get("http://localhost:5002/api/sign-to-speech");
      setOutput(response.data.output);
    } catch (error) {
      console.error("Error recognizing sign:", error);
      setOutput("Failed to detect sign.");
    }
  };

  return (
    <div className="min-h-screen bg-purple-100 flex flex-col items-center justify-center p-4">
      <h1 className="text-3xl font-bold mb-6 text-purple-800">Sign to Voice</h1>
      <button
        onClick={handleStart}
        className="bg-purple-600 text-white px-6 py-3 rounded-lg shadow-md hover:bg-purple-700"
      >
        Start Detection
      </button>
      {output && <p className="mt-4 text-lg text-purple-900">Detected: {output}</p>}
    </div>
  );
};

export default SignToVoice;