from __future__ import annotations

from typing import List

from app.schemas import Blog, BlogPreview, BlogPreviewListResponse, BlogRequest


class BlogRepository:
    def __init__(self):
        self._blogs: List[Blog] = []

    def get_blog_previews(self, request: BlogRequest, page: int, per_page: int) -> BlogPreviewListResponse:
        filtered = self._blogs

        # Filter by categories if provided (match by name or id)
        if request.categories:
            requested_names = {c.name.lower() for c in request.categories if c.name}
            requested_ids = {c.id for c in request.categories if c.id is not None}

            def has_matching_category(blog: Blog) -> bool:
                blog_names = {c.name.lower() for c in blog.categories}
                blog_ids = {c.id for c in blog.categories if c.id is not None}
                return bool(requested_names & blog_names) or bool(requested_ids & blog_ids)

            filtered = [blog for blog in filtered if has_matching_category(blog)]

        if request.search:
            query = request.search.lower()
            filtered = [blog for blog in filtered if query in blog.title.lower()]

        total = len(filtered)
        start = (page - 1) * per_page
        end = start + per_page

        previews: List[BlogPreview] = [
            BlogPreview(
                id=blog.id,
                title=blog.title,
                categories=blog.categories,
                image_url=blog.image_url,
                published_by=blog.published_by,
                created_at=blog.created_at,
                updated_at=blog.updated_at,
            )
            for blog in filtered[start:end]
        ]

        return BlogPreviewListResponse(page=page, per_page=per_page, total=total, blog_previews=previews)

    def get_blog_by_id(self, blog_id: int) -> Blog | None:
        for blog in self._blogs:
            if blog.id == blog_id:
                return blog
        return None

    def add_blog(self, blog: Blog) -> Blog:
        # Simple in-memory ID assignment if not provided
        if blog.id is None:
            next_id = (max((b.id or 0) for b in self._blogs) + 1) if self._blogs else 1
            blog.id = next_id

        self._blogs.append(blog)
        return blog

    def update_blog(self, blog_id: int, blog: Blog) -> None:
        for index, current in enumerate(self._blogs):
            if current.id == blog_id:
                self._blogs[index] = blog
                return

    def delete_blog(self, blog_id: int) -> None:
        self._blogs = [blog for blog in self._blogs if blog.id != blog_id]
