from __future__ import annotations

from typing import Optional

from app.models.db.data_models import Manufacturer
from app.utils.supabase_client_util import get_supabase_client

class ManufacturerRepository:
    """
    Repository for manufacturers.
    """

    def __init__(self) -> None:
        self._client = get_supabase_client()
        if self._client is None:
            raise RuntimeError("Supabase client is not configured.")

    def get_all_manufacturers(self) -> list[Manufacturer]:
        response = (
            self._client.table("manufacturers")
            .select("id,name")
            .order("id", desc=False)
            .execute()
        )
        return [Manufacturer.model_validate(r) for r in response.data or []]

    def get_manufacturer_by_id(self, manufacturer_id: int) -> Optional[Manufacturer]:
        response = (
            self._client.table("manufacturers")
            .select("id,name")
            .eq("id", manufacturer_id)
            .limit(1)
            .execute()
        )
        rows = response.data or []
        return Manufacturer.model_validate(rows[0]) if rows else None
    
    def get_manufacturer_by_name(self, name: str) -> Optional[Manufacturer]:
        response = (
            self._client.table("manufacturers")
            .select("id,name")
            .ilike("name", name)
            .limit(1)
            .execute()
        )
        rows = response.data or []
        return Manufacturer.model_validate(rows[0]) if rows else None
    
    def add_manufacturer(self, manufacturer: Manufacturer) -> None:
        self._client.table("manufacturers").insert(
            manufacturer.model_dump(exclude={"id"})
        ).execute()

    def update_manufacturer(self, manufacturer_id: int, manufacturer: Manufacturer) -> None:
        self._client.table("manufacturers").update(
            manufacturer.model_dump(exclude={"id"})
        ).eq("id", manufacturer_id).execute()
            
    def delete_manufacturer(self, manufacturer_id: int) -> None:
        self._client.table("manufacturers").delete().eq("id", manufacturer_id).execute()
    