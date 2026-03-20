from __future__ import annotations

from typing import Optional

from pydantic import BaseModel, Field

class EnquiryRequest(BaseModel):
    name: str = Field(..., min_length=1)
    company_name: str = Field(..., min_length=1)
    country_code: str = Field(..., min_length=1)
    phone: str = Field(..., min_length=5)
    email: str = Field(..., min_length=3)
    message: str = Field("", max_length=2000)
    created_at: Optional[str] = None


class QuoteWithProductPreviewsWithQuantityRequest(EnquiryRequest):
    product_previews_with_quantity: list[ProductPreviewWithQuantityRequest] = Field(
        ..., min_items=1
    )


class ManufacturerRequest(BaseModel):
    id: Optional[int] = None
    name: str


class ProductPreviewWithQuantityRequest(BaseModel):
    id: Optional[int] = None
    name: str
    part_number: str
    manufacturer: ManufacturerRequest

    # image url or product page url
    image_url: Optional[str] = None

    quantity: int


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


# Admin upload/create request DTOs

class CountryRequest(BaseModel):
    id: Optional[int] = None
    name: str
    code: str


class CategoryRequest(BaseModel):
    id: Optional[int] = None
    name: str


class FAQRequest(BaseModel):
    id: Optional[int] = None
    question: str = Field(..., min_length=1)
    answer: str = Field(..., min_length=1)


class ContactInfoRequest(BaseModel):
    id: Optional[int] = None
    address: str
    phone: str
    email: str = Field(..., min_length=3)
    working_hours: str
    country: str


class BlogUploadRequest(BaseModel):
    id: Optional[int] = None
    title: str
    # Stored separately via BlogCategory join table.
    image_url: str
    published_by: str

    # DD - MM - YYYY
    created_at: str
    updated_at: str

    content: str


class JobUploadRequest(BaseModel):
    id: Optional[int] = None
    title: str
    country: str
    location: str
    job_type: str
    posted_date: str  # DD - MM - YYYY

    industry: str
    requirements: str
    responsibilities: str
    description: str
    working_hours: str


class ApprovalRequest(BaseModel):
    id: Optional[int] = None
    type: str
    payload: str
    is_approved: bool
    requester: Optional[str] = None
    request_date: Optional[str] = None  # DD - MM - YYYY
    attachment_url: Optional[str] = None


