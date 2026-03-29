from __future__ import annotations

import csv
import datetime
import io
import json
import pytz
from pathlib import Path
from typing import Optional

from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile, status, Query
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.responses import FileResponse, RedirectResponse


from app.models.db.data_models import (
    Blog as BlogDb,
    Category as CategoryDb,
    ContactInfo as ContactInfoDb,
    Country as CountryDb,
    FAQ as FAQDb,
    Job as JobDb,
    Manufacturer as ManufacturerDb,
)
from app.models.api.response_models import (
    ApiResponse,
    ApprovalPreviewListResponse,
    BatchProductUploadResultResponse,
    QuotePreviewListResponse,
    QuotePreviewResponse,
    QuoteWithProductPreviewsWithQuantityResponse,
    QuoteWithProductPreviewsWithQuantityDataResponse,
    UserInfoResponse,
    ProductPreviewWithQuantityResponse,
    ManufacturerResponse,
)
from app.models.api.request_models import (
    AccountCreationRequest,
    ApprovalRequest,
    BlogWithCategoriesRequest,
    CategoryRequest,
    ContactInfoRequest,
    CountryRequest,
    FAQRequest,
    JobUploadRequest,
    ManufacturerRequest,
    NewsLetterContentRequest,
    ProductWithCountriesRequest,
    QuoteWithProductPreviewsWithQuantityRequest,
)
from app.config import settings
from app.services.log_service import LogService
from app.dependencies import (
    admin_blog_service,
    admin_catalog_service,
    admin_products_service,
    admin_newsletter_service,
    admin_approvals_service,
    admin_faq_service,
    admin_job_service,
    jwt_service,
    quotes_service,
    storage_service,
    supabase_service
)
from app.services.jwt_service import JwtTokenError
from app.utils.user_role import UserRole

router = APIRouter(prefix="/admin", tags=["admin"])
security = HTTPBearer()
timezone = pytz.timezone(settings.timezone)

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

def get_user_role(token_data: dict) -> UserRole:
    user_role = token_data.get("app_metadata", {}).get("user_role")
    try:
        return UserRole(user_role)
    except ValueError:
        raise HTTPException(status_code=403, detail="Invalid user role.")
    
def is_admin(token_data: dict) -> bool:
    if get_user_role(token_data) == UserRole.ADMIN:
        return True
    raise HTTPException(status_code=403, detail="Admin privileges required.")
    
@router.get("/user-info", response_model=UserInfoResponse)
async def get_user_info(token_data: dict = Depends(verify_token)) -> UserInfoResponse:
    user_role = get_user_role(token_data)
    uuid = token_data.get("sub")
    email = token_data.get("email")
    return UserInfoResponse(uuid=uuid, email=email, user_role=user_role.value)

@router.post("/account", response_model=ApiResponse)
async def create_account(accountCreationRequest: AccountCreationRequest, token_data: dict = Depends(verify_token)) -> ApiResponse:
    is_admin(token_data)
    
    new_user_email = accountCreationRequest.email
    new_user_password = accountCreationRequest.password
    try:
        new_user_role = UserRole(accountCreationRequest.user_role).value 
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid user role. Must be 'admin' or 'user'.")
    
    try:
        supabase_service.create_user(new_user_email, new_user_password, new_user_role)
        LogService.ADMIN.log(
            json.dumps(
                {
                    "event": "ADMIN_ACCOUNT_CREATED",
                    "actor": token_data.get("email"),
                    "created_user_email": new_user_email,
                    "created_user_role": new_user_role,
                }
            )
        )
        return ApiResponse(message="Account created successfully.")
    except Exception as exc:
        LogService.ADMIN.log(
            json.dumps(
                {
                    "event": "ADMIN_ACCOUNT_CREATE_FAILED",
                    "actor": token_data.get("email"),
                    "created_user_email": new_user_email,
                    "created_user_role": new_user_role,
                    "error": str(exc),
                    "error_type": type(exc).__name__,
                }
            ),
            level="WARNING",
        )
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    


# TODO: refactor
# This is a batch upload and/or update using CSV
# WARNING THIS ENDPOINT IS NOT COMPLETED AND IS NOT TO BE USED
@router.post("/products/batch", response_model=BatchProductUploadResultResponse)
async def upload_offer_products(
    csv_file: UploadFile = File(...),
    token_data: dict = Depends(verify_token)
) -> BatchProductUploadResultResponse:
    is_admin(token_data)

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

    LogService.ADMIN.log(
        json.dumps(
            {
                "event": "ADMIN_PRODUCTS_BATCH_CSV_PROCESSED",
                "actor": token_data.get("email"),
                "filename": csv_file.filename,
                "processed": processed,
            }
        )
    )
    return BatchProductUploadResultResponse(processed=processed, message="CSV processed (placeholder).")

@router.post("/products", response_model=ApiResponse)
async def upload_product(
    request: ProductWithCountriesRequest,
    token_data: dict = Depends(verify_token)
) -> ApiResponse:
    is_admin(token_data)
    return admin_products_service.add_product(request=request)

@router.put("/products/{product_id}", response_model=ApiResponse)
async def update_product(
    product_id: int,
    request: ProductWithCountriesRequest,
    token_data: dict = Depends(verify_token)
) -> ApiResponse:
    is_admin(token_data)
    return admin_products_service.update_product(
        product_id=product_id, request=request
    )


@router.delete("/products/{product_id}", response_model=ApiResponse)
async def delete_product(
    product_id: int,
    token_data: dict = Depends(verify_token)
) -> ApiResponse:
    is_admin(token_data)
    return admin_products_service.delete_product(product_id=product_id)

@router.post("/broadcast-newsletter", response_model=ApiResponse)
async def broadcast_newsletter(
    payload: str = Form(...),
    attachments: list[UploadFile] = File(default=[]),
    token_data: dict = Depends(verify_token)
) -> ApiResponse:
    is_admin(token_data)
    actor_email = token_data.get("email")
    parsed_payload = NewsLetterContentRequest.model_validate(json.loads(payload))
    return await admin_newsletter_service.broadcast_newsletter(
        payload=parsed_payload,
        attachments=attachments,
        actor_email=actor_email,
    )

@router.post("/faqs", response_model=ApiResponse)
async def upload_faqs(
    faqs: list[FAQRequest],
    token_data: dict = Depends(verify_token)
) -> ApiResponse:
    is_admin(token_data)
    db_faqs = [FAQDb.model_validate(f.model_dump()) for f in faqs]
    admin_faq_service.upload_faqs(db_faqs)
    return ApiResponse(message="FAQs uploaded successfully.")

@router.put("/faqs/{faq_id}", response_model=ApiResponse)
async def update_faq(
    faq_id: int,
    faq: FAQRequest,
    token_data: dict = Depends(verify_token)
) -> ApiResponse:
    is_admin(token_data)
    admin_faq_service.update_faq(faq_id, question=faq.question, answer=faq.answer)
    return ApiResponse(message="FAQ updated successfully.")

@router.delete("/faqs/{faq_id}", response_model=ApiResponse)
async def delete_faq(
    faq_id: int,
    token_data: dict = Depends(verify_token)
) -> ApiResponse:
    is_admin(token_data)
    admin_faq_service.delete_faq(faq_id)
    return ApiResponse(message="FAQ deleted successfully.")

@router.post("/contact-info", response_model=ApiResponse)
async def upload_contact_info(
    contact_info: ContactInfoRequest,
    token_data: dict = Depends(verify_token)
) -> ApiResponse:
    is_admin(token_data)
    admin_catalog_service.add_contact_info(ContactInfoDb.model_validate(contact_info.model_dump()))
    return ApiResponse(message="Contact info uploaded successfully.")

@router.put("/contact-info/{contact_id}", response_model=ApiResponse)
async def update_contact_info(
    contact_id: int,
    contact_info: ContactInfoRequest,
    token_data: dict = Depends(verify_token)
) -> ApiResponse:
    is_admin(token_data)
    admin_catalog_service.update_contact_info(
        contact_id=contact_id, contact_info=ContactInfoDb.model_validate(contact_info.model_dump())
    )
    return ApiResponse(message="Contact info updated successfully.")

@router.delete("/contact-info/{contact_id}", response_model=ApiResponse)
async def delete_contact_info(
    contact_id: int,
    token_data: dict = Depends(verify_token)
) -> ApiResponse:
    is_admin(token_data)
    admin_catalog_service.delete_contact_info(contact_id)
    return ApiResponse(message="Contact info deleted successfully.")

@router.post("/blogs", response_model=ApiResponse)
async def upload_blog(
    request: BlogWithCategoriesRequest,
    token_data: dict = Depends(verify_token)
) -> ApiResponse:
    is_admin(token_data)
    db_blog = BlogDb.model_validate(request.model_dump(exclude={"categories"}))
    db_categories = [
        CategoryDb.model_validate(category.model_dump())
        for category in request.categories
    ]
    admin_blog_service.upload_blog(db_blog, db_categories)
    return ApiResponse(message="Blog uploaded successfully.")

@router.put("/blogs/{blog_id}", response_model=ApiResponse)
async def update_blog(
    blog_id: int,
    request: BlogWithCategoriesRequest,
    token_data: dict = Depends(verify_token)
) -> ApiResponse:
    is_admin(token_data)
    db_blog = BlogDb.model_validate(request.model_dump(exclude={"categories"}))
    db_categories = [
        CategoryDb.model_validate(category.model_dump())
        for category in request.categories
    ]
    admin_blog_service.update_blog(blog_id, db_blog, db_categories)
    return ApiResponse(message="Blog updated successfully.")

@router.delete("/blogs/{blog_id}", response_model=ApiResponse)
async def delete_blog(
    blog_id: int,
    token_data: dict = Depends(verify_token)
) -> ApiResponse:
    is_admin(token_data)
    admin_blog_service.delete_blog(blog_id)
    return ApiResponse(message="Blog deleted successfully.")

@router.post("/jobs", response_model=ApiResponse)
async def upload_job(
    job: JobUploadRequest,
    token_data: dict = Depends(verify_token)
) -> ApiResponse:
    is_admin(token_data)
    admin_job_service.upload_job(JobDb.model_validate(job.model_dump()))
    return ApiResponse(message="Job uploaded successfully.")

@router.put("/jobs/{job_id}", response_model=ApiResponse)
async def update_job(
    job_id: int,
    job: JobUploadRequest,
    token_data: dict = Depends(verify_token)
) -> ApiResponse:
    is_admin(token_data)
    admin_job_service.update_job(
        job_id=job_id, job=JobDb.model_validate(job.model_dump())
    )
    return ApiResponse(message="Job updated successfully.")

@router.delete("/jobs/{job_id}", response_model=ApiResponse)
async def delete_job(
    job_id: int,
    token_data: dict = Depends(verify_token)
) -> ApiResponse:
    is_admin(token_data)
    admin_job_service.delete_job(job_id)
    return ApiResponse(message="Job deleted successfully.")

@router.post("/categories", response_model=ApiResponse)
async def upload_category(
    category: CategoryRequest,
    token_data: dict = Depends(verify_token)
) -> ApiResponse:
    is_admin(token_data)
    admin_catalog_service.add_category(CategoryDb.model_validate(category.model_dump()))
    return ApiResponse(message="Category uploaded successfully.")

@router.put("/categories/{category_id}", response_model=ApiResponse)
async def update_category(
    category_id: int,
    category: CategoryRequest,
    token_data: dict = Depends(verify_token)
) -> ApiResponse:
    is_admin(token_data)
    admin_catalog_service.update_category(
        category_id=category_id, category=CategoryDb.model_validate(category.model_dump())
    )
    return ApiResponse(message="Category updated successfully.")

@router.delete("/categories/{category_id}", response_model=ApiResponse)
async def delete_category(  
    category_id: int,
    token_data: dict = Depends(verify_token)
) -> ApiResponse:
    is_admin(token_data)
    admin_catalog_service.delete_category(category_id)
    return ApiResponse(message="Category deleted successfully.")

@router.post("/manufacturers", response_model=ApiResponse)
async def upload_manufacturer(
    manufacturer: ManufacturerRequest,
    token_data: dict = Depends(verify_token)
) -> ApiResponse:
    is_admin(token_data)
    admin_catalog_service.add_manufacturer(
        ManufacturerDb.model_validate(manufacturer.model_dump())
    )
    return ApiResponse(message="Manufacturer uploaded successfully.")

@router.put("/manufacturers/{manufacturer_id}", response_model=ApiResponse)
async def update_manufacturer(
    manufacturer_id: int,
    manufacturer: ManufacturerRequest,
    token_data: dict = Depends(verify_token)
) -> ApiResponse:
    is_admin(token_data)
    admin_catalog_service.update_manufacturer(
        manufacturer_id=manufacturer_id,
        manufacturer=ManufacturerDb.model_validate(manufacturer.model_dump()),
    )
    return ApiResponse(message="Manufacturer updated successfully.")

@router.delete("/manufacturers/{manufacturer_id}", response_model=ApiResponse)
async def delete_manufacturer(  
    manufacturer_id: int,
    token_data: dict = Depends(verify_token)
) -> ApiResponse:
    is_admin(token_data)
    admin_catalog_service.delete_manufacturer(manufacturer_id)
    return ApiResponse(message="Manufacturer deleted successfully.")

@router.post("/countries", response_model=ApiResponse)
async def upload_country(
    country: CountryRequest,
    token_data: dict = Depends(verify_token)
) -> ApiResponse:
    is_admin(token_data)
    admin_catalog_service.add_country(
        CountryDb.model_validate(country.model_dump())
    )
    return ApiResponse(message="Country uploaded successfully.")

@router.put("/countries/{country_id}", response_model=ApiResponse)
async def update_country(
    country_id: int,
    country: CountryRequest,
    token_data: dict = Depends(verify_token)
) -> ApiResponse:
    is_admin(token_data)
    admin_catalog_service.update_country(
        country_id=country_id,
        country=CountryDb.model_validate(country.model_dump()),
    )
    return ApiResponse(message="Country updated successfully.")

@router.delete("/countries/{country_id}", response_model=ApiResponse)
async def delete_country(  
    country_id: int,
    token_data: dict = Depends(verify_token)
) -> ApiResponse:
    is_admin(token_data)
    admin_catalog_service.delete_country(country_id)
    return ApiResponse(message="Country deleted successfully.")


@router.get("/quotes", response_model=QuotePreviewListResponse)
async def get_all_quotes(
    token_data: dict = Depends(verify_token),
    search: Optional[str] = "",
    page: int = Query(1, ge=1),
    per_page: int = Query(10, ge=1, le=100)
) -> QuotePreviewListResponse:
    quotes, total = quotes_service.list_quotes(
        search=search, page=page, per_page=per_page
    )
    quote_previews = [
        QuotePreviewResponse(
            name=q.name,
            company_name=q.company_name,
            created_at=q.created_at,
            is_paid=q.is_paid,
            total_amount=q.total_amount,
        )
        for q in quotes
    ]
    return QuotePreviewListResponse(
        page=page, per_page=per_page, total=total, quote_previews=quote_previews
    )

@router.get("/quote/{quote_id}", response_model=QuoteWithProductPreviewsWithQuantityResponse)
async def get_quote_by_id(
    quote_id: int,
    token_data: dict = Depends(verify_token)
) -> QuoteWithProductPreviewsWithQuantityResponse:
    
    try:
        domain = quotes_service.get_quote_with_products(quote_id=quote_id)
        product_previews = [
            ProductPreviewWithQuantityResponse(
                id=p.id,
                name=p.name,
                part_number=p.part_number,
                manufacturer=ManufacturerResponse(
                    id=p.manufacturer.id,
                    name=p.manufacturer.name,
                ),
                image_url=p.image_url,
                quantity=p.quantity,
            )
            for p in domain.product_previews_with_quantity
        ]

        dto = QuoteWithProductPreviewsWithQuantityDataResponse(
            name=domain.name,
            company_name=domain.company_name,
            country_code=domain.country_code,
            phone=domain.phone,
            email=domain.email,
            message=domain.message,
            created_at=domain.created_at,
            id=domain.id,
            is_paid=domain.is_paid,
            total_amount=domain.total_amount,
            product_previews_with_quantity=product_previews,
        )

        return QuoteWithProductPreviewsWithQuantityResponse(
            quote_with_product_previews_with_quantity=dto
        )
        
    except KeyError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc

@router.post("/quotes", response_model=ApiResponse)
async def add_quote(
    request: QuoteWithProductPreviewsWithQuantityRequest,
    token_data: dict = Depends(verify_token)
) -> ApiResponse:
    is_admin(token_data)
    quotes_service.create_quote(request=request)
    return ApiResponse(message="Quote added successfully.")

@router.put("/quote/{quote_id}", response_model=ApiResponse)
async def update_quote(
    quote_id: int,
    request: QuoteWithProductPreviewsWithQuantityRequest,
    token_data: dict = Depends(verify_token)
) -> ApiResponse:
    is_admin(token_data)
    quotes_service.update_quote(quote_id=quote_id, request=request)
    return ApiResponse(message="Quote updated successfully.")

@router.delete("/quote/{quote_id}", response_model=ApiResponse)
async def delete_quote(
    quote_id: int,
    token_data: dict = Depends(verify_token)
) -> ApiResponse:
    is_admin(token_data)
    quotes_service.delete_quote(quote_id=quote_id)
    return ApiResponse(message="Quote deleted successfully.")

# This is a download
# log_type can be web, error, admin, debug
@router.get("/log/{log_type}")
async def get_admin_logs(log_type: str, 
                         date: str = Query(None, description="Date in YYYY-MM-DD format. If not provided, defaults to today's logs."), 
                         token_data: dict = Depends(verify_token)):
    is_admin(token_data)
    if not date:
        date = datetime.datetime.now(timezone).strftime("%Y-%m-%d")
    
    log_enum = LogService.get_log_enum(log_type)

    # For logs today, we can return the file directly from the local disk (which is being written to in real-time),
    # for past logs we can fetch from S3.
    if date == datetime.datetime.now(timezone).strftime("%Y-%m-%d"):

        log_file_path = Path(log_enum.location) / f"{log_enum.prefix}_{date}.log"
        
        if not log_file_path.exists():
            raise HTTPException(status_code=404, detail=f"Log file for {date} not found.")
        
        return FileResponse(
            path=log_file_path,
            filename=f"{log_enum.prefix}_{date}.log",
            media_type="text/plain"
        )
    # Get from S3 for past logs
    else:
        try:
            key = f"{log_enum.prefix}_{date}.log"
            log_content_url = storage_service.get_object_url(settings.aws_s3_log_bucket, key)

            # Force download by adding response-content-disposition parameter
            download_url = f"{log_content_url}&response-content-disposition=attachment%3B%20filename%3D{log_enum.prefix}_{date}.log"

            return RedirectResponse(url=download_url, status_code=302)

        except Exception as exc:
            raise HTTPException(status_code=404, detail=f"Log file for {date} not found.") from exc


@router.get("/approvals", response_model=ApprovalPreviewListResponse)
async def get_all_approvals(
    approval_id: Optional[int] = Query(None, ge=1),
    approval_type: Optional[str] = Query(None),
    is_approved: Optional[bool] = Query(None),
    token_data: dict = Depends(verify_token),
    page: int = Query(1, ge=1),
    per_page: int = Query(10, ge=1, le=100)
) -> ApprovalPreviewListResponse:
    user_role = get_user_role(token_data)
    requester_email = token_data.get("email") if user_role != UserRole.ADMIN else None
    return admin_approvals_service.list_approvals(
        requester_email=requester_email,
        approval_id=approval_id,
        approval_type=approval_type,
        is_approved=is_approved,
        page=page,
        per_page=per_page,
    )

@router.post("/approvals", response_model=ApiResponse)
async def add_approval(
    payload: str = Form(...),
    attachment: Optional[UploadFile] = File(None),
    token_data: dict = Depends(verify_token)
) -> ApiResponse:
    email = token_data.get("email")
    parsed_payload = ApprovalRequest.model_validate(json.loads(payload))
    return await admin_approvals_service.add_approval(
        approval=parsed_payload,
        attachment=attachment,
        requester_email=email,
        timezone=timezone,
    )

@router.delete("/approvals/{approval_id}", response_model=ApiResponse)
async def delete_approval(
    approval_id: int,
    token_data: dict = Depends(verify_token)
) -> ApiResponse:
    email = token_data.get("email")
    return admin_approvals_service.delete_approval(
        approval_id=approval_id, deleter_email=email
    )

@router.put("/approvals/{approval_id}/approve", response_model=ApiResponse)
async def approve_approval(
    approval_id: int,
    token_data: dict = Depends(verify_token)
) -> ApiResponse:
    is_admin(token_data)
    email = token_data.get("email")
    return admin_approvals_service.approve_approval(
        approval_id=approval_id, approver_email=email
    )

@router.put("/approvals/{approval_id}/reject", response_model=ApiResponse)
async def reject_approval(
    approval_id: int,
    token_data: dict = Depends(verify_token)
) -> ApiResponse:
    is_admin(token_data)
    email = token_data.get("email")
    return admin_approvals_service.reject_approval(
        approval_id=approval_id, rejector_email=email
    )
    
