# Logic for tamper detection using visual features
"""SSIM (Structural Similarity Index Measure) is a metric that compares two images 
based on how similar their structures, brightness, and contrast are, mimicking human visual perception.

It outputs a score between -1 and 1, where 1 means identical images.

Unlike simple pixel difference metrics, SSIM focuses on perceived image quality.

Commonly used for image quality assessment and detecting subtle changes or tampering."""

import cv2
from skimage.metrics import structural_similarity as ssim
import numpy as np

def compare_images_ssim(image1_path, image2_path):
    img1 = cv2.imread(image1_path, cv2.IMREAD_GRAYSCALE)
    img2 = cv2.imread(image2_path, cv2.IMREAD_GRAYSCALE)

    if img1.shape != img2.shape:
        img2 = cv2.resize(img2, (img1.shape[1], img1.shape[0]))

    score, diff = ssim(img1, img2, full=True)
    diff = (diff * 255).astype("uint8")

    print(f"SSIM score between images: {score:.4f}")
    return score, diff
