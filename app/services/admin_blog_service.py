from __future__ import annotations

from typing import List

from app.models.db.data_models import Blog, Category
from app.repositories.blog_repository import BlogRepository
from app.repositories.category_repository import CategoryRepository


class AdminBlogService:
    def __init__(self, *, blog_repo: BlogRepository, category_repo: CategoryRepository) -> None:
        self._blog_repo = blog_repo
        self._category_repo = category_repo

    def upload_blog(self, blog: Blog, categories: List[Category]) -> Blog:
        # BlogCategory join is handled by CategoryRepository.
        blog.categories = categories
        created = self._blog_repo.add_blog(blog)
        self._category_repo.add_categories_to_blog(created.id, categories)
        return created

    def update_blog(self, blog_id: int, blog: Blog, categories: List[Category]) -> None:
        blog.id = blog_id
        blog.categories = categories
        self._blog_repo.update_blog(blog_id, blog)
        self._category_repo.update_categories_of_blog(blog_id, categories)

    def delete_blog(self, blog_id: int) -> None:
        self._blog_repo.delete_blog(blog_id)
        self._category_repo.delete_all_categories_from_blog(blog_id)

