from app.models.db.data_models import FAQ
from app.utils.supabase_client_util import get_supabase_client

class FaqRepository:
    def __init__(self):
        self._client = get_supabase_client()
        if self._client is None:
            raise RuntimeError("Supabase client is not configured.")

    def get_all_faqs(self) -> list[FAQ]:
        response = (
            self._client.table("faqs")
            .select("id,question,answer")
            .order("id", desc=False)
            .execute()
        )
        return [FAQ.model_validate(row) for row in response.data or []]

    def add_faq(self, question: str, answer: str) -> None:
        self._client.table("faqs").insert(
            {"question": question, "answer": answer}
        ).execute()

    def delete_faq(self, faq_id: int) -> None:
        self._client.table("faqs").delete().eq("id", faq_id).execute()

    def update_faq(self, faq_id: int, question: str, answer: str) -> None:
        self._client.table("faqs").update(
            {"question": question, "answer": answer}
        ).eq("id", faq_id).execute()
