from __future__ import annotations

from typing import List, Optional

from app.models.db.data_models import Job
from app.utils.supabase_client_util import get_supabase_client


class JobRepository:
    """
    In-memory mock repository for jobs.
    Replace with real database access when implementing persistence.
    """

    def __init__(self) -> None:
        self._jobs: List[Job] = []
        self._client = get_supabase_client()

    def get_all_jobs(self) -> list[Job]:
        if self._client is None:
            return self._jobs

        response = (
            self._client.table("tbl_job")
            .select("*")
            .order("id", desc=False)
            .execute()
        )
        return [Job.model_validate(r) for r in response.data or []]

    def get_job_by_id(self, job_id: int) -> Optional[Job]:
        if self._client is None:
            for job in self._jobs:
                if job.id == job_id:
                    return job
            return None

        response = (
            self._client.table("tbl_job")
            .select("*")
            .eq("id", job_id)
            .limit(1)
            .execute()
        )
        rows = response.data or []
        return Job.model_validate(rows[0]) if rows else None

    def add_job(self, job: Job) -> Job:
        """
        Add a new job. If no id is provided, assign a simple incremental id.
        """
        if self._client is None:
            if job.id is None:
                next_id = (max((j.id or 0) for j in self._jobs) + 1) if self._jobs else 1
                job.id = next_id
            self._jobs.append(job)
            return job

        row = job.model_dump(exclude={"id"})
        insert_resp = self._client.table("tbl_job").insert(row).execute()
        inserted = (insert_resp.data or [])[:1]
        if inserted and inserted[0].get("id") is not None:
            job.id = inserted[0]["id"]
        return job

    def update_job(self, job_id: int, job: Job) -> None:
        if self._client is None:
            for index, current in enumerate(self._jobs):
                if current.id == job_id:
                    self._jobs[index] = job
                    return
            return

        self._client.table("tbl_job").update(job.model_dump(exclude={"id"})).eq("id", job_id).execute()

    def delete_job(self, job_id: int) -> None:
        if self._client is None:
            self._jobs = [job for job in self._jobs if job.id != job_id]
            return

        self._client.table("tbl_job").delete().eq("id", job_id).execute()
