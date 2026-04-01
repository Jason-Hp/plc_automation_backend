from __future__ import annotations

from typing import Optional

from pydantic import BaseModel, Field


class Manufacturer(BaseModel):
    id: Optional[int] = None
    name: str


class Country(BaseModel):
    id: Optional[int] = None
    name: str
    code: str


class Category(BaseModel):
    id: Optional[int] = None
    name: str


class Product(BaseModel):
    id: Optional[int]
    name: str
    part_number: str
    manufacturer: Manufacturer

    # image url or product page url
    image_url: Optional[str] = None

    description: Optional[str] = None


class FAQ(BaseModel):
    id: Optional[int] = None
    question: str = Field(..., min_length=1)
    answer: str = Field(..., min_length=1)


class ContactInfo(BaseModel):
    id: Optional[int] = None
    address: str
    phone: str
    email: str = Field(..., min_length=3)
    working_hours: Optional[str] = None
    country: str


class Blog(BaseModel):
    id: Optional[int] = None
    title: str
    image_url: Optional[str] = None
    published_by: str

    # DD - MM - YYYY
    created_at: Optional[str] = None
    updated_at: Optional[str] = None

    content: str


class Job(BaseModel):
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
    working_hours: Optional[str] = None


class Approval(BaseModel):
    id: Optional[int] = None
    type: str
    payload: str
    is_approved: bool
    requester: Optional[str] = None
    request_date: Optional[str] = None  # DD - MM - YYYY
    attachment_url: Optional[str] = None


class NewsletterSubscriber(BaseModel):
    id: Optional[int] = None
    email: str = Field(..., min_length=3)
    subscribed_date: Optional[str] = None


class Quote(BaseModel):
    name: str = Field(..., min_length=1)
    company_name: str = Field(..., min_length=1)
    country_code: str = Field(..., min_length=1)
    phone: str = Field(..., min_length=5)
    email: str = Field(..., min_length=3)
    message: str = Field("", max_length=2000)
    created_at: Optional[str] = None

    id: Optional[int] = None
    is_paid: Optional[bool] = False
    total_amount: Optional[int] = 0

# The below are data models for JOIN TABLES
# Do not use them if not needed; Always conform to using JOINs in SQL queries

class QuoteProduct(BaseModel):
    quote_id: int
    product_id: int
    quantity: int


class ProductCountry(BaseModel):
    product_id: int
    country_id: int


class BlogCategory(BaseModel):
    blog_id: int
    category_id: int

