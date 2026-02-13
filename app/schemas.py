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

class ProductPreview(BaseModel):
    id: str
    name: str
    part_number: str

    # image url or product page url
    image_url: Optional[str] = None

class Product(ProductPreview):
    manufacturer: Optional[str] = None
    stock: Optional[bool] = None
    description: Optional[str] = None
    available_for_countries: Optional[set[str]] = None

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


class NewsletterRequest(BaseModel):
    email: str = Field(..., min_length=3)

class OfferProductUploadResult(BaseModel):
    processed: int
    message: str

class AdminLoginRequest(BaseModel):
    username: str = Field(..., min_length=1)
    password: str = Field(..., min_length=1)

class NewsLetterContentRequest(BaseModel):
    subject: str = Field(..., min_length=1)
    content: str = Field(..., min_length=1)

# TODO: refactor these schema FAQ, req and resp -> for FAQ and Contact Info
class FAQRequest(BaseModel):
    question: str = Field(..., min_length=1)
    answer: str = Field(..., min_length=1)

class FAQResponse(FAQRequest):
    id: int

class ContactInfoRequest(BaseModel):
    address: str
    phone: str
    email: str = Field(..., min_length=3)
    working_hours: str
    country: str


class ContactInfoResponse(ContactInfoRequest):
    id: int

class BlogPreview(BaseModel):
    id: int
    title: str
    category: str
    image_url: str
    published_by: str

    # DD - MM - YYYY
    created_at: str
    updated_at: str

class Blog(BlogPreview):
    content: str

class BlogRequest(BaseModel):
    search: Optional[str]
    category: Optional[str]


class BlogPreviewListResponse(BaseModel):
    page: int
    per_page: int
    total: int
    blog_previews: List[BlogPreview] = []

class JobPreview(BaseModel):
    id: int
    title: str
    country: str
    location: str
    job_type: str
    posted_date: str  # DD - MM - YYYY

class Job(JobPreview):
    industry: str
    requirements: str
    responsibilities: str
    descritpion: str
    working_hours: str

class JobApplicationRequest(BaseModel):
    first_name: str = Field(..., min_length=1)
    last_name: str = Field(..., min_length=1)
    email: str = Field(..., min_length=3)
    country_code: str = Field(..., min_length=1)
    phone: str = Field(..., min_length=5)
    experience: str = Field(..., min_length=1)

