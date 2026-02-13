from __future__ import annotations

from fastapi import APIRouter, HTTPException

from app.schemas import FAQ, ContactInfo, Category, Manufacturer, Country
from app.utils.translation_util import translate_text
from app.repositories.faq_repository import FaqRepository
from app.repositories.contact_info_repository import ContactInfoRepository
from app.repositories.category_repository import CategoryRepository
from app.repositories.maufacturer_repository import ManufacturerRepository
from app.repositories.country_repository import CountryRepository

router = APIRouter(tags=["info"])
faq_repo = FaqRepository()
contact_info_repo = ContactInfoRepository()
category_repo = CategoryRepository()
manufacturer_repo = ManufacturerRepository()
country_repo = CountryRepository()

@router.get("/faqs")
async def get_faqs() -> list[FAQ]:
    faqs = faq_repo.get_all_faqs()
    for faq in faqs:
        faq.question = translate_text(faq.question)
        faq.answer = translate_text(faq.answer)
    return faqs

@router.get("/contact-info")
async def get_contact_info() -> list[ContactInfo]:
    return contact_info_repo.get_all_contact_info()

@router.get("/contact-info/{country}")
async def get_contact_info_by_country(country: str) -> ContactInfo:
    contact_info = contact_info_repo.get_contact_info_by_country(country)
    if not contact_info:
        raise HTTPException(status_code=404, detail="Contact info not found")

    return contact_info

@router.get("/categories")
async def get_categories() -> list[Category]:
    return category_repo.get_all_categories()

@router.get("/manufacturers")
async def get_manufacturers() -> list[Manufacturer]:
    return manufacturer_repo.get_all_manufacturers()

@router.get("/countries")
async def get_countries() -> list[Country]:
    return country_repo.get_all_countries()