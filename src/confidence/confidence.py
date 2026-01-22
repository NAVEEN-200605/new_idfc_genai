def compute_confidence(ocr_conf=0.0, signature_present=False, stamp_present=False):
    confidence = 0.0

    # OCR confidence (main contributor)
    confidence += 0.6 * ocr_conf

    # Visual validation
    if signature_present:
        confidence += 0.2
    if stamp_present:
        confidence += 0.2

    return round(min(confidence, 1.0), 2)
