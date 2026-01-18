# Text extraction output schema (freeze this)

TEXT_SCHEMA = {
    "dealer_name": {
        "value": None,
        "confidence": 0.0
    },
    "model_name": {
        "value": None,
        "confidence": 0.0
    },
    "horse_power": {
        "value": None,
        "confidence": 0.0
    },
    "asset_cost": {
        "value": None,
        "confidence": 0.0
    }
}

# Vision teammate will follow this later
VISION_SCHEMA = {
    "signature": {
        "present": False,
        "bbox": None,
        "confidence": 0.0
    },
    "stamp": {
        "present": False,
        "bbox": None,
        "confidence": 0.0
    }
}
