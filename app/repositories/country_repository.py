from __future__ import annotations

from typing import Set, Tuple

from app.models.db.data_models import Country
from app.utils.supabase_client_util import get_supabase_client

class CountryRepository:

    def __init__(self):
        self._client = get_supabase_client()
        if self._client is None:
            raise RuntimeError("Supabase client is not configured.")

    def get_all_countries(self) -> list[Country]:
        response = (
            self._client.table("countries")
            .select("id,name,code")
            .order("id", desc=False)
            .execute()
        )
        return [Country.model_validate(r) for r in response.data or []]

    def get_country_by_id(self, country_id: int) -> Country | None:
        response = (
            self._client.table("countries")
            .select("id,name,code")
            .eq("id", country_id)
            .limit(1)
            .execute()
        )
        rows = response.data or []
        return Country.model_validate(rows[0]) if rows else None
            
    def get_country_by_code(self, code: str) -> Country | None:
        response = (
            self._client.table("countries")
            .select("id,name,code")
            .ilike("code", code)
            .limit(1)
            .execute()
        )
        rows = response.data or []
        return Country.model_validate(rows[0]) if rows else None
    
    def get_country_by_name(self, name: str) -> Country | None:
        response = (
            self._client.table("countries")
            .select("id,name,code")
            .ilike("name", name)
            .limit(1)
            .execute()
        )
        rows = response.data or []
        return Country.model_validate(rows[0]) if rows else None
    
    def add_country(self, country: Country) -> None:
        self._client.table("countries").insert(
            country.model_dump(exclude={"id"})
        ).execute()

    def update_country(self, country_id: int, country: Country) -> None:
        self._client.table("countries").update(
            country.model_dump(exclude={"id"})
        ).eq("id", country_id).execute()
            
    def delete_country(self, country_id: int) -> None:
        self._client.table("countries").delete().eq("id", country_id).execute()
        self._client.table("product_countries").delete().eq("country_id", country_id).execute()
