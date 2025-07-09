import pytest
from unittest.mock import AsyncMock, patch
from core.schemas.complaint import ComplaintCreate
from core.services.sentiment_analysis_service import SentimentAnalysisService
from core.entities.enums import SentimentEnum


@pytest.mark.asyncio
async def test_build_complaint_success():
    complaint_text = "Это тестовое сообщение"
    complaint_create = ComplaintCreate(text=complaint_text)

    mock_response = AsyncMock()
    mock_response.json.return_value = {'sentiment': 'positive'}

    mock_client = AsyncMock()
    mock_client.__aenter__ = AsyncMock(return_value=mock_client)
    mock_client.__aexit__ = AsyncMock(return_value=None)
    mock_client.post = AsyncMock(return_value=mock_response)

    with patch('core.services.sentiment_analysis_service.AsyncClient', return_value=mock_client):
        complaint = await SentimentAnalysisService.build_complaint(complaint_create)

    assert complaint.text == complaint_text
    assert complaint.sentiment == SentimentEnum.positive


@pytest.mark.asyncio
async def test_analyze_sentiment_called():
    mock_response = AsyncMock()
    mock_response.json.return_value = {'sentiment': 'negative'}

    mock_client = AsyncMock()
    mock_client.__aenter__.return_value = mock_client
    mock_client.__aexit__.return_value = None
    mock_client.post = AsyncMock(return_value=mock_response)

    with patch('core.services.sentiment_analysis_service.AsyncClient', return_value=mock_client):
        complaint_create = ComplaintCreate(text="Тестовое сообщение")
        result = await SentimentAnalysisService.analyze_sentiment(complaint_create)

        sentiment_str = result.get('sentiment')
        sentiment_enum = SentimentEnum(sentiment_str)

        assert isinstance(sentiment_enum, SentimentEnum)
        assert sentiment_enum == SentimentEnum.negative
