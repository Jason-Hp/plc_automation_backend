from __future__ import annotations

from typing import List, Optional

from fastapi import HTTPException

from app.models.db.data_models import Approval
from app.utils.supabase_client_util import get_supabase_client


class ApprovalRepository:
    """
    Repository for managing approval requests.
    Placeholder using in-memory list. Replace with SQL queries against approvals.
    """

    def __init__(self) -> None:
        self._approvals = []
        self._id_counter = 1
        self._client = get_supabase_client()

    def add_approval(self, approval: Approval) -> Approval:
        """Create a new approval request."""
        if self._client is not None:
            row = approval.model_dump(exclude={"id"})
            insert_resp = self._client.table("approvals").insert(row).execute()
            inserted = (insert_resp.data or [])[:1]
            if inserted and inserted[0].get("id") is not None:
                approval.id = inserted[0]["id"]
            return approval

        if approval.id is None:
            approval.id = self._id_counter
            self._id_counter += 1
        self._approvals.append(approval)
        return approval

    def get_approval_by_id(self, approval_id: int) -> Optional[Approval]:
        """Retrieve an approval by ID."""
        if self._client is not None:
            resp = (
                self._client.table("approvals")
                .select("*")
                .eq("id", approval_id)
                .limit(1)
                .execute()
            )
            rows = resp.data or []
            return Approval.model_validate(rows[0]) if rows else None

        for approval in self._approvals:
            if approval.id == approval_id:
                return approval
        return None

    def get_all_approvals(self) -> List[Approval]:
        """Retrieve all approval requests."""
        return self._approvals.copy()

    def get_approvals_by_type(self, approval_type: str) -> List[Approval]:
        """Retrieve approvals filtered by type."""
        return [a for a in self._approvals if a.type == approval_type]

    def get_approvals_by_status(self, is_approved: bool) -> List[Approval]:
        """Retrieve approvals filtered by approval status."""
        return [a for a in self._approvals if a.is_approved == is_approved]

    def get_pending_approvals(self) -> List[Approval]:
        """Retrieve all pending (unapproved) requests."""
        return self.get_approvals_by_status(False)

    def get_approved_approvals(self) -> List[Approval]:
        """Retrieve all approved requests."""
        return self.get_approvals_by_status(True)
    
    def get_approvals_by_requester(self, requester: str) -> List[Approval]:
        """Retrieve approvals filtered by requester."""
        return [a for a in self._approvals if a.requester == requester]
    
    def get_approvals(
        self,
        approval_id: Optional[int] = None,
        requester: Optional[str] = None,
        approval_type: Optional[str] = None,
        is_approved: Optional[bool] = None,
        page: int = 1,
        per_page: int = 10
    ) -> tuple[List[Approval], int]:
        """
        Unified filter method for approvals.
        All parameters are optional and ignored if None.
        Returns all approvals matching the provided filters.
        """
        if self._client is not None:
            base = (
                self._client.table("approvals")
                .select("*")
            )
            if approval_id is not None:
                base = base.eq("id", approval_id)
            if requester is not None:
                base = base.eq("requester", requester)
            if approval_type is not None:
                base = base.eq("type", approval_type)
            if is_approved is not None:
                base = base.eq("is_approved", is_approved)

            total_resp = base.execute()
            total = len(total_resp.data or [])

            start = (page - 1) * per_page
            end = start + per_page - 1
            slice_resp = (
                self._client.table("approvals")
                .select("*")
            )
            if approval_id is not None:
                slice_resp = slice_resp.eq("id", approval_id)
            if requester is not None:
                slice_resp = slice_resp.eq("requester", requester)
            if approval_type is not None:
                slice_resp = slice_resp.eq("type", approval_type)
            if is_approved is not None:
                slice_resp = slice_resp.eq("is_approved", is_approved)
            slice_resp = slice_resp.order("id", desc=False).range(start, end).execute()

            approvals = [Approval.model_validate(r) for r in (slice_resp.data or [])]
            return approvals, total

        results = self._approvals.copy()
        
        if approval_id is not None:
            results = [a for a in results if a.id == approval_id]
        
        if requester is not None:
            results = [a for a in results if a.requester == requester]
        
        if approval_type is not None:
            results = [a for a in results if a.type == approval_type]

        if is_approved is not None:
            results = [a for a in results if a.is_approved == is_approved]
        
        start = (page - 1) * per_page
        end = start + per_page
        return results[start:end], len(results)
    
    def delete_approval(self, approval_id: int, deleter: str) -> bool:
        """Delete an approval request by ID."""
        if self._client is not None:
            approval = self.get_approval_by_id(approval_id)
            if approval is None:
                return False
            if approval.requester != deleter:
                raise HTTPException(status_code=403, detail="Only the requester can delete this approval")
            self._client.table("approvals").delete().eq("id", approval_id).execute()
            return True

        for i, approval in enumerate(self._approvals):
            if approval.id == approval_id:
                if approval.requester != deleter:
                    raise HTTPException(status_code=403, detail="Only the requester can delete this approval")
                del self._approvals[i]
                return True
        return False

    def approve_request(self, approval_id: int) -> Optional[Approval]:
        """Mark an approval request as approved."""
        if self._client is not None:
            updated = (
                self._client.table("approvals")
                .update({"is_approved": True})
                .eq("id", approval_id)
                .execute()
            )
            rows = updated.data or []
            if rows:
                return Approval.model_validate(rows[0])
            # If supabase returns no rows, fall back to fetch.
            return self.get_approval_by_id(approval_id)

        approval = self.get_approval_by_id(approval_id)
        if approval:
            approval.is_approved = True
            return approval
        return None

    def reject_request(self, approval_id: int) -> Optional[Approval]:
        """Reject/delete an approval request."""
        if self._client is not None:
            updated = (
                self._client.table("approvals")
                .update({"is_approved": False})
                .eq("id", approval_id)
                .execute()
            )
            rows = updated.data or []
            if rows:
                return Approval.model_validate(rows[0])
            return self.get_approval_by_id(approval_id)

        approval = self.get_approval_by_id(approval_id)
        if approval:
            approval.is_approved = False
            return approval
        return None
