from __future__ import annotations

from typing import List, Optional 

from pydantic import BaseModel, Field

from app.models.api.request_models import QuoteWithProductPreviewsWithQuantityRequest
from app.models.db.data_models import Manufacturer, Category, Product, Quote, Quote

class ProductPreview(BaseModel):
    id: Optional[int]
    name: str
    part_number: str
    manufacturer: Manufacturer

    # image url or product page url
    image_url: Optional[str] = None


class ProductPreviewWithQuantity(ProductPreview):
    quantity: int


class BlogPreview(BaseModel):
    id: Optional[int] = None
    title: str
    categories: List[Category]
    image_url: str
    published_by: str

    # DD - MM - YYYY
    created_at: str
    updated_at: str


class ApprovalPreview(BaseModel):
    type: str
    payload: str
    is_approved: bool
    requester: Optional[str] = None
    request_date: Optional[str] = None  # DD - MM - YYYY
    attachment_url: Optional[str] = None


class JobPreview(BaseModel):
    id: Optional[int] = None
    title: str
    country: str
    location: str
    job_type: str
    posted_date: str  # DD - MM - YYYY

class QuotePreview(BaseModel):
    name: str = Field(..., min_length=1)
    company_name: str = Field(..., min_length=1)
    created_at: Optional[str] = None

    is_paid: Optional[bool] = False
    total_amount: Optional[int] = 0

    @classmethod
    def from_quote(cls, quote: Quote) -> QuotePreview:
        return cls.model_validate(quote.model_dump())

class QuoteWithProductPreviewsWithQuantity(BaseModel):
    # Quote table fields
    name: str
    company_name: str
    country_code: str
    phone: str
    email: str
    message: str = ""
    created_at: Optional[str] = None

    id: Optional[int] = None
    is_paid: Optional[bool] = False
    total_amount: Optional[int] = 0

    # Join table `quotes_products`
    product_previews_with_quantity: list[ProductPreviewWithQuantity]

    @classmethod
    def from_request(cls, request: QuoteWithProductPreviewsWithQuantityRequest):
        return cls.model_validate(request.model_dump())

class ProductWithStock(BaseModel):
    product: Product
    stock: bool