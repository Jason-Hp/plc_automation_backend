from __future__ import annotations

from typing import List

from app.models.db.data_models import Blog, Category
from app.repositories.blog_repository import BlogRepository
from app.repositories.blog_category_repository import BlogCategoryRepository
from app.repositories.category_repository import CategoryRepository


class AdminBlogService:
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

