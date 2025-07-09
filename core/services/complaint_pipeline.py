from typing import Optional

from core.entities.enums import CategoryEnum
from core.models.complaint import ComplaintModel
from core.repositories.complaint import ComplaintRepository
from core.schemas.complaint import ComplaintCreate, Complaint
from core.services.category_analysis_service import CategoryAnalysisService
from core.services.sentiment_analysis_service import SentimentAnalysisService


class ComplaintPipeline:
    def __init__(self, complaint_create: ComplaintCreate):
        self.complaint_create: ComplaintCreate = complaint_create
        self.complaint: Optional[Complaint] = None
        self.complaint_id: Optional[int] = None

    async def send_complaint(self) -> Complaint:
        self.complaint = await SentimentAnalysisService.build_complaint(self.complaint_create)
        return self.complaint

    async def save_into_db(self) -> ComplaintModel:
        if self.complaint is None:
            raise ValueError('Complaint not built')

        orm = ComplaintRepository()
        complaint_model: ComplaintModel = await orm.add_complaint(self.complaint)
        self.complaint_id = complaint_model.id
        return complaint_model

    async def analyze_category_and_save(self) -> CategoryEnum:
        self.complaint.category = await CategoryAnalysisService.analyze_category(self.complaint_create)

        orm = ComplaintRepository()
        updated_category = await orm.update_complaint_category(
            self.complaint_id,
            self.complaint.category
        )

        return updated_category
