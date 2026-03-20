from __future__ import annotations

from functools import lru_cache

from supabase import create_client

from app.config import settings


@lru_cache(maxsize=1)
def get_supabase_client():
    """
    Lazily create a Supabase client.

    Returns `None` when Supabase credentials are not configured yet (useful while
    developing before you populate `.env`).
    """

    if not settings.supabase_url or not settings.supabase_key:
        return None

    return create_client(settings.supabase_url, settings.supabase_key)

