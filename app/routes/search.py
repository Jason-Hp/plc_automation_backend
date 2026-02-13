
from fastapi import APIRouter, Query
from app.dependencies import search_service
from app.schemas import ProductPreview

router = APIRouter(tags=["search"]) 
@router.get("/semantic-search", response_model=list[ProductPreview])
async def semantic_search(
    query: str = Query(..., min_length=1, max_length=500),
    top_k: int = Query(10, ge=1, le=20)
) -> list[ProductPreview]:
    results = search_service.semantic_search(query=query, top_k=top_k)
    return results