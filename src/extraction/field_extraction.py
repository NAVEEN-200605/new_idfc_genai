import re
from rapidfuzz import fuzz

def extract_dealer_name(header_items):
    if not header_items:
        return None, 0.0

    # Pick largest-confidence text in header
    best = max(header_items, key=lambda x: x["confidence"])
    return best["text"], best["confidence"]


def extract_model_name(body_items):
    for item in body_items:
        text = item["text"]
        if any(k in text.lower() for k in ["model", "tractor"]):
            return text, item["confidence"]
    return None, 0.0


def extract_horse_power(body_items):
    for item in body_items:
        match = re.search(r"(\d+)\s*(HP|hp|एचपी)?", item["text"])
        if match:
            return int(match.group(1)), item["confidence"]
    return None, 0.0


def extract_asset_cost(items):
    amounts = []

    for item in items:
        nums = re.findall(r"\d{1,3}(?:,\d{3})+", item["text"])
        for n in nums:
            value = int(n.replace(",", ""))
            amounts.append((value, item["confidence"]))

    if not amounts:
        return None, 0.0

    # Choose max amount (business logic)
    return max(amounts, key=lambda x: x[0])


def extract_all_fields(layout_dict):
    dealer, d_conf = extract_dealer_name(layout_dict["header"])
    model, m_conf = extract_model_name(layout_dict["body"])
    hp, hp_conf = extract_horse_power(layout_dict["body"])
    cost, c_conf = extract_asset_cost(layout_dict["body"] + layout_dict["footer"])

    return {
        "dealer_name": {"value": dealer, "confidence": d_conf},
        "model_name": {"value": model, "confidence": m_conf},
        "horse_power": {"value": hp, "confidence": hp_conf},
        "asset_cost": {"value": cost, "confidence": c_conf}
    }
