import pytest
import pytest_asyncio
from core.entities.enums import CategoryEnum
from core.schemas.complaint import ComplaintCreate
from core.services.category_analysis_service import CategoryAnalysisService


@pytest.mark.asyncio
async def test_analyze_category_technical(monkeypatch):
    complaint_text = "we have some issues with your service"
    complaint = ComplaintCreate(text=complaint_text)

    class MockClient:
        class Chat:
            @staticmethod
            def complete(model, messages):
                class Response:
                    choices = [type('obj', (), {'message': type('obj', (), {'content': 'техническая'})})()]
                return Response()

        chat = Chat()

    monkeypatch.setattr('mistralai.Mistral', lambda api_key: MockClient())

    result = await CategoryAnalysisService.analyze_category(complaint)
    assert result == CategoryEnum.technical


@pytest.mark.asyncio
async def test_analyze_category_payment(monkeypatch):
    complaint_text = "can't pay for my subscription"
    complaint = ComplaintCreate(text=complaint_text)

    class MockClient:
        class Chat:
            @staticmethod
            def complete(model, messages):
                class Response:
                    choices = [type('obj', (), {'message': type('obj', (), {'content': 'оплата'})})()]
                return Response()

        chat = Chat()

    monkeypatch.setattr('mistralai.Mistral', lambda api_key: MockClient())

    result = await CategoryAnalysisService.analyze_category(complaint)
    assert result == CategoryEnum.payment


@pytest.mark.asyncio
async def test_analyze_category_other(monkeypatch):
    complaint_text = "hello guys how are you?"
    complaint = ComplaintCreate(text=complaint_text)

    class MockClient:
        class Chat:
            @staticmethod
            def complete(model, messages):
                class Response:
                    choices = [type('obj', (), {'message': type('obj', (), {'content': 'неизвестно'})})()]
                return Response()

        chat = Chat()

    monkeypatch.setattr('mistralai.Mistral', lambda api_key: MockClient())

    result = await CategoryAnalysisService.analyze_category(complaint)
    assert result == CategoryEnum.other
