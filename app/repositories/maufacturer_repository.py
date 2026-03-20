from __future__ import annotations

from typing import Optional

from app.models.db.data_models import Manufacturer
from app.utils.supabase_client_util import get_supabase_client

class ManufacturerRepository:
    """
    Placeholder repository. Replace with SQL queries against manufacturers.
    """

    def __init__(self) -> None:
        self._manufacturers = [
            Manufacturer(
                id=1,
                name="Siemens",
            ),
            Manufacturer(
                id=2,
                name="Allen-Bradley",
            ),
        ]
        self._client = get_supabase_client()

    def get_all_manufacturers(self) -> list[Manufacturer]:
        # {RULE} Get all manufacturers {RULE}
        if self._client is None:
            return self._manufacturers

        response = (
            self._client.table("manufacturers")
            .select("id,name")
            .order("id", desc=False)
            .execute()
        )
        return [Manufacturer.model_validate(r) for r in response.data or []]

    def get_manufacturer_by_id(self, manufacturer_id: int) -> Optional[Manufacturer]:
        if self._client is None:
            for item in self._manufacturers:
                if item.id == manufacturer_id:
                    return item
            return None

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
        if self._client is None:
            for item in self._manufacturers:
                if item.name.lower() == name.lower():
                    return item
            return None

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
        if self._client is None:
            self._manufacturers.append(manufacturer)
            return

        self._client.table("manufacturers").insert(
            manufacturer.model_dump(exclude={"id"})
        ).execute()

    def update_manufacturer(self, manufacturer_id: int, manufacturer: Manufacturer) -> None:
        if self._client is None:
            for idx, item in enumerate(self._manufacturers):
                if item.id == manufacturer_id:
                    self._manufacturers[idx] = manufacturer
                    return
            return

        self._client.table("manufacturers").update(
            manufacturer.model_dump(exclude={"id"})
        ).eq("id", manufacturer_id).execute()
            
    def delete_manufacturer(self, manufacturer_id: int) -> None:
        if self._client is None:
            self._manufacturers = [
                item for item in self._manufacturers if item.id != manufacturer_id
            ]
            return

        self._client.table("manufacturers").delete().eq("id", manufacturer_id).execute()
    