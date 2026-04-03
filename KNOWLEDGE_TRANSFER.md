# Knowledge Transfer Document: PLC Automation Backend

This document provides a comprehensive overview of the PLC Automation Backend project, its architecture, setup instructions, and core functionalities to facilitate a smooth knowledge transfer.

## **Table of Contents**
1. [Project Overview](#project-overview)
2. [Tech Stack](#tech-stack)
3. [Project Structure](#project-structure)
4. [Setup & Installation](#setup--installation)
5. [Running the Application](#running-the-application)
6. [Core Architecture & Logic](#core-architecture--logic)
    - [Request Flow](#request-flow)
    - [Authentication & Authorization](#authentication--authorization)
    - [Database & Supabase](#database--supabase)
    - [Logging System](#logging-system)
    - [Translation System](#translation-system)
    - [Semantic Search](#semantic-search)
7. [Key Modules](#key-modules)
8. [Maintenance & Best Practices](#maintenance--best-practices)

---

## **Project Overview**
The PLC Automation Backend is a FastAPI-based RESTful API designed to manage industrial automation product catalogs, blog posts, job listings, and user inquiries. It serves as the backbone for the PLC Automation web platform, providing both public and administrative endpoints.

---

## **Tech Stack**
- **Language**: Python 3.10+ (Current environment suggests Python 3.14 compatible)
- **Framework**: [FastAPI](https://fastapi.tiangolo.com/)
- **Database**: [Supabase](https://supabase.com/) (PostgreSQL)
- **Authentication**: Supabase Auth (JWT)
- **Storage**: AWS S3 (optional) or Local File System
- **Search**: OpenAI Embeddings for Semantic Search
- **Translation**: `deep-translator` (Google Translate API)
- **Scheduler**: `APScheduler` (for log management)
- **Email**: `aiosmtplib` (SMTP)

---

## **Project Structure**
The project follows a layered architecture (Controller -> Service -> Repository) to ensure separation of concerns.

```text
plc_automation_backend/
├── app/
│   ├── main.py             # Entry point of the FastAPI application
│   ├── config.py           # Configuration management (Pydantic Settings)
│   ├── dependencies.py     # FastAPI dependency injection
│   ├── middlewares/        # Custom middlewares (Logging, Context)
│   ├── models/             # Data models (API request/response, DB, Domain)
│   ├── repositories/       # Data access layer (Supabase interaction)
│   ├── routes/             # API route definitions (Controllers)
│   ├── services/           # Business logic layer
│   ├── scheduler/          # Background tasks (Log rotation)
│   ├── utils/              # Utility functions (Translation, Formatting)
│   └── logs/               # Local log storage
├── .env.example            # Template for environment variables
├── requirements.txt        # Project dependencies
└── README.md               # Quick start and API overview
```

---

## **Setup & Installation**

### **Prerequisites**
- Python 3.10 or higher.
- A Supabase project.
- (Optional) OpenAI API Key for semantic search.
- (Optional) AWS Account for S3 storage.

### **Step-by-Step Setup**

1.  **Clone the Repository**:
    ```bash
    git clone <repository-url>
    cd plc_automation_backend
    ```

2.  **Create a Virtual Environment**:
    ```bash
    python -m venv venv
    # Windows
    .\venv\Scripts\activate
    # macOS/Linux
    source venv/bin/activate
    ```

3.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

4.  **Configure Environment Variables**:
    - Copy `.env.example` to `.env`.
    - Fill in the required values:
        - `SUPABASE_URL` and `SUPABASE_KEY` (Found in Supabase Project Settings > API).
        - `DATABASE_URL` (Optional, if using direct DB access).
        - `OPENAI_API_KEY` (Required for semantic search).
        - SMTP settings for email notifications.

---

## **Running the Application**

### **Local Development**
Run the server using `uvicorn` with auto-reload:
```bash
uvicorn app.main:app --reload --port 8000
```
- **API Docs**: Access Swagger UI at `http://localhost:8000/docs`.
- **Health Check**: `GET /api/health`.

### **Production**
In production, use a process manager like Gunicorn with Uvicorn workers:
```bash
gunicorn -w 4 -k uvicorn.workers.UvicornWorker app.main:app
```

---

## **Core Architecture & Logic**

### **Request Flow**
1.  **Middleware**: [ContextMiddleware](file:///c%3A/Users/pollo/Desktop/plc_automation_backend/app/middlewares/context_middleware.py) extracts headers like `lang` and `country` and stores them in a context variable.
2.  **Routes**: [routes/](file:///c%3A/Users/pollo/Desktop/plc_automation_backend/app/routes/) handles incoming requests and validates input models.
3.  **Services**: [services/](file:///c%3A/Users/pollo/Desktop/plc_automation_backend/app/services/) contains unified business logic for both public and administrative operations.
4.  **Repositories**: [repositories/](file:///c%3A/Users/pollo/Desktop/plc_automation_backend/app/repositories/) interacts with Supabase using the [supabase-py](https://github.com/supabase-community/supabase-py) client.

### **Authentication & Authorization**
- **Admin Routes**: Protected by JWT verification. Admin endpoints reside under `/api/admin`.
- **User Roles**: Roles are stored in Supabase's `app_metadata` (e.g., `user_role: admin`).

### **Database & Supabase**
- The project uses [supabase_client_util.py](file:///c%3A/Users/pollo/Desktop/plc_automation_backend/app/utils/supabase_client_util.py) to initialize a singleton client.
- Repositories like [product_repository.py](file:///c%3A/Users/pollo/Desktop/plc_automation_backend/app/repositories/product_repository.py) perform CRUD operations via the client.

### **Logging System**
- **LoggingMiddleware**: Logs all incoming requests and responses.
- **LogService**: Provides structured logging (WEB, ERROR, ADMIN, DEBUG).
- **LogScheduler**: A background task in [log_scheduler.py](file:///c%3A/Users/pollo/Desktop/plc_automation_backend/app/scheduler/log_scheduler.py) rotates and archives logs periodically.

### **Translation System**
- Automatically translates content based on the `lang` header.
- Uses [translation_util.py](file:///c%3A/Users/pollo/Desktop/plc_automation_backend/app/utils/translation_util.py) which leverages `GoogleTranslator` with a fallback to English.

### **Semantic Search**
- Implemented in [search_service.py](file:///c%3A/Users/pollo/Desktop/plc_automation_backend/app/services/search_service.py).
- Uses OpenAI embeddings to convert product descriptions into vectors for high-relevance search results.

---

## **Key Modules**
- **Products**: Management of product catalogs, manufacturers, and country-specific availability.
- **Blogs**: Categorized blog posts with localization support.
- **Jobs**: Career listings and application management.
- **Forms**: Handles user inquiries, quotes, and newsletter subscriptions.
- **Admin**: A comprehensive set of endpoints for data management and user administration.

---

## **Maintenance & Best Practices**
- **Adding a New Feature**: 
    1. Define models in `app/models/`.
    2. Create a repository in `app/repositories/`.
    3. Implement business logic in `app/services/`.
    4. Expose via a router in `app/routes/`.
- **Environment Changes**: Always update `.env.example` when adding new configuration keys.
- **Error Handling**: Use the `LogService` to capture exceptions and provide meaningful API responses.

---

*This document is intended for onboarding and internal use. For further clarification, refer to the inline comments in the source code.*
