from __future__ import annotations

from typing import List

from app.models.db.data_models import Category
from app.utils.supabase_client_util import get_supabase_client


class BlogCategoryRepository:
    """
    Repository for the `blogs_categories` JOIN TABLE.
    """

    def __init__(self) -> None:
        self._client = get_supabase_client()
        if self._client is None:
            raise RuntimeError("Supabase client is not configured.")

    def get_categories_by_blog_id(self, blog_id: int) -> List[Category]:
        join_resp = (
            self._client.table("blogs_categories")
            .select("category_id")
            .eq("blog_id", blog_id)
            .execute()
        )
        join_data = join_resp.data or []
        category_ids = [r.get("category_id") for r in join_data if r.get("category_id") is not None]
        
        if not category_ids:
            return []

        cat_resp = (
            self._client.table("categories")
            .select("id,name")
            .in_("id", category_ids)
            .execute()
        )
        return [Category.model_validate(r) for r in (cat_resp.data or [])]

    def add_categories_to_blog(self, blog_id: int, categories: List[Category]) -> None:
        insert_rows = [
            {"blog_id": blog_id, "category_id": c.id}
            for c in categories
            if c.id is not None
        ]
        if insert_rows:
            self._client.table("blogs_categories").insert(insert_rows).execute()

    def delete_all_categories_from_blog(self, blog_id: int) -> None:
        self._client.table("blogs_categories").delete().eq("blog_id", blog_id).execute()

    def update_categories_of_blog(self, blog_id: int, categories: List[Category]) -> None:
        self.delete_all_categories_from_blog(blog_id)
        self.add_categories_to_blog(blog_id, categories)
