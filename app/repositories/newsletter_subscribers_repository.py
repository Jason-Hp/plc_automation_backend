from __future__ import annotations

from datetime import datetime
from typing import Set

import pytz

from app.config import settings
from app.utils.supabase_client_util import get_supabase_client


class NewsletterRepository:
    """
    Repository for newsletter subscribers.
    """

    def __init__(self) -> None:
        self._client = get_supabase_client()
        if self._client is None:
            raise RuntimeError("Supabase client is not configured.")

    def is_subscribed(self, email: str) -> bool:
        response = (
            self._client.table("newsletter_subscribers")
            .select("id")
            .eq("email", email.lower())
            .limit(1)
            .execute()
        )
        return bool(response.data)

    def subscribe(self, email: str) -> None:
        subscribed_date = datetime.now(pytz.timezone(settings.timezone)).strftime("%Y-%m-%d")
        self._client.table("newsletter_subscribers").upsert(
            {"email": email.lower(), "subscribed_date": subscribed_date},
            on_conflict="email",
        ).execute()

    def get_all_subscribers(self) -> Set[str]:
        response = (
            self._client.table("newsletter_subscribers")
            .select("email")
            .execute()
        )
        return {r.get("email") for r in (response.data or []) if r.get("email")}
