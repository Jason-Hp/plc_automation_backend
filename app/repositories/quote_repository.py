from __future__ import annotations

from copy import deepcopy
from datetime import datetime, timezone

from app.schemas import Quote, QuoteListResponse, ProductPreviewWithQuantity


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

    def get_all_quotes(self, search: str, page: int, per_page: int) -> QuoteListResponse:
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

        return QuoteListResponse(
            page=page,
            per_page=per_page,
            total=total,
            quotes=all_quotes[start:end],
        )

    def get_quote_by_id(self, id: int) -> Quote:
        return self._hydrate_quote(id)

    def add_quote(self, quote: Quote) -> int:
        quote_id = self._next_quote_id
        self._next_quote_id += 1

        # Simulate quote entity/table persistence
        quote_entity = quote.model_copy(deep=True)
        quote_entity.id = quote_id
        quote_entity.created_at = quote_entity.created_at or datetime.now(timezone.utc).isoformat()
        self._quote_table[quote_id] = quote_entity

        # Simulate quote_products join table persistence
        self.add_products_to_quote(quote_id, quote_entity.product_previews_with_quantity)
        return quote_id

    def update_quote(self, id: int, quote: Quote) -> None:
        if id not in self._quote_table:
            return

        updated_quote = quote.model_copy(deep=True)
        updated_quote.id = id
        updated_quote.created_at = updated_quote.created_at or self._quote_table[id].created_at

        self._quote_table[id] = updated_quote
        self.update_products_to_quote(id, updated_quote.product_previews_with_quantity)

    def delete_quote(self, id: int) -> None:
        if id not in self._quote_table:
            return

        self._quote_table.pop(id, None)
        self.delete_all_products_from_quote(id)

    # Join Table stuff
    def add_products_to_quote(self, quote_id: int, products: list[ProductPreviewWithQuantity]) -> None:
        for product in products:
            if product.id is None:
                continue
            self._quote_products_table.append(
                {
                    "quote_id": quote_id,
                    "product_id": product.id,
                    "quantity": product.quantity,
                }
            )

    def delete_all_products_from_quote(self, quote_id: int) -> None:
        self._quote_products_table = [
            entry
            for entry in self._quote_products_table
            if entry["quote_id"] != quote_id
        ]

    def update_products_to_quote(self, quote_id: int, products: list[ProductPreviewWithQuantity]) -> None:
        self.delete_all_products_from_quote(quote_id)
        self.add_products_to_quote(quote_id, products)

    def _hydrate_quote(self, quote_id: int) -> Quote:
        quote = self._quote_table.get(quote_id)
        if not quote:
            raise KeyError(f"Quote with id={quote_id} not found")

        hydrated_quote = quote.model_copy(deep=True)
        join_rows = [
            entry
            for entry in self._quote_products_table
            if entry["quote_id"] == quote_id
        ]

        quantities_by_product_id = {
            row["product_id"]: row["quantity"]
            for row in join_rows
        }

        hydrated_products = []
        for product in hydrated_quote.product_previews_with_quantity:
            copied_product = deepcopy(product)
            if copied_product.id is not None and copied_product.id in quantities_by_product_id:
                copied_product.quantity = quantities_by_product_id[copied_product.id]
            hydrated_products.append(copied_product)

        hydrated_quote.product_previews_with_quantity = hydrated_products
        return hydrated_quote

    def _matches_search(self, quote: Quote, search: str) -> bool:
        quote_fields = [
            quote.name,
            quote.company_name,
            quote.country_code,
            quote.phone,
            quote.email,
            quote.message,
            str(quote.id or ""),
            str(quote.total_amount or ""),
        ]

        if any(search in str(value).lower() for value in quote_fields):
            return True

        for product in quote.product_previews_with_quantity:
            product_fields = [
                product.name,
                product.part_number,
                product.manufacturer.name,
                str(product.quantity),
            ]
            if any(search in str(value).lower() for value in product_fields):
                return True

        return False
