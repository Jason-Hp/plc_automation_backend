from contextvars import ContextVar

# Context variables used to propagate language and country
# information from request headers through the application.
# Country is represented as a simple string country code (e.g. "SG").

lang_context: ContextVar[str] = ContextVar("lang", default="en")
country_context: ContextVar[str] = ContextVar("country", default="SG")