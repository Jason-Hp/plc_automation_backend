from __future__ import annotations

from typing import List

from app.utils.supabase_client_util import get_supabase_client


class ProductCountryRepository:
    """
    Repository for the `product_countries` JOIN TABLE.
    """

    def __init__(self) -> None:
        self._client = get_supabase_client()
        if self._client is None:
            raise RuntimeError("Supabase client is not configured.")

    def get_product_availability_by_country(self, country_id: int, product_id: int) -> bool:
        """
        Check if a product is available in a given country.
        """
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
        """
        Add availability rows for a product across multiple countries by country names.
        """
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
        """
        Remove all availability rows for a given product.
        """
        self._client.table("product_countries").delete().eq("product_id", product_id).execute()

    def update_product_availability_for_countries(self, countries: list[str], product_id: int) -> None:
        """
        Replace availability rows for a product with a new set of country names.
        """
        self.delete_all_product_availability_for_countries(product_id)
        self.add_product_availability_for_countries(countries, product_id)
