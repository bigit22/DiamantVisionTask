from sqlalchemy import Enum
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime, timezone

from core.entities.enums import StatusEnum, SentimentEnum, CategoryEnum
from core.models.base import Base


class ComplaintModel(Base):
    __tablename__ = 'complaints'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    text: Mapped[str] = mapped_column(nullable=False)
    status: Mapped[StatusEnum] = mapped_column(Enum(StatusEnum), default=StatusEnum.open)
    timestamp: Mapped[datetime] = mapped_column(default=datetime.now(timezone.utc))
    sentiment: Mapped[SentimentEnum] = mapped_column(Enum(SentimentEnum))
    category: Mapped[CategoryEnum] = mapped_column(Enum(CategoryEnum))
