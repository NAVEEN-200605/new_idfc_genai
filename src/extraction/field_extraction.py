import re
import random
from rapidfuzz import process

# =========================
# MASTER DATA
# =========================

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

# =========================
# RANDOM FALLBACK POOLS
# =========================

RANDOM_HP = [30, 35, 45, 50, 55]

RANDOM_MODELS = MODEL_MASTER

RANDOM_COSTS = [
    450000, 500000, 525000,
    600000, 650000, 700000
]

RANDOM_DEALERS = [
    "ABC Tractors Pvt Ltd",
    "Sri Sai Tractors",
    "Jai Kisan Motors",
    "Shree Agro Industries",
    "Om Tractors"
]

# =========================
# UTILS
# =========================

def merge_text(items):
    return " ".join(
        [i["text"] for i in items if len(i["text"]) > 1]
    ).lower()

# =========================
# FIELD EXTRACTION
# =========================

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

    # handwritten / noisy catches
    for t in texts:
        if "575" in t and "di" in t:
            return "Mahindra 575 DI", 0.9
        if "735" in t:
            return "Swaraj 735 FE", 0.85
        if "5310" in t:
            return "John Deere 5310", 0.85

    # fuzzy fallback
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
        found = re.findall(r"\d{5,7}", text)
        for f in found:
            val = int(f)
            if val > 50000:
                numbers.append((val, item["confidence"]))

    if not numbers:
        return None, 0.0

    value, conf = max(numbers, key=lambda x: x[0])
    return value, conf

# =========================
# MAIN AGGREGATOR
# =========================

def extract_all_fields(layout):
    dealer, d_conf = extract_dealer_name(layout["header"])
    model, m_conf = extract_model_name(layout["body"])
    hp, hp_conf = extract_hp(layout["body"])
    cost, c_conf = extract_asset_cost(layout["footer"])

    inference = {
        "dealer_random": False,
        "model_random": False,
        "hp_random": False,
        "cost_random": False
    }

    # -------- RANDOM FALLBACKS --------

    if dealer is None:
        dealer = random.choice(RANDOM_DEALERS)
        d_conf = 0.25
        inference["dealer_random"] = True

    if model is None:
        model = random.choice(RANDOM_MODELS)
        m_conf = 0.25
        inference["model_random"] = True

    if hp is None:
        hp = random.choice(RANDOM_HP)
        hp_conf = 0.25
        inference["hp_random"] = True

    if cost is None:
        cost = random.choice(RANDOM_COSTS)
        c_conf = 0.25
        inference["cost_random"] = True

    # -------- CONFIDENCE --------

    final_confidence = (
        0.30 * d_conf +
        0.25 * m_conf +
        0.20 * hp_conf +
        0.25 * c_conf
    )

    if any(inference.values()):
        final_confidence *= 0.7

    final_confidence = round(final_confidence, 3)

    return {
        "dealer_name": dealer,
        "model_name": model,
        "horse_power": hp,
        "asset_cost": cost,
        "inference": inference
    }, final_confidence
