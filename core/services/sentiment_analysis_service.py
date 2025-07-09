import traceback

from httpx import AsyncClient

from core.dependencies import settings
from core.entities.enums import StatusEnum, SentimentEnum, CategoryEnum
from core.schemas.complaint import Complaint, ComplaintCreate


class SentimentAnalysisService:
    @staticmethod
    async def build_complaint(complaint: ComplaintCreate) -> Complaint:
        try:
            result = await SentimentAnalysisService.analyze_sentiment(complaint)

            sentiment_str = result.get('sentiment')
            if not isinstance(sentiment_str, str):
                sentiment_str = 'unknown'

            try:
                sentiment_enum = SentimentEnum(sentiment_str)
            except ValueError:
                sentiment_enum = SentimentEnum.unknown

            cmp = Complaint(
                text=complaint.text,
                status=StatusEnum.open,
                timestamp=None,
                sentiment=sentiment_str,
                category=CategoryEnum.other,
            )
            return cmp
        except Exception as e:
            print(f'Exception occurred: {e}')
            traceback.print_exc()
            cmp = Complaint(
                text=complaint.text,
                status=StatusEnum.open,
                timestamp=None,
                sentiment=SentimentEnum.unknown,
                category=CategoryEnum.other,
            )
            return cmp

    @staticmethod
    async def analyze_sentiment(complaint: ComplaintCreate):
        print('INFO:     analyze_sentiment was called from the REAL class')

        async with AsyncClient() as client:
            result = await client.post(
                url=settings.SENTIMENT_ANALYSIS_URL,
                headers={'apikey': settings.APILAYER_API_KEY},
                json={'text': complaint.text},
            )

        return await result.json()
