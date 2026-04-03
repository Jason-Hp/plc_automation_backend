import json
from fastapi import APIRouter, UploadFile, File, Query, Form

from app.dependencies import job_service
from app.models.api.request_models import JobApplicationRequest
from app.models.api.response_models import (
    ApiResponse,
    JobResponse,
    JobPreviewListResponse,
)

router = APIRouter(prefix="/jobs", tags=["jobs"])


@router.get("/", response_model=JobPreviewListResponse)
async def get_job_postings(
    page: int = Query(1, ge=1), per_page: int = Query(10, ge=1, le=100)
) -> JobPreviewListResponse:
    return job_service.list_job_postings(page=page, per_page=per_page)


@router.get("/{job_id}", response_model=JobResponse)
async def get_job_posting(job_id: int) -> JobResponse:
    return job_service.get_job_posting(job_id=job_id)

#DEPRECATED: Might be handled entirely on the frontend
@router.post("/{job_id}/application", response_model=ApiResponse)
async def submit_job_application(
    job_id: int,
    payload: str = Form(...),
    resume: UploadFile = File(...),
) -> ApiResponse:
    parsed_payload = JobApplicationRequest.model_validate(json.loads(payload))
    return await job_service.submit_job_application(
        job_id=job_id, payload=parsed_payload, resume=resume
    )
