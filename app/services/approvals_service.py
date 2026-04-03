from __future__ import annotations

import datetime

from fastapi import HTTPException, UploadFile

from app.config import settings
from app.models.api.request_models import ApprovalRequest
from app.models.api.response_models import (
    ApiResponse,
    ApprovalPreviewDataResponse,
    ApprovalPreviewListResponse,
)
from app.models.db.data_models import Approval as ApprovalDb
from app.repositories.approval_repository import ApprovalRepository
from app.services.log_service import LogService
from app.services.storage_service import StorageService


class AdminApprovalsService:
    def __init__(
        self,
        *,
        approval_repo: ApprovalRepository,
        storage_service: StorageService,
    ) -> None:
        self._approval_repo = approval_repo
        self._storage_service = storage_service

    def list_approvals(
        self,
        *,
        requester_email: str | None,
        approval_id: int | None,
        approval_type: str | None,
        is_approved: bool | None,
        page: int,
        per_page: int,
    ) -> ApprovalPreviewListResponse:
        approvals, total = self._approval_repo.get_approvals(
            approval_id=approval_id,
            approval_type=approval_type,
            is_approved=is_approved,
            requester=requester_email,
            page=page,
            per_page=per_page,
        )
        approval_previews = [
            ApprovalPreviewDataResponse(
                id=a.id,
                type=a.type,
                payload=a.payload,
                is_approved=a.is_approved,
                requester=a.requester,
                request_date=a.request_date,
                attachment_url=a.attachment_url,
            )
            for a in approvals
        ]

        return ApprovalPreviewListResponse(
            page=page, 
            per_page=per_page, 
            total=total, 
            approval_previews=approval_previews
        )

    async def add_approval(
        self,
        *,
        approval: ApprovalRequest,
        attachment: UploadFile | None,
        requester_email: str,
        timezone: datetime.tzinfo,
    ) -> ApiResponse:
        approval_db = ApprovalDb.model_validate(approval.model_dump())

        if approval_db.requester is None:
            approval_db.requester = requester_email

        if approval_db.request_date is None:
            approval_db.request_date = datetime.datetime.now(timezone).strftime(
                "%Y-%m-%d"
            )

        if attachment:
            attachment_url = self._storage_service.save_upload_public(
                settings.aws_s3_blob_bucket,
                await attachment.read(),
                original_filename=attachment.filename,
            )
            approval_db.attachment_url = attachment_url

        LogService.ADMIN.log(
            f"New approval request added by {requester_email}: {approval_db.model_dump_json()}"
        )
        self._approval_repo.add_approval(approval_db)
        return ApiResponse(message="Approval added successfully.")

    def delete_approval(
        self, *, approval_id: int, deleter_email: str
    ) -> ApiResponse:
        success = self._approval_repo.delete_approval(
            approval_id, deleter=deleter_email
        )
        if not success:
            raise HTTPException(status_code=404, detail="Approval not found.")

        LogService.ADMIN.log(
            f"Approval request {approval_id} deleted by {deleter_email}"
        )
        return ApiResponse(message="Approval deleted successfully.")

    def approve_approval(
        self, *, approval_id: int, approver_email: str
    ) -> ApprovalPreviewDataResponse:
        approval = self._approval_repo.approve_request(approval_id)
        if not approval:
            raise HTTPException(status_code=404, detail="Approval not found.")

        LogService.ADMIN.log(
            f"Approval request {approval_id} approved by {approver_email}"
        )
        return ApprovalPreviewDataResponse(
            id=approval.id,
            type=approval.type,
            payload=approval.payload,
            is_approved=approval.is_approved,
            requester=approval.requester,
            request_date=approval.request_date,
            attachment_url=approval.attachment_url,
        )

    def reject_approval(
        self, *, approval_id: int, rejector_email: str
    ) -> ApprovalPreviewDataResponse:
        approval = self._approval_repo.reject_request(approval_id)
        if not approval:
            raise HTTPException(status_code=404, detail="Approval not found.")

        LogService.ADMIN.log(
            f"Approval request {approval_id} rejected by {rejector_email}"
        )
        return ApprovalPreviewDataResponse(
            id=approval.id,
            type=approval.type,
            payload=approval.payload,
            is_approved=approval.is_approved,
            requester=approval.requester,
            request_date=approval.request_date,
            attachment_url=approval.attachment_url,
        )

