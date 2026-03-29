from __future__ import annotations

from fastapi import HTTPException, UploadFile

from app.config import settings
from app.models.api.request_models import JobApplicationRequest
from app.models.api.response_models import ApiResponse, JobPreviewResponse, JobResponse, JobPreviewListResponse
from app.repositories.job_repository import JobRepository
from app.services.email_service import EmailService
from app.utils.formatter_util import format_form
from app.utils.translation_util import translate_text


class PublicJobsService:
    def __init__(
        self,
        *,
        job_repo: JobRepository,
        email_service: EmailService,
    ) -> None:
        self._job_repo = job_repo
        self._email_service = email_service

    def _ensure_digits(self, value: str, field_name: str) -> None:
        if not value.isdigit():
            error_message = translate_text(f"{field_name} must contain only digits")
            raise HTTPException(status_code=400, detail=error_message)

    def list_job_postings(self, page: int = 1, per_page: int = 10) -> JobPreviewListResponse:
        jobs = self._job_repo.get_all_jobs()
        total = len(jobs)
        start = (page - 1) * per_page
        end = start + per_page
        sliced_jobs = jobs[start:end]
        
        previews = [
            JobPreviewResponse(
                id=job.id,
                title=job.title,
                country=job.country,
                location=job.location,
                job_type=job.job_type,
                posted_date=job.posted_date,
            )
            for job in sliced_jobs
        ]
        return JobPreviewListResponse(
            page=page,
            per_page=per_page,
            total=total,
            job_previews=previews
        )

    def get_job_posting(self, *, job_id: int) -> JobResponse:
        job = self._job_repo.get_job_by_id(job_id)
        if not job:
            raise HTTPException(status_code=404, detail="Job not found")

        translated = job.model_copy(deep=True)
        translated.description = translate_text(translated.description)
        translated.requirements = translate_text(translated.requirements)
        translated.responsibilities = translate_text(translated.responsibilities)
        return JobResponse.model_validate(translated.model_dump())

    async def submit_job_application(
        self,
        *,
        job_id: int,
        payload: JobApplicationRequest,
        resume: UploadFile,
    ) -> ApiResponse:
        self._ensure_digits(payload.phone, "phone number")

        job = self._job_repo.get_job_by_id(job_id)
        if not job:
            raise HTTPException(status_code=404, detail="Job not found")

        resume_bytes = await resume.read()

        self._email_service.send(
            subject=f"Apply for [{job.title}]",
            body="",
            html_body=format_form(payload),
            to_addrs=[settings.hr_email],
            attachments=[
                (
                    resume.filename,
                    resume_bytes,
                    resume.content_type or "application/octet-stream",
                )
            ],
        )

        return ApiResponse(
            message=translate_text("Application submitted successfully.")
        )

