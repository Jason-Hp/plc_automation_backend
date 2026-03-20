from __future__ import annotations

from typing import Optional

from app.models.db.data_models import Blog
from app.utils.supabase_client_util import get_supabase_client


class BlogRepository:
    def __init__(self):
        self._blogs: list[Blog] = []
        self._client = get_supabase_client()

    def get_blog_previews(
        self,
        search: Optional[str],
        categories: Optional[list[str]],
        page: int,
        per_page: int,
    ) -> tuple[list[Blog], int]:
        """
        Repository returns DB models only.
        Controller/routes are responsible for mapping to API DTOs.
        """
        if self._client is None:
            filtered = self._blogs

            if categories:
                requested = {c.lower() for c in categories if c}

                def has_matching_category(blog: Blog) -> bool:
                    blog_names = {c.name.lower() for c in blog.categories}
                    return bool(requested & blog_names)

                filtered = [blog for blog in filtered if has_matching_category(blog)]

            if search:
                query = search.lower()
                filtered = [blog for blog in filtered if query in blog.title.lower()]

            total = len(filtered)
            start = (page - 1) * per_page
            end = start + per_page
            return filtered[start:end], total

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

        # Hydrate categories for returned blogs.
        blog_ids = [r.get("id") for r in blog_rows if r.get("id") is not None]
        if not blog_ids:
            return [], total

        join_resp = (
            self._client.table(join_table)
            .select("blog_id,category_id")
            .in_("blog_id", blog_ids)
            .execute()
        )
        join_data = join_resp.data or []
        category_ids = list({r.get("category_id") for r in join_data if r.get("category_id") is not None})
        categories_map = {}
        if category_ids:
            cat_resp = (
                self._client.table(category_table)
                .select("id,name")
                .in_("id", category_ids)
                .execute()
            )
            categories_map = {r.get("id"): r for r in (cat_resp.data or [])}

        blogs_out: list[Blog] = []
        for row in blog_rows:
            bid = row.get("id")
            # Build categories list.
            cats = [
                {
                    "id": r.get("category_id"),
                    "name": (categories_map.get(r.get("category_id")) or {}).get("name"),
                }
                for r in join_data
                if r.get("blog_id") == bid and r.get("category_id") is not None
            ]
            # Filter out any missing category names.
            cats = [c for c in cats if c.get("name")]

            blog_obj = Blog.model_validate(
                {
                    **row,
                    "categories": cats,
                }
            )
            blogs_out.append(blog_obj)

        return blogs_out, total

    def get_blog_by_id(self, blog_id: int) -> Blog | None:
        if self._client is None:
            for blog in self._blogs:
                if blog.id == blog_id:
                    return blog
            return None

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

        row = rows[0]

        join_resp = (
            self._client.table("blogs_categories")
            .select("category_id")
            .eq("blog_id", blog_id)
            .execute()
        )
        join_data = join_resp.data or []
        category_ids = [r.get("category_id") for r in join_data if r.get("category_id") is not None]
        cats = []
        if category_ids:
            cat_resp = (
                self._client.table("categories")
                .select("id,name")
                .in_("id", category_ids)
                .execute()
            )
            cats = cat_resp.data or []

        blog_obj = Blog.model_validate({**row, "categories": cats})
        return blog_obj

    def add_blog(self, blog: Blog) -> Blog:
        if self._client is None:
            # Simple in-memory ID assignment if not provided
            if blog.id is None:
                next_id = (max((b.id or 0) for b in self._blogs) + 1) if self._blogs else 1
                blog.id = next_id

            self._blogs.append(blog)
            return blog

        row = blog.model_dump(exclude={"categories"})
        insert_resp = self._client.table("blogs").insert(row).execute()
        # Supabase may return inserted rows; best-effort assignment.
        inserted = (insert_resp.data or [])[:1]
        if inserted and inserted[0].get("id") is not None:
            blog.id = inserted[0]["id"]
        return blog

    def update_blog(self, blog_id: int, blog: Blog) -> None:
        if self._client is None:
            for index, current in enumerate(self._blogs):
                if current.id == blog_id:
                    self._blogs[index] = blog
                    return
            return

        row = blog.model_dump(exclude={"id", "categories"})
        self._client.table("blogs").update(row).eq("id", blog_id).execute()

    def delete_blog(self, blog_id: int) -> None:
        if self._client is None:
            self._blogs = [blog for blog in self._blogs if blog.id != blog_id]
            return

        self._client.table("blogs").delete().eq("id", blog_id).execute()
