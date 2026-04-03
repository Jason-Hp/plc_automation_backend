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
from app.services.info_service import InfoService
from app.services.blog_service import BlogService
from app.services.job_service import JobService
from app.services.product_service import ProductService
from app.services.admin_newsletter_service import AdminNewsletterService
from app.services.admin_approvals_service import AdminApprovalsService
from app.services.storage_service import StorageService
from app.services.supabase_service import SupabaseService
from app.services.forms_service import FormsService

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

info_service = InfoService(
    faq_repo=faq_repo,
    contact_info_repo=contact_info_repo,
    category_repo=category_repo,
    manufacturer_repo=manufacturer_repo,
    country_repo=country_repo,
)

blog_service = BlogService(
    blog_repo=blog_repo, category_repo=category_repo, blog_category_repo=blog_category_repo
)

job_service = JobService(job_repo=job_repo, email_service=email_service)

product_service = ProductService(
    manufacturer_repo=manufacturer_repo,
    product_repo=product_repo,
    product_country_repo=product_country_repo,
    country_repo=country_repo,
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
