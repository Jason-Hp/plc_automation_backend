from __future__ import annotations

from typing import List, Tuple
from datetime import datetime
import pytz

from app.config import settings
from app.models.api.request_models import QuoteWithProductPreviewsWithQuantityRequest
from app.models.db.data_models import Quote
from app.models.domain.domain_models import QuoteWithProductPreviewsWithQuantity
from app.repositories.quote_product_repository import QuoteProductRepository
from app.repositories.quote_repository import QuoteRepository


class QuotesService:
    """
    Business logic for quote lifecycle.

    Repositories:
      - `QuoteRepository` persists the `quotes` table.
      - `QuoteProductRepository` persists the `quotes_products` join table.
    """

    def __init__(
        self,
        *,
        quote_repo: QuoteRepository,
        quote_product_repo: QuoteProductRepository,
    ) -> None:
        self._quote_repo = quote_repo
        self._quote_product_repo = quote_product_repo

    def list_quotes(self, search: str, page: int, per_page: int) -> Tuple[List[Quote], int]:
        return self._quote_repo.get_all_quotes(search, page, per_page)

    def get_quote_with_products(self, quote_id: int) -> QuoteWithProductPreviewsWithQuantity:
        quote = self._quote_repo.get_quote_by_id(quote_id)
        product_previews = self._quote_product_repo.get_product_previews_with_quantity_by_quote_id(quote_id)
        return QuoteWithProductPreviewsWithQuantity.model_validate(
            {**quote.model_dump(), "product_previews_with_quantity": product_previews}
        )

    def create_quote(self, request: QuoteWithProductPreviewsWithQuantityRequest) -> int:
        domain_quote = QuoteWithProductPreviewsWithQuantity.from_request(request)
        db_quote = Quote.model_validate(domain_quote.model_dump())
        db_quote.created_at = datetime.now(pytz.timezone(settings.timezone)).strftime("%Y-%m-%d %H:%M:%S")
        quote_id = self._quote_repo.add_quote(db_quote)
        self._quote_product_repo.add_products_to_quote_with_quantity(
            quote_id, domain_quote.product_previews_with_quantity
        )
        return quote_id

    def update_quote(self, quote_id: int, request: QuoteWithProductPreviewsWithQuantityRequest) -> None:
        domain_quote = QuoteWithProductPreviewsWithQuantity.from_request(request)
        db_quote = Quote.model_validate(domain_quote.model_dump())
        db_quote.id = quote_id

        self._quote_repo.update_quote(db_quote)
        self._quote_product_repo.update_products_to_quote_with_quantity(
            quote_id, domain_quote.product_previews_with_quantity
        )

    def delete_quote(self, quote_id: int) -> None:
        self._quote_repo.delete_quote(quote_id)
        self._quote_product_repo.delete_products_to_quote_with_quantity(quote_id)

