from __future__ import annotations

from functools import lru_cache

from supabase import create_client

from app.config import settings


@lru_cache(maxsize=1)
def get_supabase_client():
    """
    Get a cached Supabase client.
    """
    return create_client(settings.supabase_url, settings.supabase_key)

