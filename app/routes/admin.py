from __future__ import annotations

import csv
import io
import json
from typing import Optional

from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile, status, Query
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from pydantic import ValidationError

from app.schemas import QuoteListResponse, Quote, Country, Manufacturer, Category, Job, Product, Blog, BatchProductUploadResult, AdminLoginRequest, ApiResponse, NewsLetterContentRequest, FAQ, ContactInfo
from app.config import Settings
from app.dependencies import (
    blog_repo,
    category_repo,
    contact_info_repo,
    country_repo,
    email_service,
    faq_repo,
    job_repo,
    jwt_service,
    manufacturer_repo,
    newsletter_repo,
    product_repo,
    quote_repo
)
from app.services.jwt_service import JwtTokenError

router = APIRouter(prefix="/admin", tags=["admin"])
settings = Settings()
security = HTTPBearer()

async def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)) -> dict:
    try:
        token = credentials.credentials
        payload = jwt_service.decode_jwt_token(token)
        return payload
    except JwtTokenError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(exc)
        ) from exc

# TODO: refactor
# This is a batch upload and/or update using CSV
@router.post("/products/batch", response_model=BatchProductUploadResult)
async def upload_offer_products(
    csv_file: UploadFile = File(...),
    token_data: dict = Depends(verify_token)
) -> BatchProductUploadResult:
    if not csv_file.filename.endswith(".csv"):
        raise HTTPException(status_code=400, detail="Only CSV files are supported.")

    payload = await csv_file.read()
    # TODO: error handling for CSV parsing
    text_stream = io.StringIO(payload.decode("utf-8", errors="ignore"))
    reader = csv.DictReader(text_stream)

    processed = 0
    for row in reader:
        # TODO: Replace with DB upsert into offer product tables.
        _ = row
        processed += 1

    return BatchProductUploadResult(processed=processed, message="CSV processed (placeholder).")

@router.post("/products", response_model=ApiResponse)
async def upload_product(
    product: Product,
    country_ids: list[int],
    token_data: dict = Depends(verify_token)
) -> ApiResponse:
    product_repo.add_product(product)
    country_repo.add_product_availability_for_country(country_ids, product.id)
    return ApiResponse(message="Product uploaded successfully.")

@router.put("/products/{product_id}", response_model=ApiResponse)
async def update_product(
    product_id: int,
    product: Product,
    country_ids: list[int],
    token_data: dict = Depends(verify_token)
) -> ApiResponse:
    product_repo.update_product(product_id, product)
    country_repo.update_product_availability_for_country(country_ids, product.id)
    return ApiResponse(message="Product updated successfully.")


@router.delete("/products/{product_id}", response_model=ApiResponse)
async def delete_product(
    product_id: int,
    token_data: dict = Depends(verify_token)
) -> ApiResponse:
    product_repo.delete_product(product_id)
    country_repo.delete_all_product_availability_for_country(product_id)
    return ApiResponse(message="Product deleted successfully.") 

@router.post("/broadcast-newsletter", response_model=ApiResponse)
async def broadcast_newsletter(
    payload: str = Form(...),
    attachments: list[UploadFile] = File(default=[]),
    token_data: dict = Depends(verify_token)
) -> ApiResponse:
    try:
        parsed_payload = NewsLetterContentRequest.model_validate_json(payload)
    except ValidationError as exc:
        raise HTTPException(status_code=422, detail=json.loads(exc.json())) from exc

    subscribers = newsletter_repo.get_all_subscribers()
    cc_addrs = list(subscribers)

    email_attachments = None

    if attachments:
        email_attachments = []
        for attachment in attachments:
            email_attachments.append(
                (attachment.filename, await attachment.read(), attachment.content_type or "application/octet-stream")
            )

    email_service.send(
        parsed_payload.subject,
        parsed_payload.content,
        email_service.smtp_from,
        cc_addrs,
        email_attachments
    )

    return ApiResponse(message="Newsletter broadcasted.")

@router.post("/faqs", response_model=ApiResponse)
async def upload_faqs(
    faqs: list[FAQ],
    token_data: dict = Depends(verify_token)
) -> ApiResponse:
    
    # Able to do batching here (But not needed as adding FAQs is not frequent or big)
    for faq in faqs:
        faq_repo.add_faq(faq.question, faq.answer)

    return ApiResponse(message="FAQs uploaded successfully.")

@router.put("/faqs/{faq_id}", response_model=ApiResponse)
async def update_faq(
    faq_id: int,
    faq: FAQ,
    token_data: dict = Depends(verify_token)
) -> ApiResponse:
    
    faq_repo.update_faq(faq_id, faq.question, faq.answer)

    return ApiResponse(message="FAQ updated successfully.")

@router.delete("/faqs/{faq_id}", response_model=ApiResponse)
async def delete_faq(
    faq_id: int,
    token_data: dict = Depends(verify_token)
) -> ApiResponse:
    
    faq_repo.delete_faq(faq_id)

    return ApiResponse(message="FAQ deleted successfully.")

@router.post("/contact-info", response_model=ApiResponse)
async def upload_contact_info(
    contact_info: ContactInfo,
    token_data: dict = Depends(verify_token)
) -> ApiResponse:
    
    contact_info_repo.add_contact_info(contact_info)

    return ApiResponse(message="Contact info uploaded successfully.")

@router.put("/contact-info/{contact_id}", response_model=ApiResponse)
async def update_contact_info(
    contact_id: int,
    contact_info: ContactInfo,
    token_data: dict = Depends(verify_token)
) -> ApiResponse:
    
    contact_info_repo.update_contact_info(contact_id, contact_info)

    return ApiResponse(message="Contact info updated successfully.")

@router.delete("/contact-info/{contact_id}", response_model=ApiResponse)
async def delete_contact_info(
    contact_id: int,
    token_data: dict = Depends(verify_token)
) -> ApiResponse:
    
    contact_info_repo.delete_contact_info(contact_id)

    return ApiResponse(message="Contact info deleted successfully.")

@router.post("/blogs", response_model=ApiResponse)
async def upload_blog(
    blog: Blog,
    categories: list[Category],
    token_data: dict = Depends(verify_token)
) -> ApiResponse:
    
    blog = blog_repo.add_blog(blog)
    category_repo.add_categories_to_blog(blog.id, categories)
    return ApiResponse(message="Blog uploaded successfully.")

@router.put("/blogs/{blog_id}", response_model=ApiResponse)
async def update_blog(
    blog_id: int,
    blog: Blog,
    categories: list[Category],
    token_data: dict = Depends(verify_token)
) -> ApiResponse:
    
    blog_repo.update_blog(blog_id, blog)
    category_repo.update_categories_of_blog(blog_id, categories)

    return ApiResponse(message="Blog updated successfully.")

@router.delete("/blogs/{blog_id}", response_model=ApiResponse)
async def delete_blog(
    blog_id: int,
    token_data: dict = Depends(verify_token)
) -> ApiResponse:
    
    blog_repo.delete_blog(blog_id)
    category_repo.delete_all_categories_from_blog(blog_id)

    return ApiResponse(message="Blog deleted successfully.")

@router.post("/jobs", response_model=ApiResponse)
async def upload_job(
    job: Job,
    token_data: dict = Depends(verify_token)
) -> ApiResponse:
    
    job_repo.add_job(job)

    return ApiResponse(message="Job uploaded successfully.")

@router.put("/jobs/{job_id}", response_model=ApiResponse)
async def update_job(
    job_id: int,
    job: Job,
    token_data: dict = Depends(verify_token)
) -> ApiResponse:
    
    job_repo.update_job(job_id, job)

    return ApiResponse(message="Job updated successfully.")

@router.delete("/jobs/{job_id}", response_model=ApiResponse)
async def delete_job(
    job_id: int,
    token_data: dict = Depends(verify_token)
) -> ApiResponse:
    
    job_repo.delete_job(job_id)

    return ApiResponse(message="Job deleted successfully.")

@router.post("/categories", response_model=ApiResponse)
async def upload_category(
    category: Category,
    token_data: dict = Depends(verify_token)
) -> ApiResponse:
    
    category_repo.add_category(category)

    return ApiResponse(message="Category uploaded successfully.")

@router.put("/categories/{category_id}", response_model=ApiResponse)
async def update_category(
    category_id: int,
    category: Category,
    token_data: dict = Depends(verify_token)
) -> ApiResponse:
    
    category_repo.update_category(category_id, category)

    return ApiResponse(message="Category updated successfully.")

@router.delete("/categories/{category_id}", response_model=ApiResponse)
async def delete_category(  
    category_id: int,
    token_data: dict = Depends(verify_token)
) -> ApiResponse:
    
    category_repo.delete_category(category_id)

    return ApiResponse(message="Category deleted successfully.")

@router.post("/manufacturers", response_model=ApiResponse)
async def upload_manufacturer(
    manufacturer: Manufacturer,
    token_data: dict = Depends(verify_token)
) -> ApiResponse:
    
    manufacturer_repo.add_manufacturer(manufacturer)

    return ApiResponse(message="Manufacturer uploaded successfully.")

@router.put("/manufacturers/{manufacturer_id}", response_model=ApiResponse)
async def update_manufacturer(
    manufacturer_id: int,
    manufacturer: Manufacturer,
    token_data: dict = Depends(verify_token)
) -> ApiResponse:
    
    manufacturer_repo.update_manufacturer(manufacturer_id, manufacturer)

    return ApiResponse(message="Manufacturer updated successfully.")

@router.delete("/manufacturers/{manufacturer_id}", response_model=ApiResponse)
async def delete_manufacturer(  
    manufacturer_id: int,
    token_data: dict = Depends(verify_token)
) -> ApiResponse:
    
    manufacturer_repo.delete_manufacturer(manufacturer_id)

    return ApiResponse(message="Manufacturer deleted successfully.")

@router.post("/countries", response_model=ApiResponse)
async def upload_country(
    country: Country,
    token_data: dict = Depends(verify_token)
) -> ApiResponse:
    
    country_repo.add_country(country)

    return ApiResponse(message="Country uploaded successfully.")

@router.put("/countries/{country_id}", response_model=ApiResponse)
async def update_country(
    country_id: int,
    country: Country,
    token_data: dict = Depends(verify_token)
) -> ApiResponse:
    
    country_repo.update_country(country_id, country)

    return ApiResponse(message="Country updated successfully.")

@router.delete("/countries/{country_id}", response_model=ApiResponse)
async def delete_country(  
    country_id: int,
    token_data: dict = Depends(verify_token)
) -> ApiResponse:
    
    country_repo.delete_country(country_id)

    return ApiResponse(message="Country deleted successfully.")

# TODO: In the future, can look into filter (filter by is_paid, amount, created_at...)
@router.get("/quotes", response_model=QuoteListResponse)
async def get_all_quotes(
    token_data: dict = Depends(verify_token),
    search: Optional[str] = "",
    page: int = Query(1, ge=1),
    per_page: int = Query(10, ge=1, le=100)
) -> QuoteListResponse:
    
    return quote_repo.get_all_quotes(search, page, per_page)

@router.get("/quote/{quote_id}", response_model=Quote)
async def get_quote_by_id(
    quote_id: int,
    token_data: dict = Depends(verify_token)
) -> Quote:
    
    return quote_repo.get_quote_by_id(quote_id)

@router.post("/quotes", response_model=ApiResponse)
async def add_quote(
    quote: Quote,
    token_data: dict = Depends(verify_token)
) -> ApiResponse:
    
    quote_repo.add_quote(quote)

    return ApiResponse(message="Quote added successfully.")

@router.put("/quote/{quote_id}", response_model=ApiResponse)
async def update_quote(
    quote_id: int,
    quote: Quote,
    token_data: dict = Depends(verify_token)
) -> ApiResponse:
    
    quote_repo.update_quote(quote_id, quote)
    return ApiResponse(message="Quote updated successfully.")

@router.delete("/quote/{quote_id}", response_model=ApiResponse)
async def delete_quote(
    quote_id: int,
    token_data: dict = Depends(verify_token)
) -> ApiResponse:
    
    quote_repo.delete_quote(quote_id)

    return ApiResponse(message="Quote deleted successfully.")

@router.post("/login")
async def admin_login(payload: AdminLoginRequest) -> str:
    # TODO: return jwt token 3 hour expiry (need to change how password is accessed here for sec reasons)
    if payload.username == settings.admin_username and payload.password == settings.admin_password:
        jwt_token = jwt_service.create_jwt_token(payload.username)
        return jwt_token
    else:
        raise HTTPException(status_code=401, detail="Invalid credentials")

