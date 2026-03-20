from __future__ import annotations

from app.models.db.data_models import Job
from app.repositories.job_repository import JobRepository


class AdminJobService:
    def __init__(self, *, job_repo: JobRepository) -> None:
        self._job_repo = job_repo

    def upload_job(self, job: Job) -> None:
        self._job_repo.add_job(job)

    def update_job(self, job_id: int, job: Job) -> None:
        job.id = job_id
        self._job_repo.update_job(job_id, job)

    def delete_job(self, job_id: int) -> None:
        self._job_repo.delete_job(job_id)

