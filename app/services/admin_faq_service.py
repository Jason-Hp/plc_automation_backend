from __future__ import annotations

from typing import List

from app.models.db.data_models import FAQ
from app.repositories.faq_repository import FaqRepository


class AdminFaqService:
    def __init__(self, *, faq_repo: FaqRepository) -> None:
        self._faq_repo = faq_repo

    def upload_faqs(self, faqs: List[FAQ]) -> None:
        # Repo assigns IDs for in-memory persistence.
        for faq in faqs:
            self._faq_repo.add_faq(faq.question, faq.answer)

    def update_faq(self, faq_id: int, *, question: str, answer: str) -> None:
        self._faq_repo.update_faq(faq_id, question, answer)

    def delete_faq(self, faq_id: int) -> None:
        self._faq_repo.delete_faq(faq_id)

