from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from typing import Optional

from models import Receipt


def is_duplicate_receipt(
    db: Session,
    user_id: int,
    vendor_name: Optional[str],
    total_amount: Optional[float],
    date: Optional[datetime],
    days_window: int = 1
) -> bool:
    """
    Checks whether a similar receipt already exists.

    Duplicate criteria:
    - Same user
    - Same vendor (if available)
    - Same total amount
    - Date within +/- days_window
    """

    if not total_amount:
        return False

    query = db.query(Receipt).filter(
        Receipt.user_id == user_id,
        Receipt.total_amount == total_amount
    )

    if vendor_name:
        query = query.filter(Receipt.vendor_name == vendor_name)

    if date:
        start_date = date - timedelta(days=days_window)
        end_date = date + timedelta(days=days_window)
        query = query.filter(Receipt.date.between(start_date, end_date))

    return db.query(query.exists()).scalar()
