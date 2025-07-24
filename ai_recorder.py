import cv2
import time
import os
from ultralytics import YOLO
import json

# Settings
STREAM_URL = 0
SAVE_FOLDER = "videos"
SAVE_DETECTIONS_FOLDER = "detection_logs"
RECORD_SECONDS = 30
RECORD_SECONDS_AFTER_DETECTION = 20
MAX_VIDEOS = 4
record_extend = 0
video_id = 0
frame_counter = 0
frame_of_detection = 0
write_json = False

# Make sure folders exist
os.makedirs(SAVE_FOLDER, exist_ok=True)
os.makedirs(SAVE_DETECTIONS_FOLDER, exist_ok=True)

# Initialize video stream
cap = cv2.VideoCapture(STREAM_URL)

if not cap.isOpened():
    print("Falha ao abrir a câmera ou stream.")
    exit()

# Get stream properties
fps = cap.get(cv2.CAP_PROP_FPS)
if fps == 0 or fps is None:
    fps = 20.0  # fallback
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
frame_size = (width, height)
fourcc = cv2.VideoWriter_fourcc(*'mp4v')

# Load YOLO model
model = YOLO("yolo11n.pt")

try:
    while True:
        video_id = (video_id % MAX_VIDEOS) + 1
        filename = os.path.join(SAVE_FOLDER, f"video_{video_id}.mp4")
        out = cv2.VideoWriter(filename, fourcc, fps, frame_size)

        start = time.time()
        frame_counter = 0
        write_json = False
        frame_of_detection = 0
        record_extend = 0
        stop_ai = False

        print(f"Iniciando gravação: {filename}")

        while time.time() - start < (RECORD_SECONDS + record_extend):
            _, frame = cap.read()

            frame_counter += 1

            print(f"Frame {frame_counter}")

            if not stop_ai:
                # Run YOLO detection
                results = model.predict(frame, conf=0.3, verbose=False, stream = True)

                for result in results:
                    # Access bounding box information
                    boxes = result.boxes
                    for box in boxes:
                        # Get class ID and confidence
                        class_id = int(box.cls.item())
                        confidence = round(box.conf.item(), 2)
                        # Get class name using the model's names attribute
                        class_name = model.names[class_id]
                        if class_name == "person" and confidence >= 0.5:
                            print(f"Pessoa detectada com confiança {confidence:.2f}")
                            record_extend = RECORD_SECONDS_AFTER_DETECTION
                            frame_of_detection = frame_counter
                            write_json = True
                            stop_ai = True
                            break

            out.write(frame)

        out.release()
        print(f"Vídeo salvo: {filename}")

        if write_json:
            detection_dict = {
                "frame_of_detection": frame_of_detection,
                "video_id": video_id,
                "total_frames": frame_counter
            }
            json_path = os.path.join(SAVE_DETECTIONS_FOLDER, f"video_{video_id}.json")
            with open(json_path, "a") as f:
                json.dump(detection_dict, f)
                #f.write("\n")
            print(f"Detecção salva em: {json_path}")

except KeyboardInterrupt:
    print("Parado pelo usuário.")

cap.release()
