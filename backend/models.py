from sqlalchemy import Column, Integer, String, Float, DateTime, Text
from sqlalchemy.sql import func

from db import Base


class Receipt(Base):
    __tablename__ = "receipts"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(Integer, index=True)

    vendor_name = Column(String, nullable=True)
    date = Column(DateTime, nullable=True)

    total_amount = Column(Float, nullable=True)
    currency = Column(String(3), nullable=True)

    category = Column(String, nullable=True)
    category_confidence = Column(Float, nullable=True)
    categorization_method = Column(String, nullable=False)  # rule | llm

    status = Column(String, nullable=False, default="approved")  # approved | flagged

    raw_ocr_text = Column(Text, nullable=False)
    raw_ai_response = Column(Text, nullable=True)

    image_url = Column(String, nullable=True)

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )
