from __future__ import annotations

from typing import List

from fastapi import HTTPException

from app.models.api.response_models import (
    CategoryResponse,
    ContactInfoResponse,
    CountryResponse,
    FAQResponse,
    ManufacturerResponse,
)
from app.repositories.category_repository import CategoryRepository
from app.repositories.contact_info_repository import ContactInfoRepository
from app.repositories.country_repository import CountryRepository
from app.repositories.faq_repository import FaqRepository
from app.repositories.maufacturer_repository import ManufacturerRepository
from app.utils.translation_util import translate_text


class PublicInfosService:
    def __init__(
        self,
        *,
        faq_repo: FaqRepository,
        contact_info_repo: ContactInfoRepository,
        category_repo: CategoryRepository,
        manufacturer_repo: ManufacturerRepository,
        country_repo: CountryRepository,
    ) -> None:
        self._faq_repo = faq_repo
        self._contact_info_repo = contact_info_repo
        self._category_repo = category_repo
        self._manufacturer_repo = manufacturer_repo
        self._country_repo = country_repo

    def get_faqs(self) -> List[FAQResponse]:
        faqs = self._faq_repo.get_all_faqs()
        return [
            FAQResponse.model_validate(
                {
                    "id": faq.id,
                    "question": translate_text(faq.question),
                    "answer": translate_text(faq.answer),
                }
            )
            for faq in faqs
        ]

    def get_contact_infos(self) -> List[ContactInfoResponse]:
        return [
            ContactInfoResponse.model_validate(info.model_dump())
            for info in self._contact_info_repo.get_all_contact_info()
        ]

    def get_contact_info_by_country(self, country: str) -> ContactInfoResponse:
        contact_info = self._contact_info_repo.get_contact_info_by_country(country)
        if not contact_info:
            raise HTTPException(status_code=404, detail="Contact info not found")
        return ContactInfoResponse.model_validate(contact_info.model_dump())

    def get_categories(self) -> List[CategoryResponse]:
        return [
            CategoryResponse.model_validate(c.model_dump())
            for c in self._category_repo.get_all_categories()
        ]

    def get_manufacturers(self) -> List[ManufacturerResponse]:
        return [
            ManufacturerResponse.model_validate(m.model_dump())
            for m in self._manufacturer_repo.get_all_manufacturers()
        ]

    def get_countries(self) -> List[CountryResponse]:
        return [
            CountryResponse.model_validate(c.model_dump())
            for c in self._country_repo.get_all_countries()
        ]

