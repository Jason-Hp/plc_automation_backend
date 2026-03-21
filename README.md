# PLC Automation Backend API

Base URL: `http://localhost:8000/api`

## Architecture
- **Controller Layer**: API routes (`app/routes/`)
- **Service Layer**: Business logic (`app/services/`)
- **Repository Layer**: Data access (`app/repositories/`)
- **Supabase**: Primary database and authentication provider.

## Global Headers
- `lang`: (optional) Language for translation (default: `en`).
- `country`: (optional) Country code for context (default: `SG`).
- `Authorization`: `Bearer <token>` (Required for all `/admin/*` endpoints).

---

## Public Info Endpoints

### GET `/faqs`
**Response 200**
```json
[
  {
    "id": 1,
    "question": "What is a PLC?",
    "answer": "Programmable Logic Controller..."
  }
]
```

### GET `/contact-info`
**Response 200**
```json
[
  {
    "id": 1,
    "address": "123 Main St",
    "phone": "+65 1234 5678",
    "email": "contact@example.com",
    "working_hours": "9am-6pm",
    "country": "Singapore"
  }
]
```

### GET `/contact-info/{country}`
**Response 200**
Same as `/contact-info` but returns a single object.

### GET `/categories`
**Response 200**
```json
[
  { "id": 1, "name": "CPU" }
]
```

### GET `/manufacturers`
**Response 200**
```json
[
  { "id": 1, "name": "Siemens" }
]
```

### GET `/countries`
**Response 200**
```json
[
  { "id": 1, "name": "Singapore", "code": "SG" }
]
```

---

## Public Form Endpoints

### POST `/enquiry`
**Request body**
```json
{
  "name": "John Doe",
  "company_name": "Tech Corp",
  "country_code": "SG",
  "phone": "12345678",
  "email": "john@example.com",
  "message": "I need more information."
}
```

### POST `/quote`
**Content-Type**: `multipart/form-data`
**Request body**
- `payload`: JSON string matching `QuoteWithProductPreviewsWithQuantityRequest`
- `attachment`: (optional file)

`payload` schema:
```json
{
  "name": "John Doe",
  "company_name": "Tech Corp",
  "country_code": "SG",
  "phone": "12345678",
  "email": "john@example.com",
  "message": "Request for quote",
  "product_previews_with_quantity": [
    {
      "id": 1,
      "name": "S7-1200",
      "part_number": "6ES7214-1AG40-0XB0",
      "manufacturer": { "id": 1, "name": "Siemens" },
      "quantity": 5
    }
  ]
}
```

### POST `/newsletter`
**Request body**
```json
{
  "email": "subscriber@example.com"
}
```

---

## Products & Search

### GET `/products?page={page}&per_page={per_page}&search={search}`
**Response 200**
```json
{
  "product_previews": [...],
  "page": 1,
  "per_page": 30,
  "total": 100
}
```

### GET `/products/{product_id}`
**Response 200**
```json
{
  "product_with_stock": {
    "product": {
      "id": 1,
      "name": "S7-1200",
      "part_number": "6ES7214-1AG40-0XB0",
      "manufacturer": { "id": 1, "name": "Siemens" },
      "description": "Powerful PLC"
    },
    "stock": true
  }
}
```

### GET `/semantic-search?query={query}&top_k={top_k}`
**Response 200**
```json
{
  "product_previews": [...],
  "page": 1,
  "per_page": 10,
  "total": 10
}
```

---

## Blogs

### POST `/blogs/?page={page}&per_page={per_page}`
**Request body**
```json
{
  "search": "PLC",
  "categories": ["Guide", "News"]
}
```
**Response 200**
```json
{
  "page": 1,
  "per_page": 10,
  "total": 5,
  "blog_previews": [
    {
      "id": 1,
      "title": "Getting started with PLCs",
      "categories": [{ "id": 1, "name": "Guide" }],
      "image_url": "...",
      "published_by": "Admin",
      "created_at": "01-01-2025",
      "updated_at": "01-01-2025"
    }
  ]
}
```

### GET `/blogs/{blogId}`
**Response 200**
```json
{
  "id": 1,
  "title": "...",
  "categories": [...],
  "image_url": "...",
  "published_by": "...",
  "created_at": "...",
  "updated_at": "...",
  "content": "Full blog content here..."
}
```

---

## Jobs

### GET `/jobs/?page={page}&per_page={per_page}`
**Response 200**
```json
{
  "page": 1,
  "per_page": 10,
  "total": 1,
  "job_previews": [
    {
      "id": 1,
      "title": "PLC Engineer",
      "country": "SG",
      "location": "Singapore",
      "job_type": "Full-time",
      "posted_date": "01-01-2025"
    }
  ]
}
```

### GET `/jobs/{job_id}`
**Response 200**
```json
{
  "id": 1,
  "title": "PLC Engineer",
  "country": "SG",
  "location": "Singapore",
  "job_type": "Full-time",
  "posted_date": "01-01-2025",
  "industry": "Automation",
  "requirements": "...",
  "responsibilities": "...",
  "description": "...",
  "working_hours": "9am-6pm"
}
```

### POST `/jobs/{job_id}/application`
**Content-Type**: `multipart/form-data`
**Request body**
- `payload`: JSON string matching `JobApplicationRequest`
- `resume`: (required file)

`payload` schema:
```json
{
  "first_name": "John",
  "last_name": "Doe",
  "email": "john@doe.com",
  "country_code": "SG",
  "phone": "12345678",
  "experience": "5 years"
}
```

---

## Admin Endpoints (Requires Auth)

### GET `/admin/user-info`
**Response 200**
```json
{
  "uuid": "...",
  "email": "admin@example.com",
  "user_role": "admin"
}
```

### POST `/admin/account`
**Request body**
```json
{
  "email": "user@example.com",
  "password": "password123",
  "user_role": "user"
}
```

### POST `/admin/broadcast-newsletter`
**Content-Type**: `multipart/form-data`
**Request body**
- `payload`: JSON matching `NewsLetterContentRequest`
- `attachments`: (optional files)

`payload` schema:
```json
{
  "subject": "Weekly Updates",
  "content": "HTML or text content"
}
```

### POST `/admin/products`
**Request body**
```json
{
  "name": "New Product",
  "part_number": "PN-001",
  "manufacturer": "Siemens",
  "image_url": "...",
  "description": "...",
  "countries": ["Singapore", "Malaysia"]
}
```

### PUT `/admin/products/{product_id}`
Same schema as POST `/admin/products`.

### DELETE `/admin/products/{product_id}`

### GET `/admin/quotes?search={search}&page={page}&per_page={per_page}`
**Response 200**
```json
{
  "page": 1,
  "per_page": 10,
  "total": 1,
  "quote_previews": [
    {
      "name": "John Doe",
      "company_name": "Tech Corp",
      "created_at": "...",
      "is_paid": false,
      "total_amount": 1000
    }
  ]
}
```

### GET `/admin/quote/{quote_id}`
**Response 200**
Full quote data including `product_previews_with_quantity`.

### POST `/admin/blogs`
**Request body**
```json
{
  "title": "New Blog",
  "image_url": "...",
  "published_by": "Admin",
  "created_at": "01-01-2025",
  "updated_at": "01-01-2025",
  "content": "...",
  "categories": [{ "id": 1, "name": "Guide" }]
}
```

### GET `/admin/approvals?page={page}&per_page={per_page}`
**Request body** (used for filtering)
```json
{
  "id": null,
  "type": null,
  "is_approved": null
}
```
**Response 200**
```json
{
  "page": 1,
  "per_page": 10,
  "total": 1,
  "approvals": [...]
}
```

### POST `/admin/approvals`
**Content-Type**: `multipart/form-data`
- `payload`: JSON string matching `ApprovalRequest`
- `attachment`: (optional file)

---

## Logging

### GET `/admin/log/{log_type}?date={YYYY-MM-DD}`
- `log_type`: `web`, `error`, `admin`, `debug`
- Returns a log file for download or redirects to storage.
