import jiwer
import textdistance


def evaluate_text_metrics(ground_truth: str, ocr_text: str) -> dict:
    if not ground_truth or not ocr_text:
        return {
            "cer": None,
            "wer": None,
            "normalized_edit_distance": None
        }

    cer = jiwer.cer(ground_truth, ocr_text)
    wer = jiwer.wer(ground_truth, ocr_text)

    edit_distance = textdistance.levenshtein.distance(
        ground_truth,
        ocr_text
    )

    max_len = max(len(ground_truth), len(ocr_text))
    ned = 1 - (edit_distance / max_len)

    return {
        "cer": round(cer, 4),
        "wer": round(wer, 4),
        "normalized_edit_distance": round(ned, 4)
    }

