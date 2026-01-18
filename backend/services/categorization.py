import re
from typing import Optional, Tuple

CONFIDENCE_THRESHOLD = 2.0          # minimum rule score to accept
MAX_RULE_SCORE = 5.0                # used to normalize confidence

VENDOR_OVERRIDES = {
    "swiggy": "Food",
    "zomato": "Food",
    "uber": "Travel",
    "ola": "Travel",
    "amazon": "Shopping",
    "flipkart": "Shopping"
}


CATEGORY_RULES = {
    "Food": {
        "keywords": {
            "restaurant": 2.0,
            "cafe": 2.0,
            "dine": 1.0,
            "food": 1.0,
            "swiggy": 3.0,
            "zomato": 3.0,
            "hotel": 1.5
        }
    },
    "Travel": {
        "keywords": {
            "uber": 3.0,
            "ola": 3.0,
            "taxi": 2.0,
            "flight": 3.0,
            "train": 2.0,
            "bus": 1.5,
            "ksrtc":1.5
        }
    },
    "Shopping": {
        "keywords": {
            "amazon": 3.0,
            "flipkart": 3.0,
            "mall": 2.0,
            "store": 1.5,
            "shopping": 1.0
        }
    },
    "Utilities": {
        "keywords": {
            "electricity": 3.0,
            "water bill": 3.0,
            "gas bill": 3.0,
            "internet": 2.0,
            "broadband": 2.0,
            "recharge": 1.0
        }
    }
}

def normalize_text(text: str) -> str:
    text = text.lower()
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def match_keywords(text: str, keyword: str) -> bool:
    pattern = rf"\b{re.escape(keyword)}\b"
    return re.search(pattern, text) is not None

def categorize_text(text: str) -> Tuple[Optional[str], Optional[float], str]:
    """
    Returns:
        category (str | None)
        confidence (float | None)  # 0.0 – 1.0
        categorization_method ("rule" | "llm")
    """

    if not text or not text.strip():
        return None, None, "llm"

    text = normalize_text(text)

    for vendor, category in VENDOR_OVERRIDES.items():
        if vendor in text:
            return category, 1.0, "rule"

    scores = {}

    for category, rule_data in CATEGORY_RULES.items():
        score = 0.0
        for keyword, weight in rule_data["keywords"].items():
            if match_keywords(text, keyword):
                score += weight

        if score > 0:
            scores[category] = score

    if not scores:
        return None, None, "llm"

    best_category = max(scores, key=scores.get)
    best_score = scores[best_category]

    if best_score < CONFIDENCE_THRESHOLD:
        return None, None, "llm"

    confidence = min(best_score / MAX_RULE_SCORE, 1.0)

    # Penalize very short OCR text (low signal quality)
    if len(text) < 40:
        confidence -= 0.15

    confidence = max(0.0, round(confidence, 2))

    return best_category, confidence, "rule"
