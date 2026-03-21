from __future__ import annotations

from typing import Optional

from app.models.db.data_models import Job
from app.utils.supabase_client_util import get_supabase_client


class JobRepository:
    """
    Repository for jobs.
    """

    def __init__(self) -> None:
        self._client = get_supabase_client()
        if self._client is None:
            raise RuntimeError("Supabase client is not configured.")

    def get_all_jobs(self) -> list[Job]:
        response = (
            self._client.table("jobs")
            .select("*")
            .order("id", desc=False)
            .execute()
        )
        return [Job.model_validate(r) for r in response.data or []]

    def get_job_by_id(self, job_id: int) -> Optional[Job]:
        response = (
            self._client.table("jobs")
            .select("*")
            .eq("id", job_id)
            .limit(1)
            .execute()
        )
        rows = response.data or []
        return Job.model_validate(rows[0]) if rows else None

    def add_job(self, job: Job) -> Job:
        """
        Add a new job.
        """
        row = job.model_dump(exclude={"id"})
        insert_resp = self._client.table("jobs").insert(row).execute()
        inserted = (insert_resp.data or [])[:1]
        if inserted and inserted[0].get("id") is not None:
            job.id = inserted[0]["id"]
        return job

    def update_job(self, job_id: int, job: Job) -> None:
        self._client.table("jobs").update(job.model_dump(exclude={"id"})).eq("id", job_id).execute()

    def delete_job(self, job_id: int) -> None:
        self._client.table("jobs").delete().eq("id", job_id).execute()
