
from fastapi import APIRouter, Query
from app.dependencies import search_service
from app.schemas import ProductPreview
from app.models.api.response_models import ProductPreviewListResponse

router = APIRouter(tags=["search"]) 
@router.get("/semantic-search", response_model=ProductPreviewListResponse)
async def semantic_search(
    query: str = Query(..., min_length=1, max_length=500),
    top_k: int = Query(10, ge=1, le=20)
) -> ProductPreviewListResponse:
    results = search_service.semantic_search(query=query, top_k=top_k)
    return ProductPreviewListResponse(product_previews=results, page=1, per_page=top_k, total=len(results))