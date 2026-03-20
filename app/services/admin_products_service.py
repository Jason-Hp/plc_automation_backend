from __future__ import annotations

from fastapi import HTTPException

from app.models.api.request_models import ProductWithCountriesRequest
from app.models.api.response_models import ApiResponse
from app.models.db.data_models import Product as ProductDb
from app.repositories.country_repository import CountryRepository
from app.repositories.maufacturer_repository import ManufacturerRepository
from app.repositories.product_repository import ProductRepository


class AdminProductsService:
    def __init__(
        self,
        *,
        manufacturer_repo: ManufacturerRepository,
        product_repo: ProductRepository,
        country_repo: CountryRepository,
    ) -> None:
        self._manufacturer_repo = manufacturer_repo
        self._product_repo = product_repo
        self._country_repo = country_repo

    def add_product(self, *, request: ProductWithCountriesRequest) -> ApiResponse:
        manufacturer = self._manufacturer_repo.get_manufacturer_by_name(
            request.manufacturer
        )
        if manufacturer is None:
            raise HTTPException(status_code=400, detail="Manufacturer not found.")

        product = ProductDb(
            id=request.id,
            name=request.name,
            part_number=request.part_number,
            manufacturer=manufacturer,
            image_url=request.image_url,
            description=request.description,
        )
        self._product_repo.add_product(product)
        self._country_repo.add_product_availability_for_countries(
            request.countries, product.id
        )
        return ApiResponse(message="Product uploaded successfully.")

    def update_product(
        self,
        *,
        product_id: int,
        request: ProductWithCountriesRequest,
    ) -> ApiResponse:
        manufacturer = self._manufacturer_repo.get_manufacturer_by_name(
            request.manufacturer
        )
        if manufacturer is None:
            raise HTTPException(status_code=400, detail="Manufacturer not found.")

        product = ProductDb(
            id=product_id,
            name=request.name,
            part_number=request.part_number,
            manufacturer=manufacturer,
            image_url=request.image_url,
            description=request.description,
        )
        self._product_repo.update_product(product)
        self._country_repo.update_product_availability_for_countries(
            request.countries, product.id
        )
        return ApiResponse(message="Product updated successfully.")

    def delete_product(self, *, product_id: int) -> ApiResponse:
        self._product_repo.delete_product(product_id)
        self._country_repo.delete_all_product_availability_for_countries(product_id)
        return ApiResponse(message="Product deleted successfully.")

