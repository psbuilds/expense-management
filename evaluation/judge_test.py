from evaluation.llm_judge import llm_judge

if __name__ == "__main__":
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

    result = llm_judge(ground_truth, prediction)

    print("LLM Judge Output:")
    print(result)
