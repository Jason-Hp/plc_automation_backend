from fastapi import APIRouter, UploadFile, File, Form

from app.dependencies import public_jobs_service
from app.models.api.response_models import ApiResponse, JobPreviewResponse, JobResponse

router = APIRouter(prefix="/jobs", tags=["jobs"])

@router.get("/", response_model=list[JobPreviewResponse])
async def get_job_postings() -> list[JobPreviewResponse]:
    return public_jobs_service.list_job_postings()


@router.get("/{job_id}", response_model=JobResponse)
async def get_job_posting(job_id: int) -> JobResponse:
    return public_jobs_service.get_job_posting(job_id=job_id)

#DEPRECATED: Might be handled entirely on the frontend
@router.post("/{job_id}/application", response_model=ApiResponse)
async def submit_job_application(
    job_id: int,
    payload: str = Form(...),
    resume: UploadFile = File(...),
) -> ApiResponse:
    return await public_jobs_service.submit_job_application(
        job_id=job_id, payload=payload, resume=resume
    )
