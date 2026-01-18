import os
import json
from tqdm import tqdm
import cv2

from preprocess.image_cleaning import preprocess_image
from ocr.ocr_engine import run_ocr
from layout.layout_grouping import group_by_layout
from extraction.field_extraction import extract_all_fields

IMAGE_DIR = "data/images"
OUTPUT_FILE = "outputs/text_extraction_results.json"

def main():
    all_results = {}

    for img_name in tqdm(os.listdir(IMAGE_DIR)):
        if not img_name.lower().endswith(".png"):
            continue

        img_path = os.path.join(IMAGE_DIR, img_name)

        try:
            # Step 1: Preprocess image
            cleaned_img = preprocess_image(img_path)

            # Step 2: OCR
            ocr_result = run_ocr(cleaned_img)

            # Step 3: Layout grouping
            image_height = cleaned_img.shape[0]
            layout = group_by_layout(ocr_result, image_height)

            # Step 4: Field extraction
            fields = extract_all_fields(layout)

            # Store result
            all_results[img_name] = {
                "fields": fields
            }

        except Exception as e:
            print(f"Error processing {img_name}: {e}")
            all_results[img_name] = {
                "fields": None,
                "error": str(e)
            }

    os.makedirs("outputs", exist_ok=True)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(all_results, f, ensure_ascii=False, indent=2)

    print(f"\n✅ Text extraction completed. Results saved to {OUTPUT_FILE}")

if __name__ == "__main__":
    main()

