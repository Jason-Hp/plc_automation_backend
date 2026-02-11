from contextvars import ContextVar
from app.enums.country import Country

lang_context: ContextVar[str] = ContextVar('lang', default='en')
country_context: ContextVar[str] = ContextVar('country', default="SG")