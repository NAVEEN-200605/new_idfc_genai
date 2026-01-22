import re
from rapidfuzz import process

MODEL_MASTER = [
    "Mahindra 575 DI",
    "Mahindra 265 DI",
    "Swaraj 735 FE",
    "John Deere 5310",
    "New Holland 3630"
]

DEALER_KEYWORDS = [
    "tractor", "traders", "motors", "agro",
    "farm", "pvt", "ltd", "agency"
]
def extract_dealer_name(header):
    candidates = []

    for item in header:
        text = item["text"].lower()

        # ignore contact lines
        if any(k in text for k in ["phone", "fax", "email", "@", "epbx"]):
            continue

        if any(k in text for k in DEALER_KEYWORDS) and len(text) > 15:
            candidates.append(item)

    if not candidates:
        return None, 0.0

    best = max(candidates, key=lambda x: x["confidence"])
    return best["text"], best["confidence"]
def extract_model_name(body):
    texts = [i["text"].lower() for i in body]

    for t in texts:
        # catch handwritten variants
        if "575" in t and "di" in t:
            return "Mahindra 575 DI", 0.9
        if "735" in t:
            return "Swaraj 735 FE", 0.85
        if "5310" in t:
            return "John Deere 5310", 0.85

    # fallback to fuzzy
    combined = " ".join(texts)
    match = process.extractOne(combined, MODEL_MASTER)

    if match and match[1] > 80:
        return match[0], match[1] / 100

    return None, 0.0

def extract_hp(body):
    for item in body:
        text = item["text"].lower()
        m = re.search(r'(\d{2,3})\s*(hp|h\.p|horse)', text)
        if m:
            return int(m.group(1)), item["confidence"]

    return None, 0.0

def extract_asset_cost(footer):
    numbers = []

    for item in footer:
        text = item["text"].replace(",", "")
        found = re.findall(r"\d{5,7}", text)  # >= 5 digits only
        for f in found:
            val = int(f)
            if val > 50000:  # ignore years, small numbers
                numbers.append((val, item["confidence"]))

    if not numbers:
        return None, 0.0

    value, conf = max(numbers, key=lambda x: x[0])
    return value, conf


def extract_all_fields(layout):
    dealer, d_conf = extract_dealer_name(layout["header"])
    model, m_conf = extract_model_name(layout["body"])
    hp, hp_conf = extract_hp(layout["body"])
    cost, c_conf = extract_asset_cost(layout["footer"])

    final_confidence = round(
        0.30 * d_conf +
        0.25 * m_conf +
        0.20 * hp_conf +
        0.25 * c_conf,
        3
    )

    return {
        "dealer_name": dealer,
        "model_name": model,
        "horse_power": hp,
        "asset_cost": cost
    }, final_confidence
