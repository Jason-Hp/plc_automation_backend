# PLC Automation Backend

FastAPI backend for PLC Automation public website APIs (forms, product catalog, blog/info content, and admin management APIs).

## Tech stack
- Python + FastAPI
- Pydantic models for request/response schemas
- In-memory placeholder repositories for multiple domains (to be replaced with DB-backed repositories)

## Project status
This project is still in progress.
- `BlogRepository`, `FaqRepository`, and `ContactInfoRepository` are currently in-memory placeholders.
- Admin login currently uses hardcoded credentials (`admin` / `password`) and a simple signed token implementation.
- SMTP and persistence need environment configuration for production use.

---

## Run locally

### 1) Install dependencies
```bash
pip install -r requirements.txt
```

### 2) Configure environment
Create `.env` from `.env.example` and set values (especially SMTP and emails).

### 3) Start API
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Base URL: `http://localhost:8000`

---

## Authentication

Admin endpoints (prefix `/api/admin`) require bearer token except `/api/admin/login`.

### Login request
`POST /api/admin/login`

Request JSON:
```json
{
  "username": "admin",
  "password": "password"
}
```

Response JSON:
```json
"<token>"
```

Use token:
```http
Authorization: Bearer <token>
```

---

## API documentation

All routes are mounted under `/api`.

## 1) Health

### GET `/api/health`
Response JSON:
```json
{
  "status": "ok"
}
```

---

## 2) Forms APIs

## POST `/api/enquiry`
Request JSON:
```json
{
  "name": "John Doe",
  "company_name": "ACME Industrial",
  "country_code": "65",
  "phone": "98765432",
  "email": "john@acme.com",
  "message": "Need help with PLC panel upgrades"
}
```

Response JSON:
```json
{
  "message": "Your query has been submitted successfully."
}
```

## POST `/api/quote`
> Supports optional file upload via `multipart/form-data`.

Request JSON payload (logical schema):
```json
{
  "name": "John Doe",
  "company_name": "ACME Industrial",
  "country_code": "65",
  "phone": "98765432",
  "email": "john@acme.com",
  "message": "Need quote",
  "products": [
    {
      "id": "sample-1",
      "name": "SIMATIC S7-1500 CPU",
      "part_number": "CPU-1510",
      "quantity": 1
    }
  ]
}
```

Multipart fields:
- `payload`: JSON object above
- `attachment`: file (optional)

Response JSON:
```json
{
  "message": "Your enquiry has been submitted successfully."
}
```

## POST `/api/newsletter`
Request JSON:
```json
{
  "email": "subscriber@example.com"
}
```

Response JSON:
```json
{
  "message": "Thank you for subscribing."
}
```

## POST `/api/job-application`
> `multipart/form-data`

Form fields:
- `payload` (logical JSON schema):
```json
{
  "first_name": "Jane",
  "last_name": "Doe",
  "email": "jane@example.com",
  "country_code": "65",
  "phone": "91234567",
  "experience": "5 years",
  "role": "PLC Engineer"
}
```
- `resume`: file (required)

Response JSON:
```json
{
  "message": "Application submitted successfully."
}
```

---

## 3) Product APIs

## GET `/api/products?page=1&per_page=30&category=<optional>&search=<optional>`
Response JSON:
```json
{
  "items": [
    {
      "id": "sample-1",
      "name": "SIMATIC S7-1500 CPU",
      "part_number": "CPU-1510"
    }
  ],
  "page": 1,
  "per_page": 30,
  "total": 1
}
```

## GET `/api/products/{product_id}`
Response JSON:
```json
{
  "id": "sample-1",
  "name": "SIMATIC S7-1500 CPU",
  "part_number": "CPU-1510",
  "manufacturer": "Siemens",
  "stock": true,
  "description": "Sample PLC CPU for wiring cabinets.",
  "category": null,
  "sub_category": null,
  "url": "cpu-1510",
  "available_for_countries": ["SG"]
}
```

404 JSON:
```json
{
  "detail": "Product not found"
}
```

---

## 4) Info APIs

## GET `/api/faqs`
Response JSON:
```json
[
  {
    "id": 1,
    "question": "What is PLC automation?",
    "answer": "..."
  }
]
```

## GET `/api/contact-info`
Response JSON:
```json
[
  {
    "id": 1,
    "address": "1 Example Street",
    "phone": "+65 6000 0000",
    "email": "info@example.com",
    "working_hours": "Mon-Fri 9AM-6PM",
    "country": "SG"
  }
]
```

## GET `/api/contact-info/{country}`
Response JSON:
```json
{
  "id": 1,
  "address": "1 Example Street",
  "phone": "+65 6000 0000",
  "email": "info@example.com",
  "working_hours": "Mon-Fri 9AM-6PM",
  "country": "SG"
}
```

404 JSON:
```json
{
  "detail": "Contact info not found"
}
```

---

## 5) Blog APIs

## GET `/api/blogs/?search=<optional>&category=<optional>&page=1&per_page=10`
Response JSON:
```json
{
  "page": 1,
  "per_page": 10,
  "total": 0,
  "blog_previews": []
}
```

## GET `/api/blogs/{blogId}`
Response JSON:
```json
{
  "id": 1,
  "title": "How to select a PLC",
  "category": "Guide",
  "image_url": "https://cdn.example.com/blogs/plc-guide.jpg",
  "published_by": "PLC Automation",
  "created_at": "01-01-2025",
  "updated_at": "02-01-2025",
  "content": "..."
}
```

404 JSON:
```json
{
  "detail": "Blog not found"
}
```

---

## 6) Admin APIs (Bearer token required)

## POST `/api/admin/products/batch`
> `multipart/form-data` with field `csv_file`

Response JSON:
```json
{
  "processed": 12,
  "message": "CSV processed (placeholder)."
}
```

## POST `/api/admin/products`
Request JSON:
```json
{
  "id": "sample-2",
  "name": "Relay Module",
  "part_number": "RM-100",
  "manufacturer": "BrandX",
  "stock": true,
  "description": "Industrial relay",
  "category": "Relay",
  "sub_category": "Interface",
  "url": "relay-module",
  "available_for_countries": ["SG", "MY"]
}
```

Response JSON:
```json
{
  "message": "Product uploaded successfully."
}
```

## PUT `/api/admin/products/{product_id}`
Request JSON: same as create product.

Response JSON:
```json
{
  "message": "Product updated successfully."
}
```

## DELETE `/api/admin/products/{product_id}`
Response JSON:
```json
{
  "message": "Product deleted successfully."
}
```

## POST `/api/admin/broadcast-newsletter`
Request JSON schema:
```json
{
  "subject": "Monthly updates",
  "content": "New products available"
}
```

Optional `attachments` files via multipart.

Response JSON:
```json
{
  "message": "Newsletter broadcasted."
}
```

## POST `/api/admin/faqs`
Request JSON:
```json
[
  {
    "question": "What is PLC?",
    "answer": "Programmable Logic Controller"
  }
]
```

Response JSON:
```json
{
  "message": "FAQs uploaded successfully."
}
```

## PUT `/api/admin/faqs/{faq_id}`
Request JSON:
```json
{
  "question": "Updated question",
  "answer": "Updated answer"
}
```

Response JSON:
```json
{
  "message": "FAQ updated successfully."
}
```

## DELETE `/api/admin/faqs/{faq_id}`
Response JSON:
```json
{
  "message": "FAQ deleted successfully."
}
```

## POST `/api/admin/contact-info`
Request JSON:
```json
{
  "address": "1 Example Street",
  "phone": "+65 6000 0000",
  "email": "info@example.com",
  "working_hours": "Mon-Fri 9AM-6PM",
  "country": "SG"
}
```

Response JSON:
```json
{
  "message": "Contact info uploaded successfully."
}
```

## PUT `/api/admin/contact-info/{contact_id}`
Request JSON: same as create contact info.

Response JSON:
```json
{
  "message": "Contact info updated successfully."
}
```

## DELETE `/api/admin/contact-info/{contact_id}`
Response JSON:
```json
{
  "message": "Contact info deleted successfully."
}
```

## POST `/api/admin/blogs`
Request JSON:
```json
{
  "id": 1,
  "title": "How to select a PLC",
  "category": "Guide",
  "image_url": "https://cdn.example.com/blog.jpg",
  "published_by": "PLC Automation",
  "created_at": "01-01-2025",
  "updated_at": "01-01-2025",
  "content": "Long article body"
}
```

Response JSON:
```json
{
  "message": "Blog uploaded successfully."
}
```

## PUT `/api/admin/blogs/{blog_id}`
Request JSON: same as create blog.

Response JSON:
```json
{
  "message": "Blog updated successfully."
}
```

## DELETE `/api/admin/blogs/{blog_id}`
Response JSON:
```json
{
  "message": "Blog deleted successfully."
}
```

---

## Notes
- Language and country can be passed via headers:
  - `lang` (default `en`)
  - `country` (default `SG`)
- Some endpoints trigger SMTP email sending and will error if SMTP host is not configured.
- Logging middleware writes structured logs under configured `logs/` paths.
