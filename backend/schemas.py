from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class ReceiptBase(BaseModel):
    user_id: int
    vendor_name: Optional[str]
    date: Optional[datetime]
    total_amount: Optional[float]
    currency: Optional[str]
    category: Optional[str]
    category_confidence: Optional[float]
    categorization_method: str
    status: str

class ReceiptCreate(ReceiptBase):
    raw_ocr_text:str
    raw_ai_response:Optional[str]
    image_url:Optional[str]

class ReceiptResponse(ReceiptBase):
    id:int 
    created_at:datetime
    class Config:
        orm_mode=True                #Pydantic expects json/dicts but the response scehma (db to frontend)
                                     #ie the db prodeuces data in the form of objects data.id thus to convert from 
                                     #objects to dicts so that data is readable we use orm_mode=True so that pydantic can read the data comming in from db 
                

#Optional Later we will use maybe 
class ReceiptListResponse(BaseModel):      
    id: int
    vendor_name: Optional[str]
    total_amount: Optional[float]
    currency: Optional[str]
    category: Optional[str]
    date: Optional[datetime]

    class Config:
        orm_mode = True