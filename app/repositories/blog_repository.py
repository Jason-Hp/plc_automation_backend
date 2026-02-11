from app.schemas import Blog, BlogRequest, BlogPreviewListResponse

class BlogRepository:
    
    def __init__(self):
        pass

    def get_blog_previews(self, request: BlogRequest, page: int, per_page: int) -> BlogPreviewListResponse:
        pass

    def get_blog_by_id(self, blog_id: int) -> Blog | None:
        pass

    def add_blog(self, blog: Blog) -> None:
        pass

    def update_blog(self, blog_id: int, blog: Blog) -> None:
        pass

    def delete_blog(self, blog_id: int) -> None:
        pass