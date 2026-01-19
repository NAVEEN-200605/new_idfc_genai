import os
import json
from tqdm import tqdm

from preprocess.image_cleaning import preprocess_image
from ocr.ocr_engine import run_ocr
from extraction.field_extraction import extract_all_fields

IMAGE_DIR = "data/images"
OUTPUT_FILE = "outputs/output.json"

def main():
    results = []

    images = sorted([i for i in os.listdir(IMAGE_DIR) if i.endswith(".png")])[:3]



    for idx, img in enumerate(tqdm(images), start=1):
        doc_id = f"invoice_{idx:03d}"
        path = os.path.join(IMAGE_DIR, img)

        try:
            img_clean = preprocess_image(path)
            ocr = run_ocr(img_clean)
            height = img_clean.shape[0]

            fields = extract_all_fields(ocr, height)

            results.append({
                "doc_id": doc_id,
                "fields": fields
            })

        except Exception as e:
            results.append({
                "doc_id": doc_id,
                "fields": None,
                "error": str(e)
            })

    os.makedirs("outputs", exist_ok=True)
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)

    print("✅ Done")

if __name__ == "__main__":
    main()
