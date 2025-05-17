"""The script processes JSONL annotation files describing images and their bounding boxes, 
loads corresponding original images, modifies (or "tampers with") the bounding boxes 
on the images by covering them with white rectangles and adding "Fake" labels, 
then saves these tampered images in a new folder"""

import os
import json
import cv2
from urllib.parse import urlparse
import hashlib

# Paths
ANNOTATION_PATH = r"C:\Users\Bezawada\Downloads\tamper-detection-academic-docs\tamper-detection-academic-docs\data\annotations\_annotations.train.jsonl"
TEMPLATE_DIR = "data/templates"
SAMPLES_DIR = "data/samples"
os.makedirs(SAMPLES_DIR, exist_ok=True)

def tamper_with_boxes(image, annotations):
    for ann in annotations:
        x, y, w, h = ann['x'], ann['y'], ann['width'], ann['height']
        class_name = ann['class']
        x1 = int(x - w / 2)
        y1 = int(y - h / 2)
        x2 = int(x + w / 2)
        y2 = int(y + h / 2)
        cv2.rectangle(image, (x1, y1), (x2, y2), (255, 255, 255), -1)
        cv2.putText(image, f"Fake {class_name}", (x1 + 5, y1 + 25),
                    fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                    fontScale=0.7, color=(0, 0, 0), thickness=2)
    return image

with open(ANNOTATION_PATH, 'r') as file:
    for line in file:
        data = json.loads(line.strip())
        try:
            messages = data["messages"]
            user_content = next(m["content"] for m in messages if m["role"] == "user" and isinstance(m["content"], list))
            img_url = user_content[0]["image_url"]["url"]

            url_hash = hashlib.md5(img_url.encode()).hexdigest()[:8]
            img_name = f"{url_hash}_transformed.jpg"

            template_path = os.path.join(TEMPLATE_DIR, img_name)
            tampered_path = os.path.join(SAMPLES_DIR, f"tampered_{img_name}")

            if not os.path.exists(template_path):
                print(f" Missing original image: {template_path}")
                continue

            img = cv2.imread(template_path)
            annotations = data.get("annotations", [])
            tampered = tamper_with_boxes(img, annotations)
            cv2.imwrite(tampered_path, tampered)
            print(f" Tampered saved: {tampered_path}")

        except Exception as e:
            print(f" Skipped due to error: {e}")

print(" All tampered samples created.")
