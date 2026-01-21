import re
import os
import json
from typing import Optional, Tuple
from groq import Groq

CONFIDENCE_THRESHOLD = 2.0
MAX_RULE_SCORE = 5.0

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
            "ksrtc": 1.5
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

ALLOWED_CATEGORIES = list(CATEGORY_RULES.keys())


def normalize_text(text: str) -> str:
    text = text.lower()
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def match_keywords(text: str, keyword: str) -> bool:
    pattern = rf"\b{re.escape(keyword)}\b"
    return re.search(pattern, text) is not None


def llm_categorize(text: str) -> Tuple[Optional[str], float]:
    client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

    prompt = f"""
You are an expense categorization system.

IMPORTANT:
- Uber/Ola/Taxi/Bus/Train → Travel
- Swiggy/Zomato → Food
- Amazon/Flipkart → Shopping

Allowed categories:
{ALLOWED_CATEGORIES}

OCR Text:
{text}

Return ONLY JSON:
{{
  "category": "<category or null>",
  "confidence": <0-1>
}}
"""

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "system", "content": "Return JSON only."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.0,
        max_tokens=200
    )

    try:
        parsed = json.loads(response.choices[0].message.content)
        return parsed.get("category"), float(parsed.get("confidence", 0.0))
    except Exception:
        return None, 0.0


def categorize_text(text: str) -> Tuple[Optional[str], Optional[float], str]:

    if not text or not text.strip():
        return None, None, "llm"

    raw_text = text.lower()

    # 🔒 HARD vendor override
    for vendor, category in VENDOR_OVERRIDES.items():
        if vendor in raw_text:
            return category, 1.0, "rule"

    text = normalize_text(text)

    scores = {}

    for category, rule_data in CATEGORY_RULES.items():
        score = 0.0
        for keyword, weight in rule_data["keywords"].items():
            if match_keywords(text, keyword):
                score += weight
        if score > 0:
            scores[category] = score

    if scores:
        best_category = max(scores, key=scores.get)
        best_score = scores[best_category]

        if best_score >= CONFIDENCE_THRESHOLD:
            confidence = min(best_score / MAX_RULE_SCORE, 1.0)
            if len(text) < 40:
                confidence -= 0.15
            return best_category, round(max(confidence, 0.0), 2), "rule"

    llm_category, llm_confidence = llm_categorize(text)

    if llm_category in ALLOWED_CATEGORIES:
        return llm_category, round(llm_confidence, 2), "llm"

    return None, None, "llm"
