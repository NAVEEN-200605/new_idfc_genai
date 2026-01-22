import os
import json
import cv2
from tqdm import tqdm

from ocr.ocr_engine import run_ocr
from layout.layout_grouping import group_by_layout
from extraction.field_extraction import extract_all_fields
from vision.detect_signature import detect_signature
from vision.detect_stamp import detect_stamp
from confidence.confidence import compute_confidence
from utils.metrics import start_timer, end_timer, estimate_cost

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IMAGE_DIR = os.path.join(BASE_DIR, "data", "images")
OUTPUT_FILE = os.path.join(BASE_DIR, "outputs", "text_extraction_results.json")

def main(limit=3):
    results = []
    images = sorted(os.listdir(IMAGE_DIR))[:limit]

    for idx, img in enumerate(tqdm(images)):
        start_time = start_timer()
        img_path = os.path.join(IMAGE_DIR, img)
        doc_id = f"invoice_{idx+1:03d}"

        try:
            image = cv2.imread(img_path)
            h, _, _ = image.shape

            # 🔹 OCR
            ocr_data = run_ocr(img_path)
            avg_ocr_conf = (
                sum(i["confidence"] for i in ocr_data) / len(ocr_data)
                if ocr_data else 0.0
            )

            # 🔹 Layout + Field Extraction
            layout = group_by_layout(ocr_data, h)
            fields, _ = extract_all_fields(layout)

            # 🔹 Vision Checks
            signature = detect_signature(img_path)
            stamp = detect_stamp(img_path)

            # 🔹 Confidence
            final_conf = compute_confidence(
                ocr_conf=avg_ocr_conf,
                signature_present=signature["signature_present"],
                stamp_present=stamp["stamp_present"]
            )

            results.append({
                "doc_id": doc_id,
                "fields": {
                    "dealer_name": fields["dealer_name"],
                    "model_name": fields["model_name"],
                    "horse_power": fields["horse_power"],
                    "asset_cost": fields["asset_cost"],
                    "signature": {
                        "present": signature["signature_present"],
                        "bbox": signature["signature_bbox"]
                    },
                    "stamp": {
                        "present": stamp["stamp_present"],
                        "bbox": stamp["stamp_bbox"]
                    }
                },
                "confidence": final_conf,
                "processing_time_sec": end_timer(start_time),
                "cost_estimate_usd": estimate_cost(1)
            })

        except Exception as e:
            results.append({
                "doc_id": doc_id,
                "error": str(e)
            })

    with open(OUTPUT_FILE, "w") as f:
        json.dump(results, f, indent=2)

    print("✅ Extraction complete")

if __name__ == "__main__":
    main()
