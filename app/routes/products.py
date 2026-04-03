from __future__ import annotations

from fastapi import APIRouter, Query

from app.dependencies import product_service
from app.models.api.response_models import (
    ProductPreviewListResponse,
    ProductWithStockResponse,
)
from app.utils.context_util import country_context

router = APIRouter(tags=["products"])
@router.get("/products", response_model=ProductPreviewListResponse)
async def list_product_previews(
    page: int = Query(1, ge=1),
    per_page: int = Query(30, ge=1, le=100),
    search: str | None = None,
) -> ProductPreviewListResponse:
     
    #TODO: implement semantic search here later
    return product_service.list_product_previews(
        page=page, per_page=per_page, search=search
    )

@router.get("/products/{product_id}", response_model=ProductWithStockResponse)
async def get_product(product_id: int) -> ProductWithStockResponse:
    country_name = country_context.get()
    return product_service.get_product_with_stock(
        product_id=product_id, country_name=country_name
    )
