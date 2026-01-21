import re


def extract_numbers(text: str):
    return re.findall(r"\d+\.?\d*", text)


def evaluate_numeric_metrics(
    ground_truth_text: str,
    ocr_text: str
) -> dict:
    gt_numbers = set(extract_numbers(ground_truth_text))
    ocr_numbers = set(extract_numbers(ocr_text))

    if not gt_numbers:
        return {
            "numeric_recall": None,
            "numeric_precision": None
        }

    true_positives = len(gt_numbers & ocr_numbers)

    recall = true_positives / len(gt_numbers)
    precision = (
        true_positives / len(ocr_numbers)
        if ocr_numbers else 0.0
    )

    return {
        "numeric_recall": round(recall, 3),
        "numeric_precision": round(precision, 3)
    }
