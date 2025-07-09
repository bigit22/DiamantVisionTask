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
            sentiment_str = result.get('sentiment', 'unknown')

            if not isinstance(sentiment_str, str):
                sentiment_str = 'unknown'

            try:
                sentiment_enum = SentimentEnum(sentiment_str)
            except ValueError:
                sentiment_enum = SentimentEnum.unknown

        except Exception as e:
            print(f'Exception occurred: {e}')
            traceback.print_exc()
            sentiment_str = SentimentEnum.unknown

        return Complaint(
            text=complaint.text,
            status=StatusEnum.open,
            timestamp=None,
            sentiment=sentiment_str,
            category=CategoryEnum.other,
        )

    @staticmethod
    async def analyze_sentiment(complaint: ComplaintCreate):
        print('INFO:     analyze_sentiment was called from the REAL class')

        async with AsyncClient(timeout=20.0) as client:
            result = await client.post(
                url=settings.SENTIMENT_ANALYSIS_URL,
                headers={'apikey': settings.APILAYER_API_KEY},
                json={'text': complaint.text},
            )

        return result.json()
