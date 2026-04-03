from __future__ import annotations

from typing import Optional
from fastapi import HTTPException

from app.models.api.request_models import ProductWithCountriesRequest
from app.models.api.response_models import (
    ApiResponse,
    ManufacturerResponse,
    ProductPreviewListResponse,
    ProductPreviewResponse,
    ProductResponse,
    ProductWithStockDataResponse,
    ProductWithStockResponse,
)
from app.models.db.data_models import Product as ProductDb
from app.repositories.country_repository import CountryRepository
from app.repositories.maufacturer_repository import ManufacturerRepository
from app.repositories.product_country_repository import ProductCountryRepository
from app.repositories.product_repository import ProductRepository
from app.utils.translation_util import translate_text


class ProductService:
    def __init__(
        self,
        *,
        product_repo: ProductRepository,
        manufacturer_repo: ManufacturerRepository,
        country_repo: CountryRepository,
        product_country_repo: ProductCountryRepository,
    ) -> None:
        self._product_repo = product_repo
        self._manufacturer_repo = manufacturer_repo
        self._country_repo = country_repo
        self._product_country_repo = product_country_repo

    # --- Public Methods ---

    def list_product_previews(
        self, *, page: int, per_page: int, search: Optional[str]
    ) -> ProductPreviewListResponse:
        products, total = self._product_repo.list_products(
            page=page, per_page=per_page, search=search
        )
        return ProductPreviewListResponse(
            product_previews=[
                ProductPreviewResponse(
                    id=p.id,
                    name=p.name,
                    part_number=p.part_number,
                    manufacturer=ManufacturerResponse(
                        id=p.manufacturer.id, name=p.manufacturer.name
                    ),
                    image_url=p.image_url,
                )
                for p in products
            ],
            page=page,
            per_page=per_page,
            total=total,
        )

    def get_product_with_stock(
        self, *, product_id: int, country_name: str
    ) -> ProductWithStockResponse:
        product = self._product_repo.get_product_by_id(product_id)
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")

        country = self._country_repo.get_country_by_name(country_name)
        stock = False
        if country and country.id is not None and product.id is not None:
            stock = self._product_country_repo.get_product_availability_by_country(
                country.id, product.id
            )

        description = product.description
        if description:
            description = translate_text(description)

        product_dto = ProductResponse(
            id=product.id,
            name=product.name,
            part_number=product.part_number,
            manufacturer=ManufacturerResponse(
                id=product.manufacturer.id, name=product.manufacturer.name
            ),
            image_url=product.image_url,
            description=description,
        )
        data = ProductWithStockDataResponse(product=product_dto, stock=stock)
        return ProductWithStockResponse(product_with_stock=data)

    # --- Admin Methods ---

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
        if product.id:
            self._product_country_repo.add_product_availability_for_countries(
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
        if product.id:
            self._product_country_repo.update_product_availability_for_countries(
                request.countries, product.id
            )
        return ApiResponse(message="Product updated successfully.")

    def delete_product(self, *, product_id: int) -> ApiResponse:
        self._product_repo.delete_product(product_id)
        self._product_country_repo.delete_all_product_availability_for_countries(product_id)
        return ApiResponse(message="Product deleted successfully.")
