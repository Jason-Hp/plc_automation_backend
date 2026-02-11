from __future__ import annotations

from fastapi import APIRouter, HTTPException, Query

from app.repositories.product_repository import ProductRepository
from app.schemas import ProductPreviewListResponse, Product
from app.utils.translation_util import translate_text
from app.utils.context_util import country_context

router = APIRouter(tags=["products"])
product_repo = ProductRepository()


@router.get("/products", response_model=ProductPreviewListResponse)
async def list_products(
    page: int = Query(1, ge=1),
    per_page: int = Query(30, ge=1, le=100),
    category: str | None = None,
    search: str | None = None,
) -> ProductPreviewListResponse:
     
    #TODO: implement semantic search here later
    return product_repo.list_products(page=page, per_page=per_page, category=category, search=search)

@router.get("/products/{product_id}", response_model=Product)
async def get_product(product_id: str) -> Product:
    product = product_repo.get_product_by_id(product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    country = country_context.get()
    # If not available in the country, set stock to False to indicate that it's not orderable. This is a temporary workaround until we have proper product availability handling in place.
    if product.available_for_countries and country not in product.available_for_countries:
        product.stock = False

    if product.description:
        product.description = translate_text(product.description)

    return product
