from __future__ import annotations

from typing import List, Optional

from app.schemas import Manufacturer, Product, ProductPreviewListResponse


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

    def get_product_by_id(self, product_id: int) -> Optional[Product]:
        for item in self._products:
            if item.id == product_id:
                return item
        return None
    
    def add_product(self, product: Product) -> None:
        self._products.append(product)

    def update_product(self, product_id: int, product: Product) -> None:
        for idx, item in enumerate(self._products):
            if item.id == product_id:
                self._products[idx] = product
                return
            
    def delete_product(self, product_id: int) -> None:
        self._products = [item for item in self._products if item.id != product_id]

    def list_products(
        self,
        page: int,
        per_page: int,
        category: Optional[str],
        search: Optional[str],
    ) -> ProductPreviewListResponse:
        # TODO: Replace with SQL filtering for category + keyword search.
        filtered: List[Product] = self._products
        if search:
            filtered = [item for item in filtered if search.lower() in item.part_number.lower()]
        total = len(filtered)
        start = (page - 1) * per_page
        end = start + per_page
        return ProductPreviewListResponse(
            product_previews=filtered[start:end],
            page=page,
            per_page=per_page,
            total=total,
        )
