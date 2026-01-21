from typing import Dict, Optional


def apply_human_review(
    evaluation_result: Dict,
    human_review: Optional[Dict] = None
) -> Dict:
    """
    Applies human approval as the final verification layer.
    """

    evaluation_result["human_review"] = human_review

    if human_review is None:
        evaluation_result["final_decision"] = None  # Pending
        return evaluation_result

    evaluation_result["final_decision"] = human_review.get("approved")
    evaluation_result["corrected_fields"] = human_review.get(
        "corrected_fields", {}
    )

    return evaluation_result
