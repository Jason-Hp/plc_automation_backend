from __future__ import annotations

from fastapi import APIRouter, File, Form, UploadFile
import json
from app.dependencies import forms_service
from app.models.api.request_models import (
    EnquiryRequest,
    NewsletterRequest,
    QuoteWithProductPreviewsWithQuantityRequest,
)
from app.models.api.response_models import ApiResponse

router = APIRouter(tags=["forms"])


@router.post("/enquiry", response_model=ApiResponse)
async def submit_enquiry(payload: EnquiryRequest) -> ApiResponse:
    return await forms_service.submit_enquiry(payload=payload)


@router.post("/quote", response_model=ApiResponse)
async def submit_quote(
    payload: str = Form(...),
    attachment: UploadFile = File(None),
) -> ApiResponse:

    parsed_payload = QuoteWithProductPreviewsWithQuantityRequest.model_validate(json.loads(payload))
    
    # Force set to false to prevent users from trying to set it to true and total amount to 0 to prevent users from trying to set it to a custom value. The actual values will be calculated in the service layer based on the products and their quantities.
    parsed_payload.is_paid = False
    parsed_payload.total_amount = 0

    return await forms_service.submit_quote(payload=parsed_payload, attachment=attachment)


@router.post("/newsletter", response_model=ApiResponse)
async def subscribe_newsletter(payload: NewsletterRequest) -> ApiResponse:
    return await forms_service.subscribe_newsletter(payload=payload)

