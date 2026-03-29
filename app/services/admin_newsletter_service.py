from __future__ import annotations

import json

from fastapi import UploadFile

from app.models.api.request_models import NewsLetterContentRequest
from app.models.api.response_models import ApiResponse
from app.repositories.newsletter_subscribers_repository import (
    NewsletterRepository,
)
from app.services.email_service import EmailService
from app.services.log_service import LogService


class AdminNewsletterService:
    def __init__(
        self,
        *,
        newsletter_repo: NewsletterRepository,
        email_service: EmailService,
    ) -> None:
        self._newsletter_repo = newsletter_repo
        self._email_service = email_service

    async def broadcast_newsletter(
        self,
        *,
        payload: NewsLetterContentRequest,
        attachments: list[UploadFile],
        actor_email: str,
    ) -> ApiResponse:
        subscribers = self._newsletter_repo.get_all_subscribers()
        bcc_addrs = list(subscribers)

        email_attachments = None
        if attachments:
            email_attachments = []
            for attachment in attachments:
                email_attachments.append(
                    (
                        attachment.filename,
                        await attachment.read(),
                        attachment.content_type
                        or "application/octet-stream",
                    )
                )

        self._email_service.send(
            subject=payload.subject,
            body="",
            html_body=payload.content,
            to_addrs=None,
            cc_addrs=None,
            bcc_addrs=bcc_addrs,
            attachments=email_attachments,
        )

        LogService.ADMIN.log(
            json.dumps(
                {
                    "event": "ADMIN_NEWSLETTER_BROADCASTED",
                    "actor": actor_email,
                    "subject": payload.subject,
                    "recipients": len(bcc_addrs),
                    "attachments": len(email_attachments) if email_attachments else 0,
                }
            )
        )

        return ApiResponse(message="Newsletter broadcasted.")

