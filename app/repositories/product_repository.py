from __future__ import annotations

from typing import List, Optional

from app.models.api.response_models import ProductPreviewListResponse
from app.models.db.data_models import Product
from app.models.domain.domain_models import ProductPreview, ProductWithStock



class ProductRepository:
    """
    Placeholder repository. Replace with SQL queries against tbl_product/tbl_offer_product.
    """

    def __init__(self) -> None:
        self._products = [
            Product(
                id=1,
                name="SIMATIC S7-1500 CPU",
                part_number="CPU-1510",
                manufacturer=Manufacturer(id=1, name="Siemens"),
                stock=True,
                description="Sample PLC CPU for wiring cabinets.",
            )
        ]

    def get_product_by_id(self, product_id: int) -> Product:
        # {RULE} Get current product with id {RULE}
        for item in self._products:
            if item.id == product_id:
                return item
        return None
    
    def add_product(self, product: Product) -> None:
        self._products.append(product)

    def update_product(self, product: Product) -> None:
        # {RULE} update based on product id with product {RULE}
        for idx, item in enumerate(self._products):
            if item.id == product_id:
                self._products[idx] = product
                return
            
    def delete_product(self, product_id: int) -> None:
        # {RULE} delete based on product id {RULE}
        self._products = [item for item in self._products if item.id != product_id]

    def list_products(
        self,
        page: int,
        per_page: int,
        search: Optional[str],
    ) -> ProductPreviewListResponse:
        # {RULE} Get products filtered by search with pagination, basically wildcard search on description, name, etc and then convert it to ProductPreview {RULE}

        # TODO: Replace with SQL filtering for category + keyword search.
        filtered: List[Product] = self._products
        if search:
            filtered = [item for item in filtered if search.lower() in item.part_number.lower()]
        total = len(filtered)
        start = (page - 1) * per_page
        end = start + per_page
        filtered = filtered[start:end]

        return filtered, total

