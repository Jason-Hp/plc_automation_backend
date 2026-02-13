from __future__ import annotations

from typing import Set, Tuple

from app.schemas import Country

class CountryRepository:

    def __init__(self):
        self._countries: list[Country] = []
        # In-memory join table: (product_id, country_id)
        self._product_country_map: Set[Tuple[int, int]] = set()

    def get_all_countries(self) -> list[Country]:
        return self._countries

    def get_country_by_id(self, country_id: int) -> Country | None:
        for country in self._countries:
            if country.id == country_id:
                return country
            
    def get_country_by_code(self, code: str) -> Country | None:
        for country in self._countries:
            if country.code.lower() == code.lower():
                return country
        return None
    
    def get_country_by_name(self, name: str) -> Country | None:
        for country in self._countries:
            if country.name.lower() == name.lower():
                return country
        return None
    
    def add_country(self, country: Country) -> None:
        self._countries.append(country)

    def update_country(self, country_id: int, country: Country) -> None:
        for index, current in enumerate(self._countries):
            if current.id == country_id:
                self._countries[index] = country
                return
            
    def delete_country(self, country_id: int) -> None:
        self._countries = [country for country in self._countries if country.id != country_id]
        # Also remove any availability rows for this country
        self._product_country_map = {
            (p_id, c_id) for (p_id, c_id) in self._product_country_map if c_id != country_id
        }

    def get_product_availability_by_country(self, country_id: int, product_id: int) -> bool:
        """
        Check if a product is available in a given country, using a join table like:
        tbl_product_country_availability (product_id, country_id).
        """
        return (product_id, country_id) in self._product_country_map

    def add_product_availability_for_country(self, country_ids: list[int], product_id: int) -> None:
        """
        Add availability rows for a product across multiple countries.
        """
        for cid in country_ids:
            self._product_country_map.add((product_id, cid))

    def delete_all_product_availability_for_country(self, product_id: int) -> None:
        """
        Remove all availability rows for a given product.
        """
        self._product_country_map = {
            (p_id, c_id) for (p_id, c_id) in self._product_country_map if p_id != product_id
        }

    def update_product_availability_for_country(self, country_ids: list[int], product_id: int) -> None:
        """
        Replace availability rows for a product with a new set of country IDs.
        """
        self.delete_all_product_availability_for_country(product_id)
        self.add_product_availability_for_country(country_ids, product_id)
