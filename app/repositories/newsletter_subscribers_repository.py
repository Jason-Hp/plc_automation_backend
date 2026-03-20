from __future__ import annotations

from datetime import datetime
from typing import Set

import pytz

from app.config import settings
from app.utils.supabase_client_util import get_supabase_client


class NewsletterRepository:
    """
    Placeholder repository. Replace with database-backed implementation.
    """

    def __init__(self) -> None:
        self._subscribers: Set[str] = set()
        self._client = get_supabase_client()

    def is_subscribed(self, email: str) -> bool:
        if self._client is None:
            # {RULE} Check if email already in table {RULE}
            return email.lower() in self._subscribers

        response = (
            self._client.table("newsletter_subscribers")
            .select("id")
            .eq("email", email.lower())
            .limit(1)
            .execute()
        )
        return bool(response.data)

    def subscribe(self, email: str) -> None:
        if self._client is None:
            # {RULE} Add NewsletterSubscriber entity with email and current date in SGT {RULE}
            self._subscribers.add(email.lower())
            return

        subscribed_date = datetime.now(pytz.timezone(settings.timezone)).isoformat()
        self._client.table("newsletter_subscribers").upsert(
            {"email": email.lower(), "subscribed_date": subscribed_date},
            on_conflict="email",
        ).execute()

    def get_all_subscribers(self) -> Set[str]:
        if self._client is None:
            # {RULE} Return all emails only basically {RULE}
            return self._subscribers

        response = (
            self._client.table("newsletter_subscribers")
            .select("email")
            .execute()
        )
        return {r.get("email") for r in (response.data or []) if r.get("email")}
