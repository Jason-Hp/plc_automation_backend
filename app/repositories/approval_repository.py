from __future__ import annotations

from typing import List, Optional

from fastapi import HTTPException

from app.schemas import Approval, ApprovalResponse


class ApprovalRepository:
    """
    Repository for managing approval requests.
    Placeholder using in-memory list. Replace with SQL queries against tbl_approvals.
    """

    def __init__(self) -> None:
        self._approvals = []
        self._id_counter = 1

    def add_approval(self, approval: Approval) -> Approval:
        """Create a new approval request."""
        if approval.id is None:
            approval.id = self._id_counter
            self._id_counter += 1
        self._approvals.append(approval)
        return approval

    def get_approval_by_id(self, approval_id: int) -> Optional[Approval]:
        """Retrieve an approval by ID."""
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
    ) -> ApprovalResponse:
        """
        Unified filter method for approvals.
        All parameters are optional and ignored if None.
        Returns all approvals matching the provided filters.
        """
        results = self._approvals.copy()
        
        if approval_id is not None:
            results = [a for a in results if a.id == approval_id]
        
        if requester is not None:
            results = [a for a in results if a.requester == requester]
        
        if approval_type is not None:
            results = [a for a in results if a.type == approval_type]
        
        start = (page - 1) * per_page
        end = start + per_page
        return ApprovalResponse(
            page=page,
            per_page=per_page,
            total=len(results),
            approvals=results[start:end]
        )   
    
    def delete_approval(self, approval_id: int, deleter: str) -> bool:
        """Delete an approval request by ID."""
        for i, approval in enumerate(self._approvals):
            if approval.id == approval_id:
                if approval.requester != deleter:
                    raise HTTPException(status_code=403, detail="Only the requester can delete this approval")
                del self._approvals[i]
                return True
        return False

    def approve_request(self, approval_id: int) -> Optional[Approval]:
        """Mark an approval request as approved."""
        approval = self.get_approval_by_id(approval_id)
        if approval:
            approval.is_approved = True
            return approval
        return None

    def reject_request(self, approval_id: int) -> Optional[Approval]:
        """Reject/delete an approval request."""
        approval = self.get_approval_by_id(approval_id)
        if approval:
            approval.is_approved = False
            return approval
        return None
