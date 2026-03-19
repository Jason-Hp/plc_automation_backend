from __future__ import annotations

from fastapi import APIRouter, HTTPException, Query

from app.dependencies import country_repo, product_repo
from app.models.api.response_models import ProductPreviewListResponse, ProductWithStockResponse
from app.models.domain.domain_models import ProductPreview, ProductWithStock
from app.utils.translation_util import translate_text
from app.utils.context_util import country_context

router = APIRouter(tags=["products"])
@router.get("/products", response_model=ProductPreviewListResponse)
async def list_products(
    page: int = Query(1, ge=1),
    per_page: int = Query(30, ge=1, le=100),
    search: str | None = None,
) -> ProductPreviewListResponse:
     
    #TODO: implement semantic search here later
    products, total = product_repo.list_products(page=page, per_page=per_page, search=search)
    return ProductPreviewListResponse(
        product_previews=[ProductPreview.model_validate(product) for product in products],
        page=page,
        per_page=per_page,
        total=total
    )

@router.get("/products/{product_id}", response_model=Product)
async def get_product(product_id: int) -> ProductWithStockResponse:
    product = product_repo.get_product_by_id(product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    country_name = country_context.get()
    country = country_repo.get_country_by_name(country_name)
    product_with_stock = ProductWithStock(product=product, stock=True)
    if country and country.id is not None and product.id is not None:
        if not country_repo.get_product_availability_by_country(country.id, product.id):
            product_with_stock.stock = False

    if product_with_stock.product.description:
        product_with_stock.product.description = translate_text(product_with_stock.product.description)

    return product_with_stock
