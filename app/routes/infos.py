from __future__ import annotations

from fastapi import APIRouter, HTTPException

from app.models.api.response_models import (
    CategoryResponse,
    ContactInfoResponse,
    CountryResponse,
    FAQResponse,
    ManufacturerResponse,
)
from app.dependencies import public_infos_service

router = APIRouter(tags=["info"])
@router.get("/faqs")
async def get_faqs() -> list[FAQResponse]:
    return public_infos_service.get_faqs()

@router.get("/contact-info")
async def get_contact_info() -> list[ContactInfoResponse]:
    return public_infos_service.get_contact_infos()

@router.get("/contact-info/{country}")
async def get_contact_info_by_country(country: str) -> ContactInfoResponse:
    return public_infos_service.get_contact_info_by_country(country)

@router.get("/categories")
async def get_categories() -> list[CategoryResponse]:
    return public_infos_service.get_categories()

@router.get("/manufacturers")
async def get_manufacturers() -> list[ManufacturerResponse]:
    return public_infos_service.get_manufacturers()

@router.get("/countries")
async def get_countries() -> list[CountryResponse]:
    return public_infos_service.get_countries()