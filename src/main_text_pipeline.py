import os
import json
import cv2
from tqdm import tqdm

from ocr.ocr_engine import run_ocr
from layout.layout_grouping import group_by_layout
from extraction.field_extraction import extract_all_fields

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IMAGE_DIR = os.path.join(BASE_DIR, "data", "images")
OUTPUT_FILE = os.path.join(BASE_DIR, "outputs", "text_extraction_results.json")

def main(limit=3):
    results = []
    images = sorted(os.listdir(IMAGE_DIR))[:limit]

    for idx, img in enumerate(tqdm(images)):
        doc_id = f"invoice_{idx+1:03d}"
        img_path = os.path.join(IMAGE_DIR, img)

        try:
            image = cv2.imread(img_path)
            if image is None:
                raise ValueError("Image not readable")

            h, _, _ = image.shape

            ocr_data = run_ocr(img_path)
            layout = group_by_layout(ocr_data, h)

            extracted_fields, confidence = extract_all_fields(layout)

            results.append({
                "doc_id": doc_id,
                "fields": extracted_fields,
                "confidence": confidence
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
