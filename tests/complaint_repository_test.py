import pytest
import pytest_asyncio
from core.repositories import ComplaintRepository
from core.schemas.complaint import Complaint
from core.entities.enums import CategoryEnum, StatusEnum, SentimentEnum


@pytest_asyncio.fixture
async def repo():
    repository = ComplaintRepository()
    await repository.init_db()
    return repository


@pytest.mark.asyncio
async def test_add_and_get_complaint(repo):
    complaint_data = Complaint(
        text="Test complaint",
        status=StatusEnum.open,
        timestamp=None,
        sentiment=SentimentEnum.neutral,
        category=CategoryEnum.technical
    )
    added = await repo.add_complaint(complaint_data)
    assert added.id is not None
    complaints = await repo.get_complaints()
    assert any(c.id == added.id for c in complaints)


@pytest.mark.asyncio
async def test_update_complaint_category(repo):
    complaint_data = Complaint(
        text="Another complaint",
        status=StatusEnum.open,
        timestamp=None,
        sentiment=SentimentEnum.negative,
        category=CategoryEnum.payment
    )
    added = await repo.add_complaint(complaint_data)
    updated_category = await repo.update_complaint_category(added.id, CategoryEnum.technical)
    assert updated_category == CategoryEnum.technical
    complaints = await repo.get_complaints()
    updated_complaint = next(c for c in complaints if c.id == added.id)
    assert updated_complaint.category == CategoryEnum.technical
