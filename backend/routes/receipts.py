from fastapi import APIRouter, UploadFile, File, Depends
from sqlalchemy.orm import Session

from backend.db import get_db
from backend.models import Receipt
from backend.services.ocr import extract_text_from_image
from backend.services.categorization import categorize_text
from backend.services.duplicate_check import is_duplicate_receipt

router = APIRouter(
    prefix="/receipts",
    tags=["Receipts"]
)


@router.post("/upload")
def upload_receipt(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    #  OCR
    ocr_text = extract_text_from_image(file)

    # Categorization
    category, confidence, method = categorize_text(ocr_text)

    # Duplicate check (basic placeholder values for now)
    is_duplicate = is_duplicate_receipt(
        db=db,
        user_id=1,
        vendor_name=None,
        total_amount=None,
        date=None
    )

    status = "flagged" if is_duplicate else "approved"

    #  Save to DB
    receipt = Receipt(
        user_id=1,
        raw_ocr_text=ocr_text,
        category=category,
        category_confidence=confidence,
        categorization_method=method,
        status=status,
        review_status="pending",
        reviewed_by_human=False
    )

    db.add(receipt)
    db.commit()
    db.refresh(receipt)

    return {
        "receipt_id": receipt.id,
        "status": receipt.status,
        "review_status": receipt.review_status
    }
