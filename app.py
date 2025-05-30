from flask import Flask, request, jsonify, send_from_directory
import subprocess
import sys
import os

app = Flask(__name__, static_folder='static')

@app.route('/api/speech-to-sign', methods=['GET'])
def speech_to_sign():
    try:
        # Run speech_to_sign.py with 'speech' argument
        result = subprocess.run(
            [sys.executable, 'speech_to_sign.py', 'speech'],
            capture_output=True,
            text=True
        )
        output_lines = result.stdout.strip().split('\n')
        video_line = next((line for line in output_lines if 'Playing video:' in line), None)
        transcript_line = next((line for line in output_lines if 'Transcript:' in line), None)

        if video_line:
            video_filename = video_line.split('Playing video:')[-1].strip()
            transcript = transcript_line.split('Transcript:')[-1].strip() if transcript_line else ""
            return jsonify({
                'video_filename': video_filename,
                'transcript': transcript
            })
        else:
            return jsonify({'error': 'No video generated'}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/text-to-sign', methods=['POST'])
def text_to_sign():
    try:
        data = request.get_json()
        input_text = data.get('text', '')

        result = subprocess.run(
            [sys.executable, 'speech_to_sign.py', 'text', input_text],
            capture_output=True,
            text=True
        )

        output_lines = result.stdout.strip().split('\n')
        video_line = next((line for line in output_lines if 'Playing video:' in line), None)

        if video_line:
            video_filename = video_line.split('Playing video:')[-1].strip()
            return jsonify({'video_filename': video_filename})
        else:
            return jsonify({'error': 'No video generated'}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Serve videos from static/videos folder
@app.route('/static/videos/<path:filename>')
def serve_video(filename):
    return send_from_directory(os.path.join(app.static_folder, 'videos'), filename)

if __name__ == '__main__':
    app.run(port=5001, debug=True)
