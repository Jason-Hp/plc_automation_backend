from __future__ import annotations

from typing import List, Optional

from pydantic import BaseModel

from app.models.domain.domain_models import JobPreview, ApprovalPreview, ProductPreview, ProductWithStock, QuotePreview, QuoteWithProductPreviewsWithQuantity, BlogPreview


class ApiResponse(BaseModel):
    message: str


class BatchProductUploadResult(BaseModel):
    processed: int
    message: str


class UserInfoResponse(BaseModel):
    uuid: str
    email: str
    user_role: str


class ProductPreviewListResponse(BaseModel):
    product_previews: List[ProductPreview] = []
    page: int
    per_page: int
    total: int


class QuotePreviewListResponse(BaseModel):
    page: int
    per_page: int
    total: int
    quote_previews: list[QuotePreview] = []


class QuoteWithProductPreviewsWithQuantityResponse(BaseModel):
    quote_with_product_previews_with_quantity: QuoteWithProductPreviewsWithQuantity


class ApprovalPreviewResponse(BaseModel):
    page: int
    per_page: int
    total: int
    approvals: list[ApprovalPreview] = []


class BlogPreviewListResponse(BaseModel):
    page: int
    per_page: int
    total: int
    blog_previews: List[BlogPreview] = []


class JobPreviewListResponse(BaseModel):
    page: int
    per_page: int
    total: int
    jobs: list[JobPreview] = []
    posted_date: str  # DD - MM - YYYY


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

class ProductWithStockResponse(BaseModel):
    product_with_stock: ProductWithStock