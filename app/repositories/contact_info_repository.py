from app.models.db.data_models import ContactInfo
from app.utils.supabase_client_util import get_supabase_client


class ContactInfoRepository:
    def __init__(self):
        self._contact_infos: list[ContactInfo] = []
        self._next_id = 1
        self._client = get_supabase_client()

    def get_all_contact_info(self) -> list[ContactInfo]:
        if self._client is None:
            return self._contact_infos

        response = (
            self._client.table("tbl_contact_info")
            .select("id,address,phone,email,working_hours,country")
            .order("id", desc=False)
            .execute()
        )
        return [ContactInfo.model_validate(row) for row in response.data or []]

    def get_contact_info_by_country(self, country: str) -> ContactInfo | None:
        if self._client is None:
            for info in self._contact_infos:
                if info.country.lower() == country.lower():
                    return info
            return None

        response = (
            self._client.table("tbl_contact_info")
            .select("id,address,phone,email,working_hours,country")
            .ilike("country", country)
            .limit(1)
            .execute()
        )
        rows = response.data or []
        return ContactInfo.model_validate(rows[0]) if rows else None

    def update_contact_info(self, contact_id: int, info: ContactInfo) -> None:
        if self._client is None:
            for idx, current in enumerate(self._contact_infos):
                if current.id == contact_id:
                    self._contact_infos[idx] = ContactInfo(
                        id=contact_id, **info.model_dump()
                    )
                    return
            return

        self._client.table("tbl_contact_info").update(info.model_dump(exclude={"id"})).eq("id", contact_id).execute()

    def add_contact_info(self, info: ContactInfo) -> None:
        if self._client is None:
            self._contact_infos.append(
                ContactInfo(id=self._next_id, **info.model_dump())
            )
            self._next_id += 1
            return

        row = info.model_dump(exclude={"id"})
        self._client.table("tbl_contact_info").insert(row).execute()

    def delete_contact_info(self, contact_id: int) -> None:
        if self._client is None:
            self._contact_infos = [info for info in self._contact_infos if info.id != contact_id]
            return

        self._client.table("tbl_contact_info").delete().eq("id", contact_id).execute()
