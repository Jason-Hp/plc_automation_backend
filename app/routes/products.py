from __future__ import annotations

from fastapi import APIRouter, HTTPException, Query

from app.repositories.product_repository import ProductRepository
from app.repositories.country_repository import CountryRepository
from app.schemas import ProductPreviewListResponse, Product
from app.utils.translation_util import translate_text
from app.utils.context_util import country_context

router = APIRouter(tags=["products"])
product_repo = ProductRepository()
country_repo = CountryRepository()

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

    country_name = country_context.get()
    country = country_repo.get_country_by_name(country_name)

    if not country_repo.get_product_availability_by_country(country.id, product.id):
        product.stock = False

    if product.description:
        product.description = translate_text(product.description)

    return product
