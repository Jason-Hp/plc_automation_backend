from app.schemas import ContactInfo


class ContactInfoRepository:
    def __init__(self):
        self._contact_infos: list[ContactInfo] = []
        self._next_id = 1

    def get_all_contact_info(self) -> list[ContactInfo]:
        return self._contact_infos

    def get_contact_info_by_country(self, country: str) -> ContactInfo | None:
        for info in self._contact_infos:
            if info.country.lower() == country.lower():
                return info
        return None

    def update_contact_info(self, contact_id: int, info: ContactInfo) -> None:
        for idx, current in enumerate(self._contact_infos):
            if current.id == contact_id:
                self._contact_infos[idx] = ContactInfo(id=contact_id, **info.model_dump())
                return

    def add_contact_info(self, info: ContactInfo) -> None:
        self._contact_infos.append(ContactInfo(id=self._next_id, **info.model_dump()))
        self._next_id += 1

    def delete_contact_info(self, contact_id: int) -> None:
        self._contact_infos = [info for info in self._contact_infos if info.id != contact_id]
