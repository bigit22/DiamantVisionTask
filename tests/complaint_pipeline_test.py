import pytest
from unittest.mock import patch
from core.entities.enums import CategoryEnum
from core.schemas.complaint import ComplaintCreate, Complaint
from core.models.complaint import ComplaintModel
from core.repositories.complaint import ComplaintRepository
from core.services.sentiment_analysis_service import SentimentAnalysisService
from core.services.category_analysis_service import CategoryAnalysisService
from core.services.complaint_pipeline import ComplaintPipeline


@pytest.mark.asyncio
async def test_send_complaint():
    complaint_create = ComplaintCreate(text="test")
    mock_complaint = ComplaintCreate(text="test", sentiment="positive", category=None)
    with patch.object(SentimentAnalysisService, 'build_complaint', return_value=mock_complaint):
        pipeline = ComplaintPipeline(complaint_create)
        await pipeline.send_complaint()
        assert pipeline.complaint == mock_complaint


@pytest.mark.asyncio
async def test_save_into_db():
    complaint_create = ComplaintCreate(text="test")
    mock_complaint = ComplaintCreate(text="test", sentiment="positive", category=None)
    mock_model = ComplaintModel(id=1)
    with patch.object(SentimentAnalysisService, 'build_complaint', return_value=mock_complaint), \
         patch.object(ComplaintRepository, 'add_complaint', return_value=mock_model):
        pipeline = ComplaintPipeline(complaint_create)
        await pipeline.send_complaint()
        result = await pipeline.save_into_db()
        assert result.id == 1


@pytest.mark.asyncio
async def test_analyze_category_and_save():
    complaint_create = ComplaintCreate(text="test")
    mock_complaint = ComplaintCreate(text="test", sentiment="positive", category=None)
    pipeline = ComplaintPipeline(complaint_create)
    await pipeline.send_complaint()
    pipeline.complaint = Complaint(id=1, text="test", sentiment="positive", category=None)
    with patch.object(CategoryAnalysisService, 'analyze_category', return_value=CategoryEnum.technical), \
         patch.object(ComplaintRepository, 'update_complaint_category', return_value=CategoryEnum.technical):
        category = await pipeline.analyze_category_and_save()
        assert category == CategoryEnum.technical
