from app.schemas import Category

class CategoryRepository:
    def __init__(self):
        self._categories: list[Category] = []

    def get_all_categories(self) -> list[Category]:
        return self._categories

    def get_category_by_id(self, category_id: int) -> Category | None:
        for category in self._categories:
            if category.id == category_id:
                return category
        return None
    
    def add_categories_to_blog(self, blog_id: int, categories: list[Category]) -> None:
        # Placeholder method to associate categories with a blog in a JOIN table feature id from blog and id from category
        pass

    def delete_all_categories_from_blog(self, blog_id: int) -> None:
        # Placeholder method to remove all category associations for a blog in a JOIN table
        pass

    def update_categories_of_blog(self, blog_id: int, categories: list[Category]) -> None:
        # Placeholder method to update category associations for a blog in a JOIN table\
        delete_all_categories_from_blog(blog_id)
        add_categories_to_blog(blog_id, categories)
        pass

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