def evaluate_system_metrics(records: list) -> dict:
    """
    records: list of dicts with keys:
    - status (approved / flagged)
    - is_correct (bool)
    - categorization_method (rule / llm)
    """

    approved = [r for r in records if r["status"] == "approved"]
    flagged = [r for r in records if r["status"] == "flagged"]

    auto_approval_precision = (
        sum(r["is_correct"] for r in approved) / len(approved)
        if approved else None
    )

    flag_recall = (
        sum(not r["is_correct"] for r in flagged) / len(flagged)
        if flagged else None
    )

    rule_count = sum(r["categorization_method"] == "rule" for r in records)
    llm_count = sum(r["categorization_method"] == "llm" for r in records)

    return {
        "auto_approval_precision": auto_approval_precision,
        "flag_recall": flag_recall,
        "rule_usage_ratio": rule_count / len(records),
        "llm_usage_ratio": llm_count / len(records)
    }
