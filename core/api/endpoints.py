from fastapi import APIRouter

from core.repositories.complaint import ComplaintRepository
from core.schemas.complaint import ComplaintCreate, ComplaintResponse
from core.services.complaint_pipeline import ComplaintPipeline
from core.utils import build_response

router = APIRouter()


@router.post('/complaint')
async def post_complaint(complaint: ComplaintCreate) -> ComplaintResponse:
    pipeline: ComplaintPipeline = ComplaintPipeline(complaint)

    #  1
    await pipeline.send_complaint()

    #  2
    await pipeline.save_into_db()

    #  3
    await pipeline.analyze_category_and_save()

    return build_response(pipeline.complaint_id, pipeline.complaint)


@router.get('/complaints')
async def get_complaints():
    orm = ComplaintRepository()
    result = await orm.get_complaints()
    return result
