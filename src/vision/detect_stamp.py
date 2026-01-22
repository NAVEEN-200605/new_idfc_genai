import cv2
from utils.image_utils import preprocess_image, find_contours

def detect_stamp(image_path):
    img = cv2.imread(image_path)
    if img is None:
        raise ValueError("Image not loaded")

    thresh = preprocess_image(img)
    contours = find_contours(thresh)

    for cnt in contours:
        x, y, w, h = cv2.boundingRect(cnt)
        area = w * h
        aspect_ratio = w / float(h)

        # Stamp: roughly square
        if area > 3000 and 0.8 < aspect_ratio < 1.2:
            return {
                "stamp_present": True,
                "stamp_bbox": [x, y, x + w, y + h]
            }

    return {
        "stamp_present": False,
        "stamp_bbox": None
    }
