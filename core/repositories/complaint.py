from sqlalchemy import select
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker

from core.dependencies import settings
from core.entities.enums import CategoryEnum
from core.models.base import Base
from core.models.complaint import ComplaintModel
from core.schemas.complaint import Complaint


class ComplaintRepository:
    def __init__(self):
        self.engine = create_async_engine(url=settings.DATABASE_URL)
        self.session = async_sessionmaker(
            self.engine, expire_on_commit=False, class_=AsyncSession)

    async def init_db(self):
        async with self.engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
            await conn.run_sync(Base.metadata.create_all)

    async def add_complaint(self, complaint: Complaint) -> ComplaintModel:
        complaint_orm: ComplaintModel = ComplaintModel(
            text=complaint.text,
            status=complaint.status,
            timestamp=complaint.timestamp,
            sentiment=complaint.sentiment,
            category=complaint.category
        )

        async with self.session() as session:
            session.add(complaint_orm)
            await session.commit()
        return complaint_orm

    async def get_complaints(self):
        async with self.session() as session:
            result = await session.execute(
                select(ComplaintModel)
            )
            return result.scalars().all()

    async def update_complaint_category(self, complaint_id: int,
                                        category: CategoryEnum) -> CategoryEnum:
        async with self.session() as session:
            result = await session.execute(
                select(ComplaintModel).where(ComplaintModel.id == complaint_id)
            )
            complaint_obj = result.scalars().first()
            if complaint_obj is None:
                raise ValueError(f'Complaint {complaint_id=} not found')

            complaint_obj.category = category
            await session.commit()

            return complaint_obj.category
