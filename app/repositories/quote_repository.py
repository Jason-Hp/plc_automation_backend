from __future__ import annotations

import pytz

from datetime import datetime, timezone

from app.models.db.data_models import Quote
from app.config import settings
from app.utils.supabase_client_util import get_supabase_client


class QuoteRepository:
    """
    In-memory mock repository using a two-table structure:
    1) quote table
    2) quote_products join table
    """

    def __init__(self) -> None:
        self._quote_table: dict[int, Quote] = {}
        self._next_quote_id = 1
        self._client = get_supabase_client()

    def _matches_search(self, quote: Quote, normalized_search: str) -> bool:
        fields = [
            quote.name,
            quote.company_name,
            quote.email,
            quote.phone,
            quote.message,
            quote.country_code,
        ]
        return any(f and normalized_search in f.lower() for f in fields)

    def get_all_quotes(self, search: str, page: int, per_page: int) -> tuple[list[Quote], int]:
        if self._client is None:
            all_quotes = list(self._quote_table.values())

            normalized_search = search.strip().lower() if search else ""
            if normalized_search:
                all_quotes = [q for q in all_quotes if self._matches_search(q, normalized_search)]

            total = len(all_quotes)
            start = (page - 1) * per_page
            end = start + per_page
            return all_quotes[start:end], total

        query = (
            self._client.table("tbl_quotes")
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
        if self._client is None:
            if quote_id not in self._quote_table:
                raise KeyError(quote_id)
            return self._quote_table[quote_id]

        resp = (
            self._client.table("tbl_quotes")
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
        quote_id = self._next_quote_id
        self._next_quote_id += 1

        if self._client is None:
            quote_entity = quote.model_copy(deep=True)
            quote_entity.id = quote_id
            quote_entity.created_at = quote_entity.created_at or datetime.now(pytz.timezone(settings.timezone)).isoformat()
            self._quote_table[quote_id] = quote_entity
            return quote_id

        row = quote.model_dump(exclude={"id"})
        insert_resp = self._client.table("tbl_quotes").insert(row).execute()
        inserted = (insert_resp.data or [])[:1]
        if inserted and inserted[0].get("id") is not None:
            return inserted[0]["id"]
        return quote_id

    def update_quote(self, quote: Quote) -> None:
        if self._client is None:
            if quote.id is None or quote.id not in self._quote_table:
                return

            updated_quote = quote.model_copy(deep=True)
            # Preserve created_at if caller didn't provide it.
            updated_quote.created_at = updated_quote.created_at or self._quote_table[quote.id].created_at
            self._quote_table[quote.id] = updated_quote
            return

        if quote.id is None:
            return
        self._client.table("tbl_quotes").update(
            quote.model_dump(exclude={"id"})
        ).eq("id", quote.id).execute()

    def delete_quote(self, quote_id: int) -> None:
        if self._client is None:
            self._quote_table.pop(quote_id, None)
            return

        self._client.table("tbl_quotes").delete().eq("id", quote_id).execute()