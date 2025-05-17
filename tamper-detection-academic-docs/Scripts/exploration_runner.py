import cv2
import sys
from glob import glob
import os

# Add project root to sys.path before importing project modules
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from src.ocr_utils import extract_text
from src.detect_anomalies import compare_images_ssim
from utils.image_utils import show_side_by_side  # Optional for debugging
import logging

# Setup logger
from utils.logger import setup_logger
logger = setup_logger(name="exploration", log_file="outputs/logs/exploration.log")

# Collect all image pairs
template_paths = sorted(glob("data/templates/*.jpg"))
tampered_paths = sorted(glob("data/samples/tampered_*.jpg"))

results = []

for template_img in template_paths:
    basename = os.path.basename(template_img)
    tampered_img = f"data/samples/tampered_{basename}"

    if not os.path.exists(tampered_img):
        logger.warning(f"Missing tampered version for {basename}")
        continue

    logger.info(f"Comparing: {basename}")

    # SSIM Score
    """SSIM is a perceptual metric that quantifies the similarity between two images.
It's designed to mimic how humans perceive image quality — going beyond simple pixel-wise differences."""

    score, _ = compare_images_ssim(template_img, tampered_img)
    logger.info(f"SSIM Score: {score:.4f}")

    # OCR Text
    text_template = extract_text(template_img)
    text_tampered = extract_text(tampered_img)

    logger.info("Template Text:")
    logger.info(text_template)

    logger.info("Tampered Text:")
    logger.info(text_tampered)

    results.append({
        "image": basename,
        "ssim": score,
        "template_text": text_template,
        "tampered_text": text_tampered
    })

# Optionally: save results to CSV
import pandas as pd
df = pd.DataFrame(results)
df.to_csv("outputs/reports/exploration_results.csv", index=False)
logger.info("Results saved to outputs/reports/exploration_results.csv")
