from evaluation.evaluation_runner import run_evaluation


if __name__ == "__main__":
    # Ground Truth (Human-verified)
    ground_truth = {
        "full_text": "STARBUCKS\nDate: 2024-03-12\nTotal: 245.50 INR",
        "vendor_name": "Starbucks",
        "total_amount": 245.50,
        "currency": "INR",
        "date": "2024-03-12"
    }

    # System Prediction (OCR output)
    prediction = {
        "raw_ocr_text": "STARBUCKS Date 12/03/24 Total Rs 245.5",
        "vendor_name": "Starbucks",
        "total_amount": 245.5,
        "currency": "INR",
        "date": "2024-03-12"
    }

    # Human Review (Layer 3)
    human_review = {
        "receipt_id": 1,
        "approved": True,
        "corrected_fields": {
            "total_amount": 245.50
        },
        "reviewer_id": "human_001",
        "comments": "Amount formatting differs but value is correct"
    }

    
    # Run full 3-layer evaluation
    result = run_evaluation(
        ground_truth=ground_truth,
        prediction=prediction,
        human_review=human_review
    )

    print("\nFULL 3-LAYER EVALUATION RESULT\n")
    for key, value in result.items():
        print(f"{key}: {value}")
