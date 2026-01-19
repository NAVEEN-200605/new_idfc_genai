import re
from rapidfuzz import fuzz

BRANDS = [
    "mahindra", "swaraj", "john deere",
    "sonalika", "kubota", "new holland"
]

DEALER_KEYWORDS = [
    "tractors", "tractor", "motors", "agencies",
    "dealer", "auto", "industries", "corporation"
]

COST_KEYWORDS = ["total", "net", "grand", "amount", "price", "cost"]

IGNORE_MODEL_WORDS = [
    "dealer", "agency", "motors", "auto",
    "gst", "quotation", "invoice"
]
def get_y_center(bbox):
    try:
        if isinstance(bbox[0], (list, tuple)):
            ys = [pt[1] for pt in bbox if len(pt) >= 2]
            return sum(ys) / len(ys)
        elif len(bbox) == 4:
            return (bbox[1] + bbox[3]) / 2
    except Exception:
        pass
    return None

def normalize(t):
    return re.sub(r'[^a-z0-9 ]', '', t.lower()).strip()


# ---------------- DEALER ----------------
def extract_dealer_name(ocr, image_height):
    scored = []

    for o in ocr:
        txt = o["text"]
        low = normalize(txt)
        conf = o.get("confidence", 0.8)

        y_center = get_y_center(o["bbox"])
        if y_center is None:
            continue

        top_bias = 1.0 if y_center < 0.35 * image_height else 0.6

        keyword_score = max(
            [fuzz.partial_ratio(k, low) for k in DEALER_KEYWORDS],
            default=0
        )

        if len(low) > 8 and keyword_score > 70:
            score = keyword_score * conf * top_bias
            scored.append((score, txt))

    if scored:
        return max(scored, key=lambda x: x[0])[1]

    top_texts = [
        o["text"] for o in ocr
        if sum(p[1] for p in o["bbox"]) / 4 < 0.3 * image_height
    ]
    return max(top_texts, key=len) if top_texts else None


# ---------------- BRAND ----------------
def extract_brand(ocr):
    best, best_score = None, 0

    for o in ocr:
        txt = normalize(o["text"])
        for b in BRANDS:
            score = fuzz.partial_ratio(b, txt)
            if score > best_score and score > 85:
                best, best_score = b.title(), score

    return best


# ---------------- MODEL ----------------
def extract_model(ocr, brand):
    candidates = []

    for o in ocr:
        raw = o["text"]
        txt = normalize(raw)

        if any(w in txt for w in IGNORE_MODEL_WORDS):
            continue

        if brand and brand.lower() in txt:
            candidates.append(raw)

        if re.search(r'\b\d{3,4}\b', txt):
            candidates.append(raw)

    return max(candidates, key=len) if candidates else None


# ---------------- HP ----------------
def extract_hp(ocr):
    for o in ocr:
        txt = normalize(o["text"]).replace("hf", "hp").replace("o", "0")

        m = re.search(r'(\d{2})\s*hp', txt)
        if m:
            hp = int(m.group(1))
            if 20 <= hp <= 90:
                return hp
    return None


# ---------------- AMOUNT ----------------
def extract_amount(ocr):
    candidates = []

    for o in ocr:
        txt = normalize(o["text"])
        conf = o.get("confidence", 0.8)

        if any(x in txt for x in ["gst", "cgst", "sgst", "advance", "emi"]):
            continue

        nums = re.findall(r'\d{5,}', txt.replace(",", ""))
        if not nums:
            continue

        value = max(int(n) for n in nums)
        bonus = 1.3 if any(k in txt for k in COST_KEYWORDS) else 1.0

        candidates.append((value * bonus * conf, value))

    return max(candidates, key=lambda x: x[0])[1] if candidates else None


# ---------------- MAIN ----------------
def extract_all_fields(ocr, image_height):
    brand = extract_brand(ocr)

    return {
        "dealer_name": extract_dealer_name(ocr, image_height),
        "model_name": extract_model(ocr, brand),
        "horse_power": extract_hp(ocr),
        "asset_cost": extract_amount(ocr)
    }
