import cv2
from utils.image_utils import preprocess_image, find_contours

def detect_signature(image_path):
    img = cv2.imread(image_path)
    if img is None:
        raise ValueError("Image not loaded")

    thresh = preprocess_image(img)
    contours = find_contours(thresh)

    for cnt in contours:
        x, y, w, h = cv2.boundingRect(cnt)
        area = w * h

        # Signature: long & thin
        if area > 5000 and w > h * 2:
            return {
                "signature_present": True,
                "signature_bbox": [x, y, x + w, y + h]
            }

    return {
        "signature_present": False,
        "signature_bbox": None
    }
