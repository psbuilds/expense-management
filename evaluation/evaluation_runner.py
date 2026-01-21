from evaluation.text_metrics import evaluate_text_metrics
from evaluation.field_metrics import evaluate_field_metrics
from evaluation.numeric_metrics import evaluate_numeric_metrics
from evaluation.llm_judge import llm_judge
from evaluation.human_review import apply_human_review


def run_evaluation(
    ground_truth: dict,
    prediction: dict,
    human_review: dict | None = None
) -> dict:
    result = {}

    # -------- Layer 1: Automated Metrics --------
    result["automated_metrics"] = {
        "text": evaluate_text_metrics(
            ground_truth["full_text"],
            prediction["raw_ocr_text"]
        ),
        "fields": evaluate_field_metrics(ground_truth, prediction),
        "numeric": evaluate_numeric_metrics(
            ground_truth["full_text"],
            prediction["raw_ocr_text"]
        )
    }

    # -------- Layer 2: LLM as a Judge --------
    result["llm_judge"] = llm_judge(ground_truth, prediction)

    # -------- Layer 3: Human Approval --------
    result = apply_human_review(result, human_review)

    return result
