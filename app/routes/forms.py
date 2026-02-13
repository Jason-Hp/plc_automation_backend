from __future__ import annotations

import json

from fastapi import APIRouter, File, Form, HTTPException, UploadFile
from pydantic import ValidationError

from app.config import settings
from app.dependencies import email_service, newsletter_repo
from app.schemas import (
    ApiResponse,
    EnquiryRequest,
    NewsletterRequest,
    QuoteRequest,
)
from app.utils.translation_util import translate_text
from app.utils.formatter_util import format_form

router = APIRouter(tags=["forms"])

def ensure_digits(value: str, field_name: str) -> None:
    if not value.isdigit():
        error_message = translate_text(f"{field_name} must contain only digits")
        raise HTTPException(status_code=400, detail=error_message)


@router.post("/enquiry", response_model=ApiResponse)
async def submit_enquiry(payload: EnquiryRequest) -> ApiResponse:
    ensure_digits(payload.phone, "phone number")
    email_service.send(
        subject=f"Contact Us by {payload.name}",
        body="",
        html_body= format_form(payload),
        to_addrs=[settings.quote_and_enquiry_email],
    )
    return ApiResponse(message=translate_text("Your query has been submitted successfully."))


@router.post("/quote", response_model=ApiResponse)
async def submit_quote(payload: str = Form(...), attachment: UploadFile = File(None)) -> ApiResponse:
    try:
        parsed_payload = QuoteRequest.model_validate_json(payload)
    except ValidationError as exc:
        raise HTTPException(status_code=422, detail=json.loads(exc.json())) from exc

    ensure_digits(parsed_payload.phone, "phone number")

    email_service.send(
        subject=f"Enquiry by {parsed_payload.name}",
        body="",
        html_body=format_form(parsed_payload),
        to_addrs=[settings.quote_and_enquiry_email],
        attachments=[(attachment.filename, await attachment.read(), attachment.content_type or "application/octet-stream")] if attachment else None,
    )

    return ApiResponse(message=translate_text("Your enquiry has been submitted successfully."))


@router.post("/newsletter", response_model=ApiResponse)
async def subscribe_newsletter(payload: NewsletterRequest) -> ApiResponse:
    if newsletter_repo.is_subscribed(payload.email):
        raise HTTPException(status_code=409, detail=translate_text("You are already subscribed."))
    newsletter_repo.subscribe(payload.email)

    # Leave it simple for now, no need for templates
    admin_html = f"<p>New subscriber: {payload.email}</p>"
    user_html = (
        "<p>Thanks for subscribing to PLC Automation updates.</p>"
        "<p>We will share new blogs and videos with you soon.</p>"
    )

    # TODO: change email if needed
    email_service.send(
        subject=f"Subscribe by {payload.email}",
        html_body=admin_html,
        to_addrs=[settings.admin_email],
    )
    email_service.send(
        subject="Thanks for subscribing",
        html_body=user_html,
        to_addrs=[payload.email],
    )

    return ApiResponse(message=translate_text("Thank you for subscribing."))



