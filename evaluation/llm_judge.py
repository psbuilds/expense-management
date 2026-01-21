from typing import Dict 
import os , json 
from groq import Groq

def build_llm_judge_prompt(
    ground_truth: Dict,
    prediction: Dict
) -> str:
    """
    Builds a strict prompt for LLM-based OCR judging.
    """

    return f"""
You are an independent evaluator for an OCR-based Expense Management system.

Your job is to judge whether the OCR output is SEMANTICALLY correct
when compared to the ground truth.

IMPORTANT RULES:
- Do NOT correct the OCR.
- Do NOT explain your reasoning.
- Do NOT add extra text.
- Respond ONLY in valid JSON.

Ground Truth Text:
{ground_truth['full_text']}

OCR Output Text:
{prediction['raw_ocr_text']}

Ground Truth Fields:
Vendor: {ground_truth.get('vendor_name')}
Amount: {ground_truth.get('total_amount')}
Currency: {ground_truth.get('currency')}
Date: {ground_truth.get('date')}

OCR Extracted Fields:
Vendor: {prediction.get('vendor_name')}
Amount: {prediction.get('total_amount')}
Currency: {prediction.get('currency')}
Date: {prediction.get('date')}

Return STRICTLY this JSON format:
{{
  "semantic_match": true or false,
  "missing_or_incorrect_fields": [list of field names],
  "confidence": number between 0 and 1
}}

Use these canonical field names ONLY:
vendor_name, total_amount, currency, date
"""

def call_llm(prompt: str) -> Dict:
    """
    Calls Groq LLM to act as an OCR semantic judge.
    Must return strict JSON.
    """

    client = Groq(
        api_key=os.environ.get("GROQ_API_KEY")
    )

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a strict JSON API. "
                    "Return ONLY valid JSON. "
                    "No explanations."
                )
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.0,          # deterministic
        max_tokens=300
    )

    raw_output = response.choices[0].message.content.strip()

    try:
        parsed = json.loads(raw_output)
        return parsed
    except json.JSONDecodeError:
        # Safety fallback
        return {
            "semantic_match": False,
            "missing_or_incorrect_fields": ["llm_parse_error"],
            "confidence": 0.0
        }


def llm_judge(
    ground_truth: Dict,
    prediction: Dict
) -> Dict:
    """
    Runs LLM as an independent judge for OCR semantic correctness.
    """

    prompt = build_llm_judge_prompt(ground_truth, prediction)
    response = call_llm(prompt)

    # ---- VALIDATION (VERY IMPORTANT) ----
    required_keys = {
        "semantic_match",
        "missing_or_incorrect_fields",
        "confidence"
    }

    if not isinstance(response, dict):
        raise ValueError("LLM judge response is not a dictionary")

    if not required_keys.issubset(response.keys()):
        raise ValueError(
            f"LLM judge response missing required keys: {required_keys}"
        )

    if not isinstance(response["semantic_match"], bool):
        raise ValueError("semantic_match must be boolean")

    if not isinstance(response["missing_or_incorrect_fields"], list):
        raise ValueError("missing_or_incorrect_fields must be a list")

    if not (0.0 <= response["confidence"] <= 1.0):
        raise ValueError("confidence must be between 0 and 1")

    return response
