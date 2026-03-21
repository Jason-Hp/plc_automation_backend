from app.repositories.approval_repository import ApprovalRepository
from app.repositories.blog_repository import BlogRepository
from app.repositories.blog_category_repository import BlogCategoryRepository
from app.repositories.category_repository import CategoryRepository
from app.repositories.contact_info_repository import ContactInfoRepository
from app.repositories.country_repository import CountryRepository
from app.repositories.faq_repository import FaqRepository
from app.repositories.job_repository import JobRepository
from app.repositories.maufacturer_repository import ManufacturerRepository
from app.repositories.quote_repository import QuoteRepository
from app.repositories.newsletter_subscribers_repository import NewsletterRepository
from app.repositories.product_repository import ProductRepository
from app.repositories.product_country_repository import ProductCountryRepository
from app.repositories.quote_product_repository import QuoteProductRepository
from app.services.email_service import EmailService
from app.services.jwt_service import JwtService
from app.services.search_service import SearchService
from app.services.quotes_service import QuotesService
from app.services.admin_faq_service import AdminFaqService
from app.services.admin_blog_service import AdminBlogService
from app.services.admin_job_service import AdminJobService
from app.services.admin_catalog_service import AdminCatalogService
from app.services.admin_products_service import AdminProductsService
from app.services.admin_newsletter_service import AdminNewsletterService
from app.services.admin_approvals_service import AdminApprovalsService
from app.services.storage_service import StorageService
from app.services.supabase_service import SupabaseService
from app.services.forms_service import FormsService
from app.services.public_infos_service import PublicInfosService
from app.services.public_products_service import PublicProductsService
from app.services.public_blogs_service import PublicBlogsService
from app.services.public_jobs_service import PublicJobsService

newsletter_repo = NewsletterRepository()
approval_repo = ApprovalRepository()
faq_repo = FaqRepository()
contact_info_repo = ContactInfoRepository()
blog_repo = BlogRepository()
blog_category_repo = BlogCategoryRepository()
product_repo = ProductRepository()
product_country_repo = ProductCountryRepository()
job_repo = JobRepository()
category_repo = CategoryRepository()
manufacturer_repo = ManufacturerRepository()
country_repo = CountryRepository()
quote_repo = QuoteRepository()
quote_product_repo = QuoteProductRepository()

email_service = EmailService()
jwt_service = JwtService()
search_service = SearchService()
storage_service = StorageService()
supabase_service = SupabaseService()

quotes_service = QuotesService(quote_repo=quote_repo, quote_product_repo=quote_product_repo)

admin_faq_service = AdminFaqService(faq_repo=faq_repo)

admin_blog_service = AdminBlogService(
    blog_repo=blog_repo, category_repo=category_repo, blog_category_repo=blog_category_repo
)

admin_job_service = AdminJobService(job_repo=job_repo)

admin_catalog_service = AdminCatalogService(
    category_repo=category_repo,
    manufacturer_repo=manufacturer_repo,
    country_repo=country_repo,
    contact_info_repo=contact_info_repo,
)

admin_products_service = AdminProductsService(
    manufacturer_repo=manufacturer_repo,
    product_repo=product_repo,
    product_country_repo=product_country_repo,
)

admin_newsletter_service = AdminNewsletterService(
    newsletter_repo=newsletter_repo,
    email_service=email_service,
)

admin_approvals_service = AdminApprovalsService(
    approval_repo=approval_repo, storage_service=storage_service
)

forms_service = FormsService(
    email_service=email_service,
    newsletter_repo=newsletter_repo,
    quotes_service=quotes_service,
)

public_infos_service = PublicInfosService(
    faq_repo=faq_repo,
    contact_info_repo=contact_info_repo,
    category_repo=category_repo,
    manufacturer_repo=manufacturer_repo,
    country_repo=country_repo,
)

public_products_service = PublicProductsService(
    product_repo=product_repo,
    country_repo=country_repo,
    product_country_repo=product_country_repo,
)

public_blogs_service = PublicBlogsService(
    blog_repo=blog_repo, blog_category_repo=blog_category_repo
)

public_jobs_service = PublicJobsService(
    job_repo=job_repo,
    email_service=email_service,
)
