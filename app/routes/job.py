import json

from fastapi import APIRouter, UploadFile, File, HTTPException, Form
from pydantic import ValidationError

from app.schemas import ApiResponse, Job, JobApplicationRequest, JobPreview
from app.dependencies import email_service, job_repo, storage_service
from app.utils.translation_util import translate_text
from app.config import settings
from app.utils.formatter_util import format_form
from app.routes.forms import ensure_digits

router = APIRouter(prefix="/jobs", tags=["jobs"])

@router.get("/", response_model=list[JobPreview])
async def get_job_postings() -> list[JobPreview]:
    jobs = job_repo.get_all_jobs()
    return jobs


@router.get("/{job_id}", response_model=Job)
async def get_job_posting(job_id: int) -> Job:
    job = job_repo.get_job_by_id(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")

    job.description = translate_text(job.description)
    job.requirements = translate_text(job.requirements)
    job.responsibilities = translate_text(job.responsibilities)
    return job


@router.post("/{job_id}/application", response_model=ApiResponse)
async def submit_job_application(
    job_id: int,
    payload: str = Form(...),
    resume: UploadFile = File(...),
) -> ApiResponse:
    try:
        parsed_payload = JobApplicationRequest.model_validate_json(payload)
    except ValidationError as exc:
        raise HTTPException(status_code=422, detail=json.loads(exc.json())) from exc

    ensure_digits(parsed_payload.phone, "phone number")

    job = job_repo.get_job_by_id(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")

    resume_bytes = await resume.read()
    storage_service.save_upload(resume.filename, resume_bytes)

    email_service.send(
        subject=f"Apply for [{job.title}]",
        body="",
        html_body=format_form(parsed_payload),
        to_addrs=[settings.hr_email],
        attachments=[(resume.filename, resume_bytes, resume.content_type or "application/octet-stream")],
    )

    return ApiResponse(message=translate_text("Application submitted successfully."))
