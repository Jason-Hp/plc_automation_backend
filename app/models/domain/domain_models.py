from __future__ import annotations

from typing import Any, List, Optional 

from pydantic import BaseModel, Field

#
# Domain models must not import from API request/response models or DB models.
# These are business-level shapes used internally by services/controllers.
#


class Manufacturer(BaseModel):
    id: Optional[int] = None
    name: str


class Category(BaseModel):
    id: Optional[int] = None
    name: str


class Product(BaseModel):
    id: Optional[int] = None
    name: str
    part_number: str
    manufacturer: Manufacturer
    image_url: Optional[str] = None
    description: Optional[str] = None

class ProductPreview(BaseModel):
    id: Optional[int]
    name: str
    part_number: str
    manufacturer: Manufacturer

    # image url or product page url
    image_url: Optional[str] = None


class ProductPreviewWithQuantity(ProductPreview):
    quantity: int


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
    def from_quote(cls, quote: BaseModel | dict[str, Any]) -> QuotePreview:
        """
        Build from a Quote-like object (e.g. DB model) without importing DB types.
        """
        data = quote.model_dump() if isinstance(quote, BaseModel) else quote
        return cls.model_validate(data)

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
    def from_request(cls, request: BaseModel | dict[str, Any]) -> QuoteWithProductPreviewsWithQuantity:
        """
        Build from a request-like object without importing API request types.
        """
        data = request.model_dump() if isinstance(request, BaseModel) else request
        return cls.model_validate(data)

class ProductWithStock(BaseModel):
    product: Product
    stock: bool