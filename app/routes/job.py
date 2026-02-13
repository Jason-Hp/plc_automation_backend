from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from app.schemas import JobPreview, Job, ApiResponse, JobApplicationRequest
from app.repositories.job_repository import JobRepository
from app.utils.translation_util import translate_text
from app.services.email_service import EmailService
from app.services.storage_service import StorageService
from app.config import settings
from app.utils.formatter_util import format_form
from app.routes.forms import ensure_digits

router = APIRouter(prefix="/jobs", tags=["jobs"])
job_repo = JobRepository()
email_service = EmailService()
storage_service = StorageService()

@router.get("/", response_model=list[JobPreview])
async def get_job_postings() -> list[JobPreview]:
    jobs = job_repo.get_all_jobs()
    return jobs

@router.get("/{job_id}", response_model=Job)
async def get_job_posting(job_id: int) -> Job:
    job = job_repo.get_job_by_id(job_id)
    job.description = translate_text(job.description)
    job.requirements = translate_text(job.requirements)
    job.responsibilities = translate_text(job.responsibilities)
    return job

@router.post("/{job_id}/application", response_model=ApiResponse)
async def submit_job_application(
    payload: JobApplicationRequest,
    job_id: int,
    resume: UploadFile = File(...),
) -> ApiResponse:
    ensure_digits(payload.phone, "phone number")
    resume_bytes = await resume.read()
    storage_service.save_upload(resume.filename, resume_bytes)

    job = job_repo.get_job_by_id(job_id)

    email_service.send(
        subject=f"Apply for [{job.title}]",
        body="",
        html_body=format_form(payload),
        to_addrs=[settings.hr_email],
        attachments=[(resume.filename, resume_bytes, resume.content_type or "application/octet-stream")],
    )

    return ApiResponse(message=translate_text("Application submitted successfully."))