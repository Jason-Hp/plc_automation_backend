from __future__ import annotations

from fastapi import HTTPException, UploadFile
import datetime
import pytz

from app.config import settings
from app.models.api.request_models import (
    EnquiryRequest,
    NewsletterRequest,
    QuoteWithProductPreviewsWithQuantityRequest,
)
from app.models.api.response_models import ApiResponse
from app.repositories.newsletter_subscribers_repository import (
    NewsletterRepository,
)
from app.services.email_service import EmailService
from app.services.quotes_service import QuotesService
from app.services.log_service import LogService
from app.utils.formatter_util import format_form
from app.utils.translation_util import translate_text


class FormsService:
    def __init__(
        self,
        *,
        email_service: EmailService,
        newsletter_repo: NewsletterRepository,
        quotes_service: QuotesService,
    ) -> None:
        self._email_service = email_service
        self._newsletter_repo = newsletter_repo
        self._quotes_service = quotes_service

    def _ensure_digits(self, value: str, field_name: str) -> None:
        if not value.isdigit():
            error_message = translate_text(f"{field_name} must contain only digits")
            raise HTTPException(status_code=400, detail=error_message)

    async def submit_enquiry(self, *, payload: EnquiryRequest) -> ApiResponse:
        self._ensure_digits(payload.phone, "phone number")
        if payload.created_at == None:
            payload.created_at = datetime.datetime.now(pytz.timezone(settings.timezone)).strftime("%Y-%m-%d %H:%M:%S")
        self._email_service.send(
            subject=f"Contact Us by {payload.name}",
            body="",
            html_body=format_form(payload),
            to_addrs=[settings.quote_and_enquiry_email],
        )
        return ApiResponse(
            message=translate_text("Your query has been submitted successfully.")
        )

    async def submit_quote(
        self,
        *,
        payload: QuoteWithProductPreviewsWithQuantityRequest,
        attachment: UploadFile | None,
    ) -> ApiResponse:
        self._ensure_digits(payload.phone, "phone number")
        self._quotes_service.create_quote(request=payload)

        attachments = (
            [
                (
                    attachment.filename,
                    await attachment.read(),
                    attachment.content_type
                    or "application/octet-stream",
                )
            ]
            if attachment
            else None
        )

        self._email_service.send(
            subject=f"Enquiry by {payload.name}",
            body="",
            html_body=format_form(payload),
            to_addrs=[settings.quote_and_enquiry_email],
            attachments=attachments,
        )

        return ApiResponse(
            message=translate_text("Your enquiry has been submitted successfully.")
        )

    async def subscribe_newsletter(
        self, *, payload: NewsletterRequest
    ) -> ApiResponse:
        if self._newsletter_repo.is_subscribed(payload.email):
            raise HTTPException(
                status_code=409, detail=translate_text("You are already subscribed.")
            )

        self._newsletter_repo.subscribe(payload.email)

        admin_html = f"<p>New subscriber: {payload.email}</p>"
        user_html = (
            "<p>Thanks for subscribing to PLC Automation updates.</p>"
            "<p>We will share new blogs and videos with you soon.</p>"
        )

        self._email_service.send(
            subject=f"Subscribe by {payload.email}",
            html_body=admin_html,
            to_addrs=[settings.admin_email],
            body=""
        )
        self._email_service.send(
            subject="Thanks for subscribing",
            html_body=user_html,
            to_addrs=[payload.email],
            body=""
        )

        LogService.ADMIN.log(f"{payload.email} subscribed to newsletter")

        return ApiResponse(message=translate_text("Thank you for subscribing."))

