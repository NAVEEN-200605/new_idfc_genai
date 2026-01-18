from paddleocr import PaddleOCR
import logging

# suppress PaddleOCR info messages
logging.getLogger("paddleocr").setLevel(logging.WARNING)

# Initialize OCR
ocr_model = PaddleOCR(
    use_angle_cls=True,
    lang="multi"   # English + Hindi + mixed
)

def run_ocr(image):
    results = ocr_model.ocr(image, cls=True)
    ocr_outputs = []

    if results is None:
        return ocr_outputs

    for line in results:
        for box, (text, conf) in line:
            ocr_outputs.append({
                "text": text.strip(),
                "bbox": box,
                "confidence": float(conf)
            })
    return ocr_outputs
