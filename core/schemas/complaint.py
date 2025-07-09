from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from core.entities.enums import StatusEnum, SentimentEnum, CategoryEnum


class ComplaintCreate(BaseModel):
    text: str


class Complaint(ComplaintCreate):
    status: Optional[StatusEnum]
    timestamp: Optional[datetime]
    sentiment: Optional[SentimentEnum]
    category: Optional[CategoryEnum]

    class Config:
        from_attributes = True


class ComplaintResponse(BaseModel):
    id: int
    status: StatusEnum
    sentiment: SentimentEnum
    category: Optional[CategoryEnum]
