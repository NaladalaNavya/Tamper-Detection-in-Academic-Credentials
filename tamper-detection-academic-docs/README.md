# 🕵️‍♂️ Tamper Detection in Academic Documents

A computer vision and OCR-powered pipeline for detecting tampering in academic documents such as certificates, mark sheets, and transcripts. This system compares clean document templates with synthetically tampered versions and flags suspicious alterations based on image structure and text content.

---

## 📌 Key Features

- ✅ **Automated image ingestion** from annotation `.jsonl`
- ✅ **Simulates realistic tampering** using bounding boxes with text overlays or erasure
- ✅ **Performs OCR** using Tesseract to extract visible content
- ✅ **Measures structural similarity** using SSIM between template and tampered images
- ✅ **Flags textual differences** using OCR-based string similarity
- ✅ **Generates a detailed CSV report** with scores and tampering flags
- ✅ Modular design: templates, tampering, comparison, and reporting all decoupled

---

## 🧠 Technology Stack

- Python 3.x
- OpenCV (`cv2`) — image manipulation
- pytesseract — OCR engine (Tesseract)
- scikit-image — SSIM comparison
- pandas — tabular report generation
- matplotlib — optional visual inspection
- YOLOv5 (optional future model for real detection tasks)

---

## 🧪 Tampering Simulation

Tampering is synthetically introduced by:

- Drawing over bounding boxes with fake text or whiteout
- Optionally altering more regions for greater SSIM variation
- Enabling easy customization to simulate real-world forgery techniques

---

## 📊 Output Report

After running the pipeline, you'll get:

📄 `outputs/reports/exploration_results.csv`

| image                  | ssim_score | text_similarity | is_suspicious | template_text       | tampered_text        |
| ---------------------- | ---------- | --------------- | ------------- | ------------------- | -------------------- |
| `doc1_transformed.jpg` | 0.9975     | 0.96            | False         | John Doe, ID 12345  | John Doe, ID 12345   |
| `doc2_transformed.jpg` | 0.9721     | 0.89            | **True**      | Grade: A, June 2021 | Grade: A+, June 2022 |

A row is **flagged as suspicious** if:

- `ssim_score < 0.98` or
- `text_similarity < 0.95`

---

## ▶️ How to Run

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```
