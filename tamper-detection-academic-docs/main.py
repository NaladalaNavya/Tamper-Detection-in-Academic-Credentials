import sys
import os
sys.path.append(os.path.abspath('.'))

import difflib
import pandas as pd
from glob import glob
from src.ocr_utils import extract_text
from src.detect_anomalies import compare_images_ssim
from utils.logger import setup_logger

# Initialize logger
logger = setup_logger("main", "outputs/logs/main.log")

# Step 1: Download template images
def run_step1_download():
    logger.info("🚀 Step 1: Downloading template images")
    os.system("python Templates_create.py")

# Step 2: Generate tampered samples using annotations
def run_step2_generate_tampered():
    logger.info("🚀 Step 2: Creating tampered images")
    os.system("python samples_create.py")

# Step 3: SSIM + OCR Comparison
def run_step3_compare_and_report():
    logger.info("🚀 Step 3: Comparing templates and tampered images")
    results = []
    ssim_threshold = 0.98
    ocr_threshold = 0.95

    template_paths = sorted(glob("data/templates/*.jpg"))

    for template_img in template_paths:
        basename = os.path.basename(template_img)
        tampered_img = f"data/samples/tampered_{basename}"

        if not os.path.exists(tampered_img):
            logger.warning(f"⚠️ Missing tampered image for {basename}")
            continue

        try:
            # SSIM comparison
            ssim_score, _ = compare_images_ssim(template_img, tampered_img)

            # OCR comparison
            text_template = extract_text(template_img)
            text_tampered = extract_text(tampered_img)
            ocr_similarity = difflib.SequenceMatcher(None, text_template, text_tampered).ratio()

            is_suspicious = ssim_score < ssim_threshold or ocr_similarity < ocr_threshold

            results.append({
                "image": basename,
                "ssim_score": round(ssim_score, 4),
                "text_similarity": round(ocr_similarity, 4),
                "is_suspicious": is_suspicious,
                "template_text": text_template,
                "tampered_text": text_tampered
            })

            marker = "🚨" if is_suspicious else "✅"
            logger.info(f"{marker} {basename} | SSIM: {ssim_score:.4f} | OCR: {ocr_similarity:.4f}")

        except Exception as e:
            logger.error(f"❌ Error processing {basename}: {e}")

    # Save results
    os.makedirs("outputs/reports", exist_ok=True)
    df = pd.DataFrame(results)
    df.to_csv("outputs/reports/exploration_results.csv", index=False)
    logger.info("📄 Report saved to outputs/reports/exploration_results.csv")

# Entry point
def main():
    logger.info("🎯 Tamper Detection Pipeline Started")
    run_step1_download()
    run_step2_generate_tampered()
    run_step3_compare_and_report()
    logger.info("✅ Pipeline completed")

if __name__ == "__main__":
    main()
