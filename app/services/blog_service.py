from __future__ import annotations

from typing import List
from fastapi import HTTPException

from app.models.db.data_models import Blog, Category
from app.models.api.request_models import BlogRequest
from app.models.api.response_models import (
    BlogPreviewListResponse,
    BlogPreviewResponse,
    BlogResponse,
    CategoryResponse,
)
from app.repositories.blog_repository import BlogRepository
from app.repositories.blog_category_repository import BlogCategoryRepository
from app.repositories.category_repository import CategoryRepository
from app.utils.translation_util import translate_text


class BlogService:
    def __init__(
        self,
        *,
        blog_repo: BlogRepository,
        category_repo: CategoryRepository,
        blog_category_repo: BlogCategoryRepository,
    ) -> None:
        self._blog_repo = blog_repo
        self._category_repo = category_repo
        self._blog_category_repo = blog_category_repo

    # --- Public Methods ---

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

    # --- Admin Methods ---

    def upload_blog(self, blog: Blog, categories: List[Category]) -> Blog:
        created = self._blog_repo.add_blog(blog)
        if created.id:
            self._blog_category_repo.add_categories_to_blog(created.id, categories)
        return created

    def update_blog(self, blog_id: int, blog: Blog, categories: List[Category]) -> None:
        blog.id = blog_id
        self._blog_repo.update_blog(blog_id, blog)
        self._blog_category_repo.update_categories_of_blog(blog_id, categories)

    def delete_blog(self, blog_id: int) -> None:
        self._blog_repo.delete_blog(blog_id)
        self._blog_category_repo.delete_all_categories_from_blog(blog_id)
