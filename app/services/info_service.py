from __future__ import annotations

from typing import List
from fastapi import HTTPException

from app.models.db.data_models import FAQ, Category, ContactInfo, Country, Manufacturer
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


class InfoService:
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

    # --- Public Methods ---

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

    # --- Admin Methods (FAQ) ---

    def upload_faqs(self, faqs: List[FAQ]) -> None:
        for faq in faqs:
            self._faq_repo.add_faq(faq.question, faq.answer)

    def update_faq(self, faq_id: int, *, question: str, answer: str) -> None:
        self._faq_repo.update_faq(faq_id, question, answer)

    def delete_faq(self, faq_id: int) -> None:
        self._faq_repo.delete_faq(faq_id)

    # --- Admin Methods (Catalog: Categories, Manufacturers, Countries, Contact Info) ---

    def add_category(self, category: Category) -> None:
        self._category_repo.add_category(category)

    def update_category(self, category_id: int, category: Category) -> None:
        category.id = category_id
        self._category_repo.update_category(category_id, category)

    def delete_category(self, category_id: int) -> None:
        self._category_repo.delete_category(category_id)

    def add_manufacturer(self, manufacturer: Manufacturer) -> None:
        self._manufacturer_repo.add_manufacturer(manufacturer)

    def update_manufacturer(self, manufacturer_id: int, manufacturer: Manufacturer) -> None:
        manufacturer.id = manufacturer_id
        self._manufacturer_repo.update_manufacturer(manufacturer_id, manufacturer)

    def delete_manufacturer(self, manufacturer_id: int) -> None:
        self._manufacturer_repo.delete_manufacturer(manufacturer_id)

    def add_country(self, country: Country) -> None:
        self._country_repo.add_country(country)

    def update_country(self, country_id: int, country: Country) -> None:
        country.id = country_id
        self._country_repo.update_country(country_id, country)

    def delete_country(self, country_id: int) -> None:
        self._country_repo.delete_country(country_id)

    def add_contact_info(self, contact_info: ContactInfo) -> None:
        self._contact_info_repo.add_contact_info(contact_info)

    def update_contact_info(self, contact_id: int, contact_info: ContactInfo) -> None:
        contact_info.id = contact_id
        self._contact_info_repo.update_contact_info(contact_id, contact_info)

    def delete_contact_info(self, contact_id: int) -> None:
        self._contact_info_repo.delete_contact_info(contact_id)
