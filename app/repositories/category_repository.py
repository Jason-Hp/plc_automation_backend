from __future__ import annotations

from typing import Dict, List

from app.models.db.data_models import Category
from app.utils.supabase_client_util import get_supabase_client


class CategoryRepository:
    def __init__(self):
        self._client = get_supabase_client()
        if self._client is None:
            raise RuntimeError("Supabase client is not configured.")

    def get_all_categories(self) -> list[Category]:
        response = (
            self._client.table("categories")
            .select("id,name")
            .order("id", desc=False)
            .execute()
        )
        return [Category.model_validate(r) for r in response.data or []]

    def get_category_by_id(self, category_id: int) -> Category | None:
        response = (
            self._client.table("categories")
            .select("id,name")
            .eq("id", category_id)
            .limit(1)
            .execute()
        )
        rows = response.data or []
        return Category.model_validate(rows[0]) if rows else None
    
    def get_category_by_name(self, name: str) -> Category | None:
        response = (
            self._client.table("categories")
            .select("id,name")
            .ilike("name", name)
            .limit(1)
            .execute()
        )
        rows = response.data or []
        return Category.model_validate(rows[0]) if rows else None

    def add_category(self, category: Category) -> None:
        self._client.table("categories").insert(
            category.model_dump(exclude={"id"})
        ).execute()

    def update_category(self, category_id: int, category: Category) -> None:
        self._client.table("categories").update(
            category.model_dump(exclude={"id"})
        ).eq("id", category_id).execute()

    def delete_category(self, category_id: int) -> None:
        self._client.table("categories").delete().eq("id", category_id).execute()
        self._client.table("blogs_categories").delete().eq("category_id", category_id).execute()