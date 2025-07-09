from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from core.entities.enums import StatusEnum, SentimentEnum, CategoryEnum


class ComplaintCreate(BaseModel):
    text: str


class Complaint(ComplaintCreate):
    status: Optional[StatusEnum] = None
    timestamp: Optional[datetime] = None
    sentiment: Optional[SentimentEnum] = None
    category: Optional[CategoryEnum] = None

    class Config:
        from_attributes = True


class ComplaintResponse(BaseModel):
    id: int
    status: StatusEnum
    sentiment: SentimentEnum
    category: Optional[CategoryEnum]
