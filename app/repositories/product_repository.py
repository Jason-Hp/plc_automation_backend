from __future__ import annotations

from typing import Optional

from app.models.db.data_models import Manufacturer, Product
from app.utils.supabase_client_util import get_supabase_client



class ProductRepository:
    """
    Repository for products.
    """

    def __init__(self) -> None:
        self._client = get_supabase_client()
        if self._client is None:
            raise RuntimeError("Supabase client is not configured.")

    def get_product_by_id(self, product_id: int) -> Product | None:
        response = (
            self._client.table("products")
            .select("id,name,part_number,manufacturer_id,image_url,description")
            .eq("id", product_id)
            .limit(1)
            .execute()
        )
        rows = response.data or []
        if not rows:
            return None
        row = rows[0]

        manuf_id = row.get("manufacturer_id")
        manuf_resp = (
            self._client.table("manufacturers")
            .select("id,name")
            .eq("id", manuf_id)
            .limit(1)
            .execute()
        )
        manuf_rows = manuf_resp.data or []
        manufacturer = (
            Manufacturer.model_validate(manuf_rows[0])
            if manuf_rows
            else Manufacturer(id=manuf_id, name="Unknown")
        )

        return Product(
            id=row.get("id"),
            name=row.get("name"),
            part_number=row.get("part_number"),
            manufacturer=manufacturer,
            image_url=row.get("image_url"),
            description=row.get("description"),
        )
    
    def add_product(self, product: Product) -> None:
        row = product.model_dump(exclude={"id", "manufacturer"})
        row["manufacturer_id"] = product.manufacturer.id
        insert_resp = self._client.table("products").insert(row).execute()
        inserted = (insert_resp.data or [])[:1]
        if inserted and inserted[0].get("id") is not None:
            product.id = inserted[0]["id"]

    def update_product(self, product: Product) -> None:
        if product.id is None:
            return

        row = product.model_dump(exclude={"id", "manufacturer"})
        row["manufacturer_id"] = product.manufacturer.id
        self._client.table("products").update(row).eq("id", product.id).execute()
            
    def delete_product(self, product_id: int) -> None:
        self._client.table("products").delete().eq("id", product_id).execute()

    def list_products(
        self,
        page: int,
        per_page: int,
        search: Optional[str],
    ) -> tuple[list[Product], int]:
        query = (
            self._client.table("products")
            .select("id,name,part_number,manufacturer_id,image_url,description")
        )
        if search:
            query = query.ilike("part_number", f"%{search}%")

        total_resp = query.execute()
        total = len(total_resp.data or [])

        start = (page - 1) * per_page
        end = start + per_page - 1
        slice_resp = query.order("id", desc=False).range(start, end).execute()
        rows = slice_resp.data or []

        manufacturer_ids = list({r.get("manufacturer_id") for r in rows if r.get("manufacturer_id") is not None})
        manuf_map = {}
        if manufacturer_ids:
            m_resp = (
                self._client.table("manufacturers")
                .select("id,name")
                .in_("id", manufacturer_ids)
                .execute()
            )
            manuf_map = {r.get("id"): r.get("name") for r in (m_resp.data or []) if r.get("id") is not None}

        products: list[Product] = []
        for r in rows:
            mid = r.get("manufacturer_id")
            products.append(
                Product(
                    id=r.get("id"),
                    name=r.get("name"),
                    part_number=r.get("part_number"),
                    manufacturer=Manufacturer(id=mid, name=manuf_map.get(mid) or "Unknown"),
                    image_url=r.get("image_url"),
                    description=r.get("description"),
                )
            )
        return products, total
