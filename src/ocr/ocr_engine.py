import easyocr

reader = easyocr.Reader(
    ['en', 'hi'],
    gpu=True
)
def run_ocr(image_path):
    results = reader.readtext(
        image_path,
        detail=1,
        paragraph=False,
        contrast_ths=0.1,
        adjust_contrast=0.5,
        text_threshold=0.6
    )

    extracted = []
    for bbox, text, conf in results:
        if conf < 0.4 or len(text.strip()) < 2:
            continue

        extracted.append({
            "text": text.strip(),
            "bbox": bbox,
            "confidence": round(float(conf), 3)
        })

    return extracted
