from app.schemas import Blog, BlogRequest, BlogPreviewListResponse


class BlogRepository:
    def __init__(self):
        self._blogs: list[Blog] = []

    def get_blog_previews(self, request: BlogRequest, page: int, per_page: int) -> BlogPreviewListResponse:
        filtered = self._blogs

        if request.category:
            filtered = [blog for blog in filtered if blog.category.lower() == request.category.lower()]

        if request.search:
            query = request.search.lower()
            filtered = [blog for blog in filtered if query in blog.title.lower()]

        total = len(filtered)
        start = (page - 1) * per_page
        end = start + per_page

        previews = [
            blog.model_dump(include={"id", "title", "category", "image_url", "published_by", "created_at", "updated_at"})
            for blog in filtered[start:end]
        ]

        return BlogPreviewListResponse(page=page, per_page=per_page, total=total, blog_previews=previews)

    def get_blog_by_id(self, blog_id: int) -> Blog | None:
        for blog in self._blogs:
            if blog.id == blog_id:
                return blog
        return None

    def add_blog(self, blog: Blog) -> None:
        self._blogs.append(blog)

    def update_blog(self, blog_id: int, blog: Blog) -> None:
        for index, current in enumerate(self._blogs):
            if current.id == blog_id:
                self._blogs[index] = blog
                return

    def delete_blog(self, blog_id: int) -> None:
        self._blogs = [blog for blog in self._blogs if blog.id != blog_id]
