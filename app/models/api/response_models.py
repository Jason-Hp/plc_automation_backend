from __future__ import annotations

from typing import List, Optional

from pydantic import BaseModel

#
# API DTOs (response models)
# These must not depend on domain/db models.
#


class ManufacturerResponse(BaseModel):
    id: Optional[int] = None
    name: str


class CategoryResponse(BaseModel):
    id: Optional[int] = None
    name: str


class CountryResponse(BaseModel):
    id: Optional[int] = None
    name: str
    code: str


class FAQResponse(BaseModel):
    id: Optional[int] = None
    question: str
    answer: str


class ContactInfoResponse(BaseModel):
    id: Optional[int] = None
    address: str
    phone: str
    email: str
    working_hours: str
    country: str


class ProductPreviewResponse(BaseModel):
    id: Optional[int] = None
    name: str
    part_number: str
    manufacturer: ManufacturerResponse

    # image url or product page url
    image_url: Optional[str] = None


class ProductPreviewWithQuantityResponse(ProductPreviewResponse):
    quantity: int


class ProductResponse(BaseModel):
    id: Optional[int] = None
    name: str
    part_number: str
    manufacturer: ManufacturerResponse

    # image url or product page url
    image_url: Optional[str] = None

    description: Optional[str] = None


class ProductWithStockDataResponse(BaseModel):
    product: ProductResponse
    stock: bool


class BlogPreviewResponse(BaseModel):
    id: Optional[int] = None
    title: str
    categories: List[CategoryResponse]
    image_url: Optional[str] = None
    published_by: str

    # DD - MM - YYYY
    created_at: Optional[str] = None
    updated_at: Optional[str] = None


class JobPreviewResponse(BaseModel):
    id: Optional[int] = None
    title: str
    country: str
    location: str
    job_type: str
    posted_date: str  # DD - MM - YYYY


class ApprovalPreviewDataResponse(BaseModel):
    id: int
    type: str
    payload: str
    is_approved: bool
    requester: Optional[str] = None
    request_date: Optional[str] = None  # DD - MM - YYYY
    attachment_url: Optional[str] = None


class QuotePreviewResponse(BaseModel):
    name: str
    company_name: str
    created_at: Optional[str] = None

    is_paid: Optional[bool] = False
    total_amount: Optional[int] = 0


class QuoteWithProductPreviewsWithQuantityDataResponse(BaseModel):
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
    product_previews_with_quantity: List[ProductPreviewWithQuantityResponse]


class BlogResponse(BaseModel):
    id: Optional[int] = None
    title: str
    categories: List[CategoryResponse]
    image_url: Optional[str] = None
    published_by: str

    # DD - MM - YYYY
    created_at: Optional[str] = None
    updated_at: Optional[str] = None

    content: str


class JobResponse(BaseModel):
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


class ApiResponse(BaseModel):
    message: str


class BatchProductUploadResultResponse(BaseModel):
    processed: int
    message: str


class UserInfoResponse(BaseModel):
    uuid: str
    email: str
    user_role: str


class ProductPreviewListResponse(BaseModel):
    product_previews: List[ProductPreviewResponse] = []
    page: int
    per_page: int
    total: int


class QuotePreviewListResponse(BaseModel):
    page: int
    per_page: int
    total: int
    quote_previews: List[QuotePreviewResponse] = []


class QuoteWithProductPreviewsWithQuantityResponse(BaseModel):
    quote_with_product_previews_with_quantity: QuoteWithProductPreviewsWithQuantityDataResponse


class ApprovalPreviewListResponse(BaseModel):
    page: int
    per_page: int
    total: int
    approval_previews: List[ApprovalPreviewDataResponse] = []


class BlogPreviewListResponse(BaseModel):
    page: int
    per_page: int
    total: int
    blog_previews: List[BlogPreviewResponse] = []


class JobPreviewListResponse(BaseModel):
    page: int
    per_page: int
    total: int
    job_previews: List[JobPreviewResponse] = []


class ProductWithStockResponse(BaseModel):
    product_with_stock: ProductWithStockDataResponse

