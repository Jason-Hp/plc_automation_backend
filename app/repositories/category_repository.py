from __future__ import annotations

from typing import Dict, List

from app.schemas import Category


class CategoryRepository:
    def __init__(self):
        self._categories: List[Category] = []
        # In-memory join table: blog_id -> list[Category]
        self._blog_categories: Dict[int, List[Category]] = {}

    def get_all_categories(self) -> list[Category]:
        return self._categories

    def get_category_by_id(self, category_id: int) -> Category | None:
        for category in self._categories:
            if category.id == category_id:
                return category
        return None
    
    def add_categories_to_blog(self, blog_id: int, categories: list[Category]) -> None:
        """
        Associate a set of categories with a blog via a JOIN table
        (e.g. tbl_blog_category with blog_id, category_id).
        """
        self._blog_categories[blog_id] = categories

    def delete_all_categories_from_blog(self, blog_id: int) -> None:
        """
        Remove all category associations for a blog.
        """
        self._blog_categories.pop(blog_id, None)

    def update_categories_of_blog(self, blog_id: int, categories: list[Category]) -> None:
        """
        Replace the categories associated with a blog.
        """
        self.delete_all_categories_from_blog(blog_id)
        self.add_categories_to_blog(blog_id, categories)

    def get_category_by_name(self, name: str) -> Category | None:
        for category in self._categories:
            if category.name.lower() == name.lower():
                return category
        return None

    def add_category(self, category: Category) -> None:
        self._categories.append(category)

    def update_category(self, category_id: int, category: Category) -> None:
        for index, current in enumerate(self._categories):
            if current.id == category_id:
                self._categories[index] = category
                return

    def delete_category(self, category_id: int) -> None:
        self._categories = [category for category in self._categories if category.id != category_id]