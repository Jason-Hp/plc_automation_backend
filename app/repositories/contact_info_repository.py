from app.models.db.data_models import ContactInfo
from app.utils.supabase_client_util import get_supabase_client


class ContactInfoRepository:
    def __init__(self):
        self._client = get_supabase_client()
        if self._client is None:
            raise RuntimeError("Supabase client is not configured.")

    def get_all_contact_info(self) -> list[ContactInfo]:
        response = (
            self._client.table("contact_infos")
            .select("id,address,phone,email,working_hours,country")
            .order("id", desc=False)
            .execute()
        )
        return [ContactInfo.model_validate(row) for row in response.data or []]

    def get_contact_info_by_country(self, country: str) -> ContactInfo | None:
        response = (
            self._client.table("contact_infos")
            .select("id,address,phone,email,working_hours,country")
            .ilike("country", country)
            .limit(1)
            .execute()
        )
        rows = response.data or []
        return ContactInfo.model_validate(rows[0]) if rows else None

    def update_contact_info(self, contact_id: int, info: ContactInfo) -> None:
        self._client.table("contact_infos").update(info.model_dump(exclude={"id"})).eq("id", contact_id).execute()

    def add_contact_info(self, info: ContactInfo) -> None:
        row = info.model_dump(exclude={"id"})
        self._client.table("contact_infos").insert(row).execute()

    def delete_contact_info(self, contact_id: int) -> None:
        self._client.table("contact_infos").delete().eq("id", contact_id).execute()
