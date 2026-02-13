from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.middlewares.logging_middleware import LoggingMiddleware
from app.middlewares.context_middleware import ContextMiddleware
from app.config import settings
from app.routes import admin, forms, infos, products, blogs, search, job

app = FastAPI(title=settings.app_name)

origins = [origin.strip() for origin in settings.allowed_origins.split(",") if origin.strip()]

app.add_middleware(
    ContextMiddleware
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins or ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(
    LoggingMiddleware
)

app.include_router(forms.router, prefix="/api")
app.include_router(products.router, prefix="/api")
app.include_router(admin.router, prefix="/api")
app.include_router(infos.router, prefix="/api")
app.include_router(blogs.router, prefix="/api")
app.include_router(search.router, prefix="/api")
app.include_router(job.router, prefix="/api")

@app.get("/api/health")
async def health_check() -> dict[str, str]:
    return {"status": "ok"}
