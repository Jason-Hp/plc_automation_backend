from __future__ import annotations



from app.models.db.data_models import Quote
from app.utils.supabase_client_util import get_supabase_client


class QuoteRepository:
    """
    Repository for quotes.
    """

    def __init__(self) -> None:
        self._client = get_supabase_client()
        if self._client is None:
            raise RuntimeError("Supabase client is not configured.")

    def get_all_quotes(self, search: str, page: int, per_page: int) -> tuple[list[Quote], int]:
        query = (
            self._client.table("quotes")
            .select("*")
        )
        if search:
            query = query.ilike("name", f"%{search}%")

        total_resp = query.execute()
        total = len(total_resp.data or [])

        start = (page - 1) * per_page
        end = start + per_page - 1
        slice_resp = query.order("id", desc=False).range(start, end).execute()
        return [Quote.model_validate(r) for r in (slice_resp.data or [])], total

    def get_quote_by_id(self, quote_id: int) -> Quote:
        resp = (
            self._client.table("quotes")
            .select("*")
            .eq("id", quote_id)
            .limit(1)
            .execute()
        )
        rows = resp.data or []
        if not rows:
            raise KeyError(quote_id)
        return Quote.model_validate(rows[0])

    def add_quote(self, quote: Quote) -> int:
        row = quote.model_dump(exclude={"id"})
        insert_resp = self._client.table("quotes").insert(row).execute()
        inserted = (insert_resp.data or [])[:1]
        if inserted and inserted[0].get("id") is not None:
            return inserted[0]["id"]
        raise RuntimeError("Failed to add quote")

    def update_quote(self, quote: Quote) -> None:
        if quote.id is None:
            return
        self._client.table("quotes").update(
            quote.model_dump(exclude={"id"})
        ).eq("id", quote.id).execute()

    def delete_quote(self, quote_id: int) -> None:
        self._client.table("quotes").delete().eq("id", quote_id).execute()