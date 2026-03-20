from __future__ import annotations

from typing import Dict, List, Optional

from app.models.domain.domain_models import Manufacturer as DomainManufacturer
from app.models.domain.domain_models import ProductPreviewWithQuantity
from app.utils.supabase_client_util import get_supabase_client


class QuoteProductRepository:
    """
    Repository for the `quotes_products` JOIN TABLE.

    In this backend version we keep it in-memory as:
      quote_id -> list[ProductPreviewWithQuantity]
    """

    def __init__(self) -> None:
        self._quote_products: Dict[int, List[ProductPreviewWithQuantity]] = {}
        self._client = get_supabase_client()

    def get_product_previews_with_quantity_by_quote_id(
        self, quote_id: int
    ) -> List[ProductPreviewWithQuantity]:
        if self._client is None:
            # Return a copy to avoid accidental mutation from callers.
            return list(self._quote_products.get(quote_id, []))

        join_resp = (
            self._client.table("quotes_products")
            .select("product_id,quantity")
            .eq("quote_id", quote_id)
            .execute()
        )
        join_rows = join_resp.data or []
        product_ids = [r.get("product_id") for r in join_rows if r.get("product_id") is not None]
        if not product_ids:
            return []

        products_resp = (
            self._client.table("tbl_product")
            .select("id,name,part_number,manufacturer_id,image_url")
            .in_("id", product_ids)
            .execute()
        )
        product_rows = products_resp.data or []
        products_map = {r.get("id"): r for r in product_rows if r.get("id") is not None}

        manufacturer_ids = list({r.get("manufacturer_id") for r in product_rows if r.get("manufacturer_id") is not None})
        manufacturers_map = {}
        if manufacturer_ids:
            manuf_resp = (
                self._client.table("tbl_manufacturer")
                .select("id,name")
                .in_("id", manufacturer_ids)
                .execute()
            )
            manufacturers_map = {r.get("id"): r for r in manuf_resp.data or [] if r.get("id") is not None}

        previews: List[ProductPreviewWithQuantity] = []
        for jr in join_rows:
            pid = jr.get("product_id")
            qty = jr.get("quantity")
            if pid is None or qty is None:
                continue

            prod = products_map.get(pid)
            if not prod:
                continue

            mid = prod.get("manufacturer_id")
            manuf = manufacturers_map.get(mid)
            domain_manufacturer = DomainManufacturer(
                id=mid, name=(manuf or {}).get("name") or "Unknown"
            )
            previews.append(
                ProductPreviewWithQuantity(
                    id=pid,
                    name=prod.get("name") or "",
                    part_number=prod.get("part_number") or "",
                    manufacturer=domain_manufacturer,
                    image_url=prod.get("image_url"),
                    quantity=int(qty),
                )
            )

        return previews

    def add_products_to_quote_with_quantity(
        self, quote_id: int, product_previews_with_quantity: List[ProductPreviewWithQuantity]
    ) -> None:
        if self._client is None:
            self._quote_products[quote_id] = list(product_previews_with_quantity)
            return

        insert_rows = []
        for p in product_previews_with_quantity:
            if p.id is None:
                continue
            insert_rows.append(
                {"quote_id": quote_id, "product_id": p.id, "quantity": p.quantity}
            )

        if insert_rows:
            self._client.table("quotes_products").insert(insert_rows).execute()

    def update_products_to_quote_with_quantity(
        self, quote_id: int, product_previews_with_quantity: List[ProductPreviewWithQuantity]
    ) -> None:
        if self._client is None:
            self._quote_products[quote_id] = list(product_previews_with_quantity)
            return

        self._client.table("quotes_products").delete().eq("quote_id", quote_id).execute()
        self.add_products_to_quote_with_quantity(quote_id, product_previews_with_quantity)

    def delete_products_to_quote_with_quantity(self, quote_id: int) -> None:
        if self._client is None:
            self._quote_products.pop(quote_id, None)
            return

        self._client.table("quotes_products").delete().eq("quote_id", quote_id).execute()

