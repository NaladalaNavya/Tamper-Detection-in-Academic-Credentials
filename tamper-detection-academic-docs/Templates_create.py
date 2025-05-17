"""This script downloads images from URLs listed in a JSONL annotation file. 
It saves each image locally with a unique filename derived from a hash of the image URL. 
It avoids duplicate downloads by tracking already downloaded files."""

import os
import json
import urllib.request
from urllib.parse import urlparse
import hashlib

# Paths
ANNOTATION_PATH = r"C:\Users\Bezawada\Downloads\tamper-detection-academic-docs\tamper-detection-academic-docs\data\annotations\_annotations.train.jsonl"
TEMPLATES_DIR = "data/templates"
os.makedirs(TEMPLATES_DIR, exist_ok=True)

downloaded = set()

with open(ANNOTATION_PATH, 'r') as file:
    for line in file:
        data = json.loads(line.strip())
        try:
            # Extract the image URL
            messages = data["messages"]
            user_content = next(m["content"] for m in messages if m["role"] == "user" and isinstance(m["content"], list))
            img_url = user_content[0]["image_url"]["url"]

            # Use a hash of the URL as filename to make it unique
            url_hash = hashlib.md5(img_url.encode()).hexdigest()[:8]
            img_name = f"{url_hash}_transformed.jpg"

            if img_name in downloaded:
                continue

            save_path = os.path.join(TEMPLATES_DIR, img_name)
            print(f"=> Attempting download: {img_url} -> {img_name}")


            urllib.request.urlretrieve(img_url, save_path)
            print(f"=>  Downloaded: {img_name}")
            downloaded.add(img_name)

        except Exception as e:
            print(f"=>  Skipped due to error: {e}")

print(f"=>  Total downloaded: {len(downloaded)}")
