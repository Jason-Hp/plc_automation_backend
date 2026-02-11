from __future__ import annotations

import csv
import io

from fastapi import APIRouter, File, HTTPException, UploadFile, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthCredentials

from app.schemas import Product, Blog, OfferProductUploadResult, AdminLoginRequest, ApiResponse, NewsLetterContentRequest, FAQRequest, ContactInfoRequest
from app.services.jwt_service import JwtService, EmailService
from app.repositories.newsletter_repository import NewsletterRepository
from app.repositories.faq_repository import FaqRepository
from app.repositories.contact_info_repository import ContactInfoRepository
from app.repositories.blog_repository import BlogRepository
from app.repositories.product_repository import ProductRepository

router = APIRouter(prefix="/admin", tags=["admin"])
jwt_svc = JwtService()
security = HTTPBearer()
newsletter_repo = NewsletterRepository()
email_svc = EmailService()
faq_repo = FaqRepository()
contact_info_repo = ContactInfoRepository()
blog_repo = BlogRepository()
product_repo = ProductRepository()

async def verify_token(credentials: HTTPAuthCredentials = Depends(security)) -> dict:
    try:
        token = credentials.credentials
        payload = jwt_svc.decode_jwt_token(token)
        return payload
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e)
        )

# TODO: refactor
# This is a batch upload and/or update using CSV
@router.post("/products/batch", response_model=OfferProductUploadResult)
async def upload_offer_products(
    csv_file: UploadFile = File(...),
    token_data: dict = Depends(verify_token)
) -> OfferProductUploadResult:
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

    return OfferProductUploadResult(processed=processed, message="CSV processed (placeholder).")

@router.post("/products", response_model=ApiResponse)
async def upload_product(
    product: Product,
    token_data: dict = Depends(verify_token)
) -> ApiResponse:
    product_repo.add_product(product)
    
    return ApiResponse(message="Product uploaded successfully.")

@router.put("/products/{product_id}", response_model=ApiResponse)
async def update_product(
    product_id: str,
    product: Product,
    token_data: dict = Depends(verify_token)
) -> ApiResponse:
    product_repo.update_product(product_id, product)

    return ApiResponse(message="Product updated successfully.")

@router.delete("/products/{product_id}", response_model=ApiResponse)
async def delete_product(
    product_id: str,
    token_data: dict = Depends(verify_token)
) -> ApiResponse:
    product_repo.delete_product(product_id)

    return ApiResponse(message="Product deleted successfully.") 

@router.post("/broadcast-newsletter", response_model=ApiResponse)
async def broadcast_newsletter(
    payload: NewsLetterContentRequest,
    attachments: list[UploadFile] = File(default=[]),
    token_data: dict = Depends(verify_token)
) -> ApiResponse:
    
    subscribers = newsletter_repo.get_all_subscribers()
    cc_addrs = [subscriber.email for subscriber in subscribers]
    
    email_attachments = None
    
    if attachments.__len__() > 0:
        email_attachments = []
        for attachment in attachments:
            email_attachments.append(
                (attachment.filename, await attachment.read(), attachment.content_type or "application/octet-stream")
            )
    
    email_svc.send(
        payload.subject,
        payload.content,
        email_svc.smtp_from,
        cc_addrs,
        email_attachments
    )

    return ApiResponse(message="Newsletter broadcasted.")

@router.post("/faqs", response_model=ApiResponse)
async def upload_faqs(
    faqs: list[FAQRequest],
    token_data: dict = Depends(verify_token)
) -> ApiResponse:
    
    # Able to do batching here (But not needed as adding FAQs is not frequent or big)
    for faq in faqs:
        faq_repo.add_faq(faq.question, faq.answer)

    return ApiResponse(message="FAQs uploaded successfully.")

@router.put("/faqs/{faq_id}", response_model=ApiResponse)
async def update_faq(
    faq_id: int,
    faq: FAQRequest,
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
    contact_info: ContactInfoRequest,
    token_data: dict = Depends(verify_token)
) -> ApiResponse:
    
    contact_info_repo.add_contact_info(contact_info)

    return ApiResponse(message="Contact info uploaded successfully.")

@router.put("/contact-info/{contact_id}", response_model=ApiResponse)
async def update_contact_info(
    contact_id: int,
    contact_info: ContactInfoRequest,
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
    token_data: dict = Depends(verify_token)
) -> ApiResponse:
    
    blog_repo.add_blog(blog)

    return ApiResponse(message="Blog uploaded successfully.")

@router.put("/blogs/{blog_id}", response_model=ApiResponse)
async def update_blog(
    blog_id: int,
    blog: Blog,
    token_data: dict = Depends(verify_token)
) -> ApiResponse:
    
    blog_repo.update_blog(blog_id, blog)

    return ApiResponse(message="Blog updated successfully.")

@router.delete("/blogs/{blog_id}", response_model=ApiResponse)
async def delete_blog(
    blog_id: int,
    token_data: dict = Depends(verify_token)
) -> ApiResponse:
    
    blog_repo.delete_blog(blog_id)

    return ApiResponse(message="Blog deleted successfully.")

@router.post("/login")
async def admin_login(payload: AdminLoginRequest) -> str:
    # return jwt token 3 hour expiry (need to change how password is accessed here for sec reasons)
    if payload.username == "admin" and payload.password == "password":
        jwt_token = jwt_svc.create_jwt_token(payload.username)
        return jwt_token
    else:
        raise HTTPException(status_code=401, detail="Invalid credentials")


