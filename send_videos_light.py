import requests
import os
import time

SERVER_URL = "http://127.0.0.1:5000/upload"  # ✅ Must match Flask route exactly
VIDEO_DIR = "videos"
DETECTION_DIR = "detection_logs"
video_id = 1
MAX_VIDEOS = 10

def video_send(dir, id, server_url):
    filepath = os.path.join(dir, f"video_{id}.mp4")
    if not os.path.exists(filepath):
        print(f"Video {filepath} não encontrado.")
        return

    with open(filepath, "rb") as f:
        files = {"video": (f"video_{id}.mp4", f)}
        response = requests.post(server_url, files=files)
        print(f"{filepath} -> {response.status_code}: {response.text}")

while True:
    # Se caso não existe video e json correspondente, refaça a verificação
    if not (os.path.exists(VIDEO_DIR+'/'+f"video_{video_id}.mp4") and os.path.exists(DETECTION_DIR+'/'+f"video_{video_id}.json")):
        print(f'Nenhum video encontrado, aguardando ...')
        time.sleep(5)
    else:
        print(f'Enviando video {VIDEO_DIR}/video_{video_id}.mp4 para {SERVER_URL}')
        video_id = video_id + 1
        if video_id > MAX_VIDEOS:
            video_id = 1
        video_send(VIDEO_DIR, video_id, SERVER_URL)
