from __future__ import annotations

from typing import Optional

from app.models.db.data_models import Category, ContactInfo, Country, Manufacturer
from app.repositories.category_repository import CategoryRepository
from app.repositories.contact_info_repository import ContactInfoRepository
from app.repositories.country_repository import CountryRepository
from app.repositories.maufacturer_repository import ManufacturerRepository


class AdminCatalogService:
    def __init__(
        self,
        *,
        category_repo: CategoryRepository,
        manufacturer_repo: ManufacturerRepository,
        country_repo: CountryRepository,
        contact_info_repo: ContactInfoRepository,
    ) -> None:
        self._category_repo = category_repo
        self._manufacturer_repo = manufacturer_repo
        self._country_repo = country_repo
        self._contact_info_repo = contact_info_repo

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

