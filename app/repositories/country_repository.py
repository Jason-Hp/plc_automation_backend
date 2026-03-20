from __future__ import annotations

from typing import Set, Tuple

from app.models.db.data_models import Country
from app.utils.supabase_client_util import get_supabase_client

class CountryRepository:

    def __init__(self):
        self._countries: list[Country] = []
        # In-memory join table: (product_id, country_id)
        self._product_country_map: Set[Tuple[int, int]] = set()
        self._client = get_supabase_client()

    def get_all_countries(self) -> list[Country]:
        if self._client is None:
            return self._countries

        response = (
            self._client.table("countries")
            .select("id,name,code")
            .order("id", desc=False)
            .execute()
        )
        return [Country.model_validate(r) for r in response.data or []]

    def get_country_by_id(self, country_id: int) -> Country | None:
        if self._client is None:
            for country in self._countries:
                if country.id == country_id:
                    return country
            return None

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
        if self._client is None:
            for country in self._countries:
                if country.code.lower() == code.lower():
                    return country
            return None

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
        if self._client is None:
            for country in self._countries:
                if country.name.lower() == name.lower():
                    return country
            return None

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
        if self._client is None:
            self._countries.append(country)
            return

        self._client.table("countries").insert(
            country.model_dump(exclude={"id"})
        ).execute()

    def update_country(self, country_id: int, country: Country) -> None:
        if self._client is None:
            for index, current in enumerate(self._countries):
                if current.id == country_id:
                    self._countries[index] = country
                    return
            return

        self._client.table("countries").update(
            country.model_dump(exclude={"id"})
        ).eq("id", country_id).execute()
            
    def delete_country(self, country_id: int) -> None:
        if self._client is None:
            self._countries = [country for country in self._countries if country.id != country_id]
            # Also remove any availability rows for this country
            self._product_country_map = {
                (p_id, c_id) for (p_id, c_id) in self._product_country_map if c_id != country_id
            }
            return

        self._client.table("countries").delete().eq("id", country_id).execute()
        self._client.table("product_countries").delete().eq("country_id", country_id).execute()

    def get_product_availability_by_country(self, country_id: int, product_id: int) -> bool:
        """
        Check if a product is available in a given country, using a join table like:
        product_countries (product_id, country_id).
        """
        if self._client is None:
            return (product_id, country_id) in self._product_country_map

        response = (
            self._client.table("product_countries")
            .select("product_id,country_id")
            .eq("product_id", product_id)
            .eq("country_id", country_id)
            .limit(1)
            .execute()
        )
        return bool(response.data)

    def add_product_availability_for_countries(self, countries: list[str], product_id: int) -> None:
        # {RULE} Add in JOIN TABLE using countries to get corresponding country ids map to product id {RULE}
        """
        Add availability rows for a product across multiple countries.
        """
        if self._client is None:
            # `countries` are country names (not ids). Map them to known country ids.
            for country_name in countries:
                country = self.get_country_by_name(country_name)
                if country is None or country.id is None:
                    continue
                self._product_country_map.add((product_id, country.id))
            return

        # Map country names to ids (case-insensitive).
        response = self._client.table("countries").select("id,name").execute()
        rows = response.data or []
        name_to_id = {
            (r.get("name") or "").lower(): r.get("id")
            for r in rows
            if r.get("id") is not None and r.get("name") is not None
        }

        insert_rows = []
        for country_name in countries:
            cid = name_to_id.get((country_name or "").lower())
            if cid is None:
                continue
            insert_rows.append({"product_id": product_id, "country_id": cid})

        if insert_rows:
            self._client.table("product_countries").insert(insert_rows).execute()

    def delete_all_product_availability_for_countries(self, product_id: int) -> None:
        # {RULE} Delete all entries in JOIN TABLE with product id {RULE}
        """
        Remove all availability rows for a given product.
        """
        if self._client is None:
            self._product_country_map = {
                (p_id, c_id) for (p_id, c_id) in self._product_country_map if p_id != product_id
            }
            return

        self._client.table("product_countries").delete().eq("product_id", product_id).execute()

    def update_product_availability_for_countries(self, countries: list[str], product_id: int) -> None:
        # {RULE} Call delete_all_product_availability_for_countries, then call add_product_availability_for_countries {RULE}
        """
        Replace availability rows for a product with a new set of country IDs.
        """
        self.delete_all_product_availability_for_countries(product_id)
        self.add_product_availability_for_countries(countries, product_id)
