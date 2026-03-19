from __future__ import annotations

from typing import Optional

from pydantic import BaseModel, Field

from app.models.domain.domain_models import ProductPreviewWithQuantity


class EnquiryRequest(BaseModel):
    name: str = Field(..., min_length=1)
    company_name: str = Field(..., min_length=1)
    country_code: str = Field(..., min_length=1)
    phone: str = Field(..., min_length=5)
    email: str = Field(..., min_length=3)
    message: str = Field("", max_length=2000)
    created_at: Optional[str] = None


class QuoteWithProductPreviewsWithQuantityRequest(EnquiryRequest):
    product_previews_with_quantity: list[ProductPreviewWithQuantity] = Field(..., min_items=1)


class NewsletterRequest(BaseModel):
    email: str = Field(..., min_length=3)


class AdminLoginRequest(BaseModel):
    username: str = Field(..., min_length=1)
    password: str = Field(..., min_length=1)


class NewsLetterContentRequest(BaseModel):
    subject: str = Field(..., min_length=1)
    content: str = Field(..., min_length=1)


class BlogRequest(BaseModel):
    search: Optional[str]
    categories: Optional[list[str]]


class JobApplicationRequest(BaseModel):
    first_name: str = Field(..., min_length=1)
    last_name: str = Field(..., min_length=1)
    email: str = Field(..., min_length=3)
    country_code: str = Field(..., min_length=1)
    phone: str = Field(..., min_length=5)
    experience: str = Field(..., min_length=1)


class AccountCreationRequest(BaseModel):
    email: str = Field(..., min_length=3)
    password: str = Field(..., min_length=6)
    user_role: str = Field(..., min_length=1)

class ProductWithCountriesRequest(BaseModel):
    id: Optional[int] = None
    name: str
    part_number: str
    manufacturer: str

    # image url or product page url
    image_url: Optional[str] = None

    description: Optional[str] = None

    countries: list[str]

