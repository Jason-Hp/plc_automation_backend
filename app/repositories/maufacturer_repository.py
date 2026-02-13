from __future__ import annotations

from typing import Optional

from app.schemas import Manufacturer

class ManufacturerRepository:
    """
    Placeholder repository. Replace with SQL queries against tbl_manufacturer.
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

    def get_all_manufacturers(self) -> list[Manufacturer]:
        return self._manufacturers

    def get_manufacturer_by_id(self, manufacturer_id: int) -> Optional[Manufacturer]:
        for item in self._manufacturers:
            if item.id == manufacturer_id:
                return item
        return None
    
    def get_manufacturer_by_name(self, name: str) -> Optional[Manufacturer]:
        for item in self._manufacturers:
            if item.name.lower() == name.lower():
                return item
        return None
    
    def add_manufacturer(self, manufacturer: Manufacturer) -> None:
        self._manufacturers.append(manufacturer)

    def update_manufacturer(self, manufacturer_id: int, manufacturer: Manufacturer) -> None:
        for idx, item in enumerate(self._manufacturers):
            if item.id == manufacturer_id:
                self._manufacturers[idx] = manufacturer
                return
            
    def delete_manufacturer(self, manufacturer_id: int) -> None:
        self._manufacturers = [item for item in self._manufacturers if item.id != manufacturer_id]
    