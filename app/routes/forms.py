from __future__ import annotations

from fastapi import APIRouter, File, Form, HTTPException, UploadFile

from app.config import settings
from app.repositories.newsletter_repository import NewsletterRepository
from app.schemas import (
    ApiResponse,
    EnquiryRequest,
    JobApplicationRequest,
    NewsletterRequest,
    QuoteRequest,
    JobApplicationRequest
)
from app.services.email_service import EmailService
from app.services.storage_service import StorageService
from app.utils.translation_util import translate_text
from app.utils.formatter_util import format_form

router = APIRouter(tags=["forms"])
newsletter_repo = NewsletterRepository()
email_service = EmailService()
storage_service = StorageService()


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
async def submit_quote(payload: QuoteRequest, attachment: UploadFile = File(None)) -> ApiResponse:
    ensure_digits(payload.phone, "phone number")
    
    email_service.send(
        subject=f"Enquiry by {payload.name}",
        body="",
        html_body= format_form(payload),
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


@router.post("/job-application", response_model=ApiResponse)
async def submit_job_application(
    payload: JobApplicationRequest,
    resume: UploadFile = File(...),
) -> ApiResponse:
    ensure_digits(payload.phone, "phone number")
    resume_bytes = await resume.read()
    storage_service.save_upload(resume.filename, resume_bytes)

    email_service.send(
        subject=f"Apply Job {payload.first_name} {payload.last_name}",
        body="",
        html_body=format_form(payload),
        to_addrs=[settings.hr_email],
        attachments=[(resume.filename, resume_bytes, resume.content_type or "application/octet-stream")],
    )

    return ApiResponse(message=translate_text("Application submitted successfully."))



