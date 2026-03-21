from __future__ import annotations

from fastapi import HTTPException

from app.models.api.request_models import BlogRequest
from app.models.api.response_models import (
    BlogPreviewListResponse,
    BlogPreviewResponse,
    BlogResponse,
    CategoryResponse,
)
from app.repositories.blog_repository import BlogRepository
from app.repositories.blog_category_repository import BlogCategoryRepository
from app.utils.translation_util import translate_text


class PublicBlogsService:
    def __init__(self, *, blog_repo: BlogRepository, blog_category_repo: BlogCategoryRepository) -> None:
        self._blog_repo = blog_repo
        self._blog_category_repo = blog_category_repo

    def get_blogs(
        self, *, payload: BlogRequest, page: int, per_page: int
    ) -> BlogPreviewListResponse:
        blogs, total = self._blog_repo.get_blog_previews(
            search=payload.search,
            categories=payload.categories,
            page=page,
            per_page=per_page,
        )

        previews = []
        for blog in blogs:
            categories = self._blog_category_repo.get_categories_by_blog_id(blog.id) if blog.id else []
            previews.append(
                BlogPreviewResponse(
                    id=blog.id,
                    title=translate_text(blog.title),
                    categories=[
                        CategoryResponse(id=c.id, name=c.name) for c in categories
                    ],
                    image_url=blog.image_url,
                    published_by=blog.published_by,
                    created_at=blog.created_at,
                    updated_at=blog.updated_at,
                )
            )

        return BlogPreviewListResponse(
            page=page, per_page=per_page, total=total, blog_previews=previews
        )

    def get_blog(self, *, blog_id: int) -> BlogResponse:
        blog = self._blog_repo.get_blog_by_id(blog_id)
        if not blog:
            raise HTTPException(status_code=404, detail="Blog not found")

        categories = self._blog_category_repo.get_categories_by_blog_id(blog_id)
        
        title = translate_text(blog.title)
        content = translate_text(blog.content)
        return BlogResponse(
            id=blog.id,
            title=title,
            categories=[
                CategoryResponse(id=c.id, name=c.name) for c in categories
            ],
            image_url=blog.image_url,
            published_by=blog.published_by,
            created_at=blog.created_at,
            updated_at=blog.updated_at,
            content=content,
        )

