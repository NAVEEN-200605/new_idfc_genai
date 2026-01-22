import cv2
import numpy as np

def preprocess_image(image_path):
    img = cv2.imread(image_path)

    if img is None:
        raise ValueError("Image not loaded")

    # 1️⃣ Resize (EasyOCR LOVES large text)
    h, w = img.shape[:2]
    if w < 1400:
        scale = 1400 / w
        img = cv2.resize(img, None, fx=scale, fy=scale, interpolation=cv2.INTER_CUBIC)

    # 2️⃣ Grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # 3️⃣ Contrast enhancement
    clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8,8))
    gray = clahe.apply(gray)

    # 4️⃣ Light denoise (DON’T overdo for EasyOCR)
    gray = cv2.GaussianBlur(gray, (3,3), 0)

    return gray
