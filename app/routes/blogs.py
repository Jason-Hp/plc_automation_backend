
from fastapi import APIRouter, Query
from app.models.api.request_models import BlogRequest
from app.models.api.response_models import BlogPreviewListResponse, BlogResponse

from app.dependencies import blog_service

router = APIRouter(prefix="/blogs", tags=["blogs"])

@router.post("/", response_model=BlogPreviewListResponse)
async def get_blogs(
    payload: BlogRequest,
    page: int = Query(1, ge=1),
    per_page: int = Query(10, ge=1, le=100)
) -> BlogPreviewListResponse:
    return blog_service.get_blogs(
        payload=payload, page=page, per_page=per_page
    )

@router.get("/{blogId}", response_model=BlogResponse)
async def get_blog(blogId: int) -> BlogResponse:
    return blog_service.get_blog(blog_id=blogId)
