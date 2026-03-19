from __future__ import annotations

import pytz

from copy import deepcopy
from datetime import datetime, timezone

from app.models.db.data_models import Quote
from app.config import settings
from app.models.domain.domain_models import QuoteWithProductPreviewsWithQuantity


class QuoteRepository:
    """
    In-memory mock repository using a two-table structure:
    1) quote table
    2) quote_products join table
    """

    def __init__(self):
        self._quote_table: dict[int, Quote] = {}
        self._quote_products_table: list[dict[str, int]] = []
        self._next_quote_id = 1

    def get_all_quotes(self, search: str, page: int, per_page: int):
        # {RULE} Get all quotes entity {RULE}
        all_quotes = [self._hydrate_quote(quote_id) for quote_id in self._quote_table]

        normalized_search = search.strip().lower() if search else ""
        if normalized_search:
            all_quotes = [
                quote for quote in all_quotes
                if self._matches_search(quote, normalized_search)
            ]

        total = len(all_quotes)
        start = (page - 1) * per_page
        end = start + per_page

        return all_quotes[start:end], total

    def get_quote_with_product_previews_with_quantity_by_id(self, id: int) -> QuoteWithProductPreviewsWithQuantity:
        # {RULE} Get quote entity and get all products associated with the quote from the join table, with the quantity from the join table as well{RULE}
        return self._hydrate_quote(id)

    def add_quote_with_product_previews_with_quantity(self, quote_with_product_previews_with_quantity: QuoteWithProductPreviewsWithQuantity) -> int:
        # {RULE} Add quote entity to quote table and add entries to join table for associated products with their quantities {RULE}
        quote_id = self._next_quote_id
        self._next_quote_id += 1

        # Simulate quote entity/table persistence basically quote entity has everything quote has but not the product preview list (that belongs to the join table)
        quote_entity = quote.model_copy(deep=True)
        quote_entity.id = quote_id
        quote_entity.created_at = quote_entity.created_at or datetime.now(pytz.timezone(settings.timezone)).isoformat()
        self._quote_table[quote_id] = quote_entity

        # Simulate quote_products join table persistence
        self.add_products_to_quote(quote_id, quote_entity.product_previews_with_quantity)
        return quote_id

    def update_quote_with_product_previews_with_quantity(self, id: int, quote_with_product_previews_with_quantity: QuoteWithProductPreviewsWithQuantity) -> None:
        # {RULE} Update quote and join table, by first deleting all of quote_id entries in JOIN table, then replacing current quote in db with updated quote, then updating join table accordingly {RULE}
        if id not in self._quote_table:
            return

        updated_quote = quote.model_copy(deep=True)
        updated_quote.id = id
        updated_quote.created_at = updated_quote.created_at or self._quote_table[id].created_at

        self._quote_table[id] = updated_quote
        self.update_products_to_quote(id, updated_quote.product_previews_with_quantity)

    def delete_quote(self, id: int) -> None:
        # {RULE} Del entries in JOIN TABLE FIRST, then delete quote entry {RULE}
        if id not in self._quote_table:
            return

        self._quote_table.pop(id, None)
        self.delete_all_products_from_quote(id)

  
