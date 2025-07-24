from ultralytics import YOLO

model = YOLO("yolo11n.pt")

results = model.predict(source="0", conf=0.3, verbose=False, stream=True)  # use threshold menor aqui

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
            print(f"Detected {class_name} with confidence {confidence}")
            break