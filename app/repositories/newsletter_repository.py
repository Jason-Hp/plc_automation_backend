from __future__ import annotations

from typing import Set


class NewsletterRepository:
    """
    Placeholder repository. Replace with database-backed implementation.
    """

    def __init__(self) -> None:
        self._subscribers: Set[str] = set()

    def is_subscribed(self, email: str) -> bool:
        return email.lower() in self._subscribers

    def subscribe(self, email: str) -> None:
        self._subscribers.add(email.lower())

    def get_all_subscribers(self) -> Set[str]:
        return self._subscribers
