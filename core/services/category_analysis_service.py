from mistralai import Mistral

from core.dependencies import settings
from core.entities.enums import CategoryEnum
from core.schemas.complaint import ComplaintCreate


class CategoryAnalysisService:
    @staticmethod
    async def analyze_category(complaint: ComplaintCreate) -> CategoryEnum:
        client = Mistral(api_key=settings.MISTRAL_API_KEY)
        model = 'open-mistral-nemo'
        prompt = {
                    'role': 'user',
                    'content': f'Определи категорию жалобы: {complaint.text}.'
                             f'Ответь одним словом. [техническая, оплата, другое]',
        }
        category = client.chat.complete(
            model=model,
            messages=[prompt]
        ).choices[0].message.content

        try:
            result = CategoryEnum(f'{category}'.lower())
        except ValueError:
            result = CategoryEnum.other
        return result
