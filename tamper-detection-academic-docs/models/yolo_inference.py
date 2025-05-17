# Script for loading and running YOLOv5/YOLTv8
import torch
import os
import cv2

# Load YOLO model
def load_model(weights_path=None):
    try:
        if weights_path:
            model = torch.hub.load('ultralytics/yolov5', 'custom', path=weights_path)
        else:
            model = torch.hub.load('ultralytics/yolov5', 'yolov5s')  # use small model by default
        return model
    except Exception as e:
        print(f"❌ Failed to load model: {e}")
        return None

# Run inference on a single image
def detect_objects(model, image_path, conf_threshold=0.3):
    if not model:
        print("⚠️ Model is not loaded.")
        return []

    results = model(image_path)
    results = results.pandas().xyxy[0]  # get predictions in Pandas DataFrame format

    # Filter by confidence threshold
    detections = results[results['confidence'] >= conf_threshold]
    return detections

# Draw results on image
def draw_detections(image_path, detections, output_path=None):
    image = cv2.imread(image_path)
    for _, row in detections.iterrows():
        x1, y1, x2, y2, conf, cls = int(row['xmin']), int(row['ymin']), int(row['xmax']), int(row['ymax']), row['confidence'], row['name']
        cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 2)
        label = f"{cls} ({conf:.2f})"
        cv2.putText(image, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (36, 255, 12), 1)

    if output_path:
        cv2.imwrite(output_path, image)
    return image
