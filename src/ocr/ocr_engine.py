import os

# 🔴 DISABLE PIR + MKLDNN (CRITICAL)
os.environ["FLAGS_enable_pir_api"] = "0"
os.environ["FLAGS_use_mkldnn"] = "0"
os.environ["OMP_NUM_THREADS"] = "1"

from paddleocr import PaddleOCR

ocr_model = PaddleOCR(
    use_angle_cls=True,
    lang="en"
)

def run_ocr(image_path):
    results = ocr_model.ocr(image_path)
    extracted = []

    if not results or not results[0]:
        return extracted

    for line in results[0]:
        bbox, (text, conf) = line
        extracted.append({
            "text": text.strip(),
            "bbox": bbox,
            "confidence": round(conf, 3)
        })

    return extracted
