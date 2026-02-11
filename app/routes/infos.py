from __future__ import annotations

from fastapi import APIRouter

from app.schemas import FAQResponse, ContactInfoResponse
from app.utils.translation_util import translate_text
from app.repositories.faq_repository import FaqRepository
from app.repositories.contact_info_repository import ContactInfoRepository

router = APIRouter(tags=["info"])
faq_repo = FaqRepository()
contact_info_repo = ContactInfoRepository()

@router.get("/faqs")
async def get_faqs() -> list[FAQResponse]:
    faqs = faq_repo.get_all_faqs()
    for faq in faqs:
        faq.question = translate_text(faq.question)
        faq.answer = translate_text(faq.answer)
    return faqs

@router.get("/contact-info")
async def get_contact_info() -> list[ContactInfoResponse]:
    return contact_info_repo.get_all_contact_info()

@router.get("/contact-info/{country}")
async def get_contact_info_by_country(country: str) -> ContactInfoResponse:
    contact_info = contact_info_repo.get_contact_info_by_country(country)
    return contact_info