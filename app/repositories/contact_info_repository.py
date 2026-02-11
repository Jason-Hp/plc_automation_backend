
from app.schemas import ContactInfoRequest, ContactInfoResponse

class ContactInfoRepository:
    def __init__(self):
        pass

    def get_all_contact_info(self) -> list[ContactInfoResponse]:
        pass

    def get_contact_info_by_country(self, country: str) -> ContactInfoResponse:
        pass

    def update_contact_info(self, contact_id: int, info: ContactInfoRequest) -> None:
        pass

    def add_contact_info(self, info: ContactInfoRequest) -> None:
        pass

    def delete_contact_info(self, contact_id: int) -> None:
        pass

