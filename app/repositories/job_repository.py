from __future__ import annotations

from typing import List, Optional

from app.schemas import Job, JobPreview


class JobRepository:
    """
    In-memory mock repository for jobs.
    Replace with real database access when implementing persistence.
    """

    def __init__(self) -> None:
        self._jobs: List[Job] = []

    def get_all_jobs(self) -> list[JobPreview]:
        """
        Return a list of job previews (lightweight projection of Job).
        """
        return [
            JobPreview(
                id=job.id,
                title=job.title,
                country=job.country,
                location=job.location,
                job_type=job.job_type,
                posted_date=job.posted_date,
            )
            for job in self._jobs
        ]

    def get_job_by_id(self, job_id: int) -> Optional[Job]:
        for job in self._jobs:
            if job.id == job_id:
                return job
        return None

    def add_job(self, job: Job) -> Job:
        """
        Add a new job. If no id is provided, assign a simple incremental id.
        """
        if job.id is None:
            next_id = (max((j.id or 0) for j in self._jobs) + 1) if self._jobs else 1
            job.id = next_id

        self._jobs.append(job)
        return job

    def update_job(self, job_id: int, job: Job) -> None:
        for index, current in enumerate(self._jobs):
            if current.id == job_id:
                self._jobs[index] = job
                return

    def delete_job(self, job_id: int) -> None:
        self._jobs = [job for job in self._jobs if job.id != job_id]
