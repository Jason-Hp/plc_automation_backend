from __future__ import annotations

from typing import Optional

from datetime import datetime
import pytz

from app.config import settings
from app.models.db.data_models import Blog
from app.utils.supabase_client_util import get_supabase_client


class BlogRepository:
    def __init__(self):
        self._client = get_supabase_client()
        if self._client is None:
            raise RuntimeError("Supabase client is not configured.")

    def get_blog_previews(
        self,
        search: Optional[str],
        categories: Optional[list[str]],
        page: int,
        per_page: int,
    ) -> tuple[list[Blog], int]:
        """
        Repository returns DB models only.
        """
        # Supabase-backed implementation.
        blog_table = "blogs"
        join_table = "blogs_categories"
        category_table = "categories"

        blog_ids_filter = None
        if categories:
            requested = [c for c in categories if c]
            if requested:
                # Resolve category IDs from category names.
                cats = (
                    self._client.table(category_table)
                    .select("id,name")
                    .in_("name", requested)
                    .execute()
                )
                category_rows = cats.data or []
                category_ids = [r.get("id") for r in category_rows if r.get("id") is not None]
                if not category_ids:
                    return [], 0

                join_rows = (
                    self._client.table(join_table)
                    .select("blog_id,category_id")
                    .in_("category_id", category_ids)
                    .execute()
                )
                join_data = join_rows.data or []
                blog_ids_filter = list({r.get("blog_id") for r in join_data if r.get("blog_id") is not None})

        query = self._client.table(blog_table).select(
            "id,title,image_url,published_by,created_at,updated_at,content"
        )
        if search:
            query = query.ilike("title", f"%{search}%")

        if blog_ids_filter is not None:
            query = query.in_("id", blog_ids_filter)

        # Fetch slice.
        start = (page - 1) * per_page
        end = start + per_page - 1
        slice_resp = query.order("id", desc=False).range(start, end).execute()
        blog_rows = slice_resp.data or []

        # Total count (best-effort).
        total_resp = query.execute()
        total = len(total_resp.data or [])

        blogs_out = [Blog.model_validate(row) for row in blog_rows]
        return blogs_out, total

    def get_blog_by_id(self, blog_id: int) -> Blog | None:
        response = (
            self._client.table("blogs")
            .select("id,title,image_url,published_by,created_at,updated_at,content")
            .eq("id", blog_id)
            .limit(1)
            .execute()
        )
        rows = response.data or []
        if not rows:
            return None

        return Blog.model_validate(rows[0])

    def add_blog(self, blog: Blog) -> Blog:
        blog.created_at = blog.updated_at = datetime.now(pytz.timezone(settings.timezone)).strftime("%Y-%m-%d")

        row = blog.model_dump(exclude={"id"})
        insert_resp = self._client.table("blogs").insert(row).execute()

        inserted = (insert_resp.data or [])[:1]
        if inserted and inserted[0].get("id") is not None:
            blog.id = inserted[0]["id"]
        return blog

    def update_blog(self, blog_id: int, blog: Blog) -> None:
        blog.updated_at = datetime.now(pytz.timezone(settings.timezone)).strftime("%Y-%m-%d")
        row = blog.model_dump(exclude={"id", "created_at"})
        self._client.table("blogs").update(row).eq("id", blog_id).execute()

    def delete_blog(self, blog_id: int) -> None:
        self._client.table("blogs").delete().eq("id", blog_id).execute()
