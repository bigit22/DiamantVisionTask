from core.schemas.complaint import ComplaintResponse, Complaint


def build_response(
        complaint_id: int,
        complaint: Complaint):
    response = ComplaintResponse(
        id=complaint_id,
        status=complaint.status,
        sentiment=complaint.sentiment,
        category=complaint.category
    )

    return response
