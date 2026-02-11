
from fastapi import APIRouter, HTTPException, Query
from app.schemas import Blog, BlogRequest, BlogPreviewListResponse
from app.utils.translation_util import translate_text

from app.repositories.blog_repository import BlogRepository

router = APIRouter(prefix="/blogs", tags=["blogs"])
blog_repo = BlogRepository()

@router.get("/", response_model=BlogPreviewListResponse)
async def get_blogs(
    search: str | None = None,
    category: str | None = None,
    page: int = Query(1, ge=1),
    per_page: int = Query(10, ge=1, le=100)
) -> BlogPreviewListResponse:
    payload = BlogRequest(search=search, category=category)
    response = blog_repo.get_blog_previews(request=payload, page=page, per_page=per_page)
    for blog_preview in response.blog_previews:
        blog_preview.title = translate_text(blog_preview.title)
    return response

@router.get("/{blogId}", response_model=Blog)
async def get_blog(blogId: int) -> Blog:
    blog = blog_repo.get_blog_by_id(blogId)
    if not blog:
        raise HTTPException(status_code=404, detail="Blog not found")

    blog.title = translate_text(blog.title)
    blog.content = translate_text(blog.content)
    return blog
