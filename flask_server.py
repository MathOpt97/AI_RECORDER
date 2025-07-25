from flask import Flask, request
import os

app = Flask(__name__)
UPLOAD_FOLDER = "uploaded_videos"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/upload', methods=['POST'])  # ✅ Must match exactly
def upload_video():
    video = request.files.get("video")
    if not video:
        return "No video provided", 400

    filepath = os.path.join(UPLOAD_FOLDER, video.filename)
    video.save(filepath)
    return f"Video saved to {filepath}", 200

if __name__ == '__main__':
    app.run(host="127.0.0.1", port=5000)
