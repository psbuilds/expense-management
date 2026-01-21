from evaluation.evaluation_runner import run_evaluation

ground_truth = {
    "full_text": "STARBUCKS\nTotal: 245.50 INR",
    "vendor_name": "Starbucks",
    "total_amount": 245.50,
    "currency": "INR",
    "date": "2024-03-12"
}

prediction = {
    "raw_ocr_text": "STARBUCKS Total Rs 245.5",
    "vendor_name": "Starbucks",
    "total_amount": 245.5,
    "currency": "INR",
    "date": "2024-03-12"
}

human_review = {
    "receipt_id": 1,
    "approved": True,
    "corrected_fields": {},
    "reviewer_id": "human_001",
    "comments": "Minor OCR formatting issue"
}

print(run_evaluation(ground_truth, prediction, human_review))
