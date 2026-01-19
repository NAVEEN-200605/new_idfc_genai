from paddleocr import PaddleOCR

ocr_model = PaddleOCR(
    use_angle_cls=True,
    lang="en"
)
def get_y_center(bbox):
    """
    Safely compute Y-center from PaddleOCR bbox.
    Works for all bbox formats.
    """
    try:
        # Case 1: [[x,y], [x,y], ...]
        if isinstance(bbox[0], (list, tuple)):
            ys = [pt[1] for pt in bbox if len(pt) >= 2]
            return sum(ys) / len(ys)

        # Case 2: [x1, y1, x2, y2]
        elif len(bbox) == 4:
            return (bbox[1] + bbox[3]) / 2

    except Exception:
        pass

    return None

def run_ocr(image):
    """
    Returns list of:
    {
        "text": str,
        "confidence": float,
        "bbox": [[x,y], [x,y], [x,y], [x,y]]
    }
    """
    result = ocr_model.ocr(image)
    ocr_data = []

    if not result:
        return ocr_data

    for line in result:
        if not isinstance(line, list):
            continue

        for item in line:
            try:
                box = item[0]
                text = item[1][0]
                conf = item[1][1]

                if isinstance(text, str) and text.strip():
                    ocr_data.append({
                        "text": text.strip(),
                        "confidence": float(conf),  # 🔥 FIXED
                        "bbox": box
                    })
            except Exception:
                continue

    return ocr_data
