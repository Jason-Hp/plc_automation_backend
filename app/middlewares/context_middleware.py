from contextvars import ContextVar
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from app.utils.context_util import lang_context, country_context

class ContextMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):

        lang = request.headers.get("lang", "en")

        lang_context.set(lang)

        country = request.headers.get("country", "SG")

        country_context.set(country)
        
        response = await call_next(request)

        # Context auto-cleaned after response
        return response