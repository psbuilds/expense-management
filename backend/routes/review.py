from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from backend.db import get_db
from backend.models import Receipt

router = APIRouter(
    prefix="/review",
    tags=["Human Review"]
)

@router.post("/submit")
def submit_human_review(payload: dict, db: Session = Depends(get_db)):
    receipt_id = payload["receipt_id"]
    approved = payload["approved"]
    corrected_fields = payload.get("corrected_fields")
    reviewer_id = payload.get("reviewer_id")

    receipt = db.query(Receipt).filter(Receipt.id == receipt_id).first()

    if not receipt:
        return {"error": "Receipt not found"}

    receipt.review_status = "approved" if approved else "rejected"
    receipt.reviewed_by_human = True
    receipt.human_reviewer_id = reviewer_id

    if corrected_fields:
        receipt.corrected_fields = corrected_fields

    db.commit()

    return {
        "receipt_id": receipt_id,
        "final_decision": approved,
        "corrected_fields": corrected_fields
    }
