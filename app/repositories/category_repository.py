from __future__ import annotations

from typing import Dict, List

from app.models.db.data_models import Category
from app.utils.supabase_client_util import get_supabase_client


class CategoryRepository:
    def __init__(self):
        self._categories: List[Category] = []
        # In-memory join table: blog_id -> list[Category]
        self._blog_categories: Dict[int, List[Category]] = {}
        self._client = get_supabase_client()

    def get_all_categories(self) -> list[Category]:
        if self._client is None:
            return self._categories

        response = (
            self._client.table("tbl_category")
            .select("id,name")
            .order("id", desc=False)
            .execute()
        )
        return [Category.model_validate(r) for r in response.data or []]

    def get_category_by_id(self, category_id: int) -> Category | None:
        if self._client is None:
            for category in self._categories:
                if category.id == category_id:
                    return category
            return None

        response = (
            self._client.table("tbl_category")
            .select("id,name")
            .eq("id", category_id)
            .limit(1)
            .execute()
        )
        rows = response.data or []
        return Category.model_validate(rows[0]) if rows else None
    
    def add_categories_to_blog(self, blog_id: int, categories: list[Category]) -> None:
        """
        Associate a set of categories with a blog via a JOIN table
        (e.g. tbl_blog_category with blog_id, category_id).
        """
        if self._client is None:
            self._blog_categories[blog_id] = categories
            return

        insert_rows = [
            {"blog_id": blog_id, "category_id": c.id}
            for c in categories
            if c.id is not None
        ]
        if insert_rows:
            self._client.table("tbl_blog_category").insert(insert_rows).execute()

    def delete_all_categories_from_blog(self, blog_id: int) -> None:
        """
        Remove all category associations for a blog.
        """
        if self._client is None:
            self._blog_categories.pop(blog_id, None)
            return

        self._client.table("tbl_blog_category").delete().eq("blog_id", blog_id).execute()

    def update_categories_of_blog(self, blog_id: int, categories: list[Category]) -> None:
        """
        Replace the categories associated with a blog.
        """
        if self._client is None:
            self.delete_all_categories_from_blog(blog_id)
            self.add_categories_to_blog(blog_id, categories)
            return

        self.delete_all_categories_from_blog(blog_id)
        self.add_categories_to_blog(blog_id, categories)

    def get_category_by_name(self, name: str) -> Category | None:
        if self._client is None:
            for category in self._categories:
                if category.name.lower() == name.lower():
                    return category
            return None

        response = (
            self._client.table("tbl_category")
            .select("id,name")
            .ilike("name", name)
            .limit(1)
            .execute()
        )
        rows = response.data or []
        return Category.model_validate(rows[0]) if rows else None

    def add_category(self, category: Category) -> None:
        if self._client is None:
            self._categories.append(category)
            return

        self._client.table("tbl_category").insert(
            category.model_dump(exclude={"id"})
        ).execute()

    def update_category(self, category_id: int, category: Category) -> None:
        if self._client is None:
            for index, current in enumerate(self._categories):
                if current.id == category_id:
                    self._categories[index] = category
                    return
            return

        self._client.table("tbl_category").update(
            category.model_dump(exclude={"id"})
        ).eq("id", category_id).execute()

    def delete_category(self, category_id: int) -> None:
        if self._client is None:
            self._categories = [category for category in self._categories if category.id != category_id]
            return

        self._client.table("tbl_category").delete().eq("id", category_id).execute()
        self._client.table("tbl_blog_category").delete().eq("category_id", category_id).execute()