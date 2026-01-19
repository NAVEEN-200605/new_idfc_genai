import cv2

def preprocess_image(image_path):
    """
    Preprocess image for OCR (handwriting-safe).
    """
    img = cv2.imread(image_path)
    if img is None:
        raise ValueError(f"Cannot read image: {image_path}")

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Light denoising only
    denoised = cv2.fastNlMeansDenoising(gray, h=20)

    return denoised
