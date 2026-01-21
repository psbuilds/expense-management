from datetime import datetime


def evaluate_field_metrics(
    ground_truth: dict,
    predicted: dict
) -> dict:
    results = {}

    # Vendor match
    gt_vendor = ground_truth.get("vendor_name")
    pred_vendor = predicted.get("vendor_name")
    results["vendor_match"] = (
        gt_vendor.lower() == pred_vendor.lower()
        if gt_vendor and pred_vendor else None
    )

    # Amount accuracy
    gt_amount = ground_truth.get("total_amount")
    pred_amount = predicted.get("total_amount")
    if gt_amount is not None and pred_amount is not None:
        results["amount_error"] = round(abs(gt_amount - pred_amount), 2)
    else:
        results["amount_error"] = None

    # Date accuracy (±1 day tolerance)
    gt_date = ground_truth.get("date")
    pred_date = predicted.get("date")
    if gt_date and pred_date:
        gt_date = datetime.fromisoformat(gt_date)
        pred_date = datetime.fromisoformat(pred_date)
        results["date_diff_days"] = abs((gt_date - pred_date).days)
    else:
        results["date_diff_days"] = None

    # Currency match
    gt_currency = ground_truth.get("currency")
    pred_currency = predicted.get("currency")
    results["currency_match"] = (
        gt_currency == pred_currency
        if gt_currency and pred_currency else None
    )

    return results
