from typing import List, Optional

from pydantic import BaseModel, Field

class ApiResponse(BaseModel):
    message: str
    
class EnquiryRequest(BaseModel):
    name: str = Field(..., min_length=1)
    company_name: str = Field(..., min_length=1)
    country_code: str = Field(..., min_length=1)
    phone: str = Field(..., min_length=5)
    email: str = Field(..., min_length=3)
    message: str = Field("", max_length=2000)
    created_at: Optional[str] = None

class Manufacturer(BaseModel):
    id: Optional[int] = None
    name: str

class ProductPreview(BaseModel):
    id: Optional[int]
    name: str
    part_number: str
    manufacturer: Manufacturer

    # image url or product page url
    image_url: Optional[str] = None

# Potentially remove code
class Country(BaseModel):
    id: Optional[int] = None
    name: str
    code: str

class Product(ProductPreview):
    stock: bool
    description: Optional[str] = None

class ProductPreviewListResponse(BaseModel):
    product_previews: List[ProductPreview] = []
    page: int
    per_page: int
    total: int

class ProductPreviewWithQuantity(ProductPreview):
    quantity: int

# Extends EnquiryRequest
class QuoteRequest(EnquiryRequest):
    product_previews_with_quantity: List[ProductPreviewWithQuantity] = Field(..., min_items=1)

class Quote(QuoteRequest):
    id: Optional[int] = None
    is_paid: Optional[bool] = False
    total_amount: Optional[int] = 0

class QuoteListResponse(BaseModel):
    page: int
    per_page: int
    total: int
    quotes: list[Quote] = []

class NewsletterRequest(BaseModel):
    email: str = Field(..., min_length=3)

class BatchProductUploadResult(BaseModel):
    processed: int
    message: str

class AdminLoginRequest(BaseModel):
    username: str = Field(..., min_length=1)
    password: str = Field(..., min_length=1)

class NewsLetterContentRequest(BaseModel):
    subject: str = Field(..., min_length=1)
    content: str = Field(..., min_length=1)

# TODO: refactor these schema FAQ, req and resp -> for FAQ and Contact Info
class FAQ(BaseModel):
    id: Optional[int] = None
    question: str = Field(..., min_length=1)
    answer: str = Field(..., min_length=1)

class ContactInfo(BaseModel):
    id: Optional[int] = None
    address: str
    phone: str
    email: str = Field(..., min_length=3)
    working_hours: str
    country: str

class Category(BaseModel):
    id: Optional[int] = None
    name: str

class BlogPreview(BaseModel):
    id: Optional[int] = None
    title: str
    categories: List[Category]
    image_url: str
    published_by: str

    # DD - MM - YYYY
    created_at: str
    updated_at: str

class Blog(BlogPreview):
    content: str

class BlogRequest(BaseModel):
    search: Optional[str]
    categories: Optional[list[Category]]


class BlogPreviewListResponse(BaseModel):
    page: int
    per_page: int
    total: int
    blog_previews: List[BlogPreview] = []

class JobPreview(BaseModel):
    id: Optional[int] = None
    title: str
    country: str
    location: str
    job_type: str
    posted_date: str  # DD - MM - YYYY

class Job(JobPreview):
    industry: str
    requirements: str
    responsibilities: str
    description: str
    working_hours: str

class JobApplicationRequest(BaseModel):
    first_name: str = Field(..., min_length=1)
    last_name: str = Field(..., min_length=1)
    email: str = Field(..., min_length=3)
    country_code: str = Field(..., min_length=1)
    phone: str = Field(..., min_length=5)
    experience: str = Field(..., min_length=1)

class Approval(BaseModel):
    id: Optional[int] = None
    type: str
    payload: str
    is_approved: bool
    requester: Optional[str] = None
    request_date: Optional[str] = None  # DD - MM - YYYY
    attachment_url: Optional[str] = None

class ApprovalResponse(BaseModel):
    page: int
    per_page: int
    total: int
    approvals: list[Approval] = []