from app.models.db.data_models import FAQ
from app.utils.supabase_client_util import get_supabase_client

class FaqRepository:
    def __init__(self):
        self._faqs: list[FAQ] = []
        self._next_id = 1
        self._client = get_supabase_client()

    def get_all_faqs(self) -> list[FAQ]:
        if self._client is None:
            return self._faqs

        response = (
            self._client.table("faqs")
            .select("id,question,answer")
            .order("id", desc=False)
            .execute()
        )
        return [FAQ.model_validate(row) for row in response.data or []]

    def add_faq(self, question: str, answer: str) -> None:
        if self._client is None:
            self._faqs.append(FAQ(id=self._next_id, question=question, answer=answer))
            self._next_id += 1
            return

        self._client.table("faqs").insert(
            {"question": question, "answer": answer}
        ).execute()

    def delete_faq(self, faq_id: int) -> None:
        if self._client is None:
            self._faqs = [faq for faq in self._faqs if faq.id != faq_id]
            return

        self._client.table("faqs").delete().eq("id", faq_id).execute()

    def update_faq(self, faq_id: int, question: str, answer: str) -> None:
        if self._client is None:
            for idx, faq in enumerate(self._faqs):
                if faq.id == faq_id:
                    self._faqs[idx] = FAQ(
                        id=faq_id, question=question, answer=answer
                    )
                    return
            return

        self._client.table("faqs").update(
            {"question": question, "answer": answer}
        ).eq("id", faq_id).execute()
