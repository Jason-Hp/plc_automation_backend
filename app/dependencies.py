from app.repositories.approval_repository import ApprovalRepository
from app.repositories.blog_repository import BlogRepository
from app.repositories.category_repository import CategoryRepository
from app.repositories.contact_info_repository import ContactInfoRepository
from app.repositories.country_repository import CountryRepository
from app.repositories.faq_repository import FaqRepository
from app.repositories.job_repository import JobRepository
from app.repositories.maufacturer_repository import ManufacturerRepository
from app.repositories.quote_repository import QuoteRepository
from app.repositories.newsletter_subscribers_repository import NewsletterRepository
from app.repositories.product_repository import ProductRepository
from app.services.email_service import EmailService
from app.services.jwt_service import JwtService
from app.services.search_service import SearchService
from app.services.storage_service import StorageService

newsletter_repo = NewsletterRepository()
approval_repo = ApprovalRepository()
faq_repo = FaqRepository()
contact_info_repo = ContactInfoRepository()
blog_repo = BlogRepository()
product_repo = ProductRepository()
job_repo = JobRepository()
category_repo = CategoryRepository()
manufacturer_repo = ManufacturerRepository()
country_repo = CountryRepository()
quote_repo = QuoteRepository()

email_service = EmailService()
jwt_service = JwtService()
search_service = SearchService()
storage_service = StorageService()
