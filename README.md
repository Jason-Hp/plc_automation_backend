# PLC Automation Backend API

Base URL: `http://localhost:8000/api`

## Architecture
- **Controller Layer**: API routes (`app/routes/`)
- **Service Layer**: Business logic (`app/services/`)
- **Repository Layer**: Data access (`app/repositories/`)
- **Supabase**: Primary database and authentication provider.

## Global Headers (MUST INCLUDE IN EVERY CALL)
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
    "answer": "Programmable Logic Controller is an industrial computer control system..."
  }
]
```

### GET `/contact-info`
**Response 200**
```json
[
  {
    "id": 1,
    "address": "123 Main St, Singapore 123456",
    "phone": "+65 1234 5678",
    "email": "contact@plc-automation.com",
    "working_hours": "Mon-Fri: 9am-6pm",
    "country": "SG"
  }
]
```

### GET `/contact-info/{country}`
**Response 200**
```json
{
  "id": 1,
  "address": "123 Main St, Singapore 123456",
  "phone": "+65 1234 5678",
  "email": "contact@plc-automation.com",
  "working_hours": "Mon-Fri: 9am-6pm",
  "country": "SG"
}
```

### GET `/categories`
**Response 200**
```json
[
  { "id": 1, "name": "CPU" },
  { "id": 2, "name": "I/O Modules" }
]
```

### GET `/manufacturers`
**Response 200**
```json
[
  { "id": 1, "name": "Siemens" },
  { "id": 2, "name": "Allen-Bradley" }
]
```

### GET `/countries`
**Response 200**
```json
[
  { "id": 1, "name": "SG", "code": "+65" },
  { "id": 2, "name": "MY", "code": "+66" }
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
  "message": "I need more information about the S7-1200 series."
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
      "image_url": "https://example.com/s7-1200.jpg",
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
  "product_previews": [
    {
      "id": 1,
      "name": "S7-1200",
      "part_number": "6ES7214-1AG40-0XB0",
      "manufacturer": { "id": 1, "name": "Siemens" },
      "image_url": "https://example.com/s7-1200.jpg"
    }
  ],
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
      "image_url": "https://example.com/s7-1200.jpg",
      "description": "Compact and powerful PLC for industrial automation tasks."
    },
    "stock": true
  }
}
```

### GET `/semantic-search?query={query}&top_k={top_k}`
**Response 200**
```json
{
  "product_previews": [
    {
      "id": 1,
      "name": "S7-1200",
      "part_number": "6ES7214-1AG40-0XB0",
      "manufacturer": { "id": 1, "name": "Siemens" },
      "image_url": "https://example.com/s7-1200.jpg"
    }
  ],
  "page": 1,
  "per_page": 10,
  "total": 1
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
      "image_url": "https://example.com/blog.jpg",
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
  "title": "Getting started with PLCs",
  "categories": [
    { "id": 1, "name": "Guide" }
  ],
  "image_url": "https://example.com/blog.jpg",
  "published_by": "Admin",
  "created_at": "01-01-2025",
  "updated_at": "01-01-2025",
  "content": "<h1>Introduction</h1><p>Full blog content here...</p>"
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
  "requirements": "Degree in Engineering, 3 years experience in PLC programming.",
  "responsibilities": "Programming PLCs, site commissioning, and technical support.",
  "description": "Join our team as a PLC Engineer to work on exciting industrial projects.",
  "working_hours": "Mon-Fri: 9am-6pm"
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
  "experience": "5 years in industrial automation"
}
```

---

## Admin Endpoints (Requires Auth)

### GET `/admin/user-info`
**Response 200**
```json
{
  "uuid": "550e8400-e29b-41d4-a716-446655440000",
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
- `attachments`: (optional list of files)

`payload` schema:
```json
{
  "subject": "Weekly Updates",
  "content": "<h1>Our Latest Products</h1><p>Check out our new catalog...</p>"
}
```

### POST `/admin/products`
**Request body**
```json
{
  "name": "New Product",
  "part_number": "PN-001",
  "manufacturer": "Siemens",
  "image_url": "https://example.com/product.jpg",
  "description": "High performance PLC module for large scale systems.",
  "countries": ["SG", "MY"]
}
```

### PUT `/admin/products/{product_id}`
Same schema as POST `/admin/products`.

### DELETE `/admin/products/{product_id}`

### POST `/admin/products/batch`
**Content-Type**: `multipart/form-data`
**Request body**
- `csv_file`: (required file)

### POST `/admin/faqs`
**Request body**
```json
[
  {
    "question": "New FAQ Question?",
    "answer": "New FAQ Answer."
  }
]
```

### PUT `/admin/faqs/{faq_id}`
**Request body**
```json
{
  "question": "Updated Question?",
  "answer": "Updated Answer."
}
```

### DELETE `/admin/faqs/{faq_id}`

### POST `/admin/contact-info`
**Request body**
```json
{
  "address": "123 New St",
  "phone": "+65 0000 0000",
  "email": "new@example.com",
  "working_hours": "9am-5pm",
  "country": "SG"
}
```

### PUT `/admin/contact-info/{contact_id}`
Same schema as POST `/admin/contact-info`.

### DELETE `/admin/contact-info/{contact_id}`

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
      "created_at": "01-03-2025",
      "is_paid": false,
      "total_amount": 1000
    }
  ]
}
```

### GET `/admin/quote/{quote_id}`
**Response 200**
```json
{
  "quote_with_product_previews_with_quantity": {
    "name": "John Doe",
    "company_name": "Tech Corp",
    "country_code": "SG",
    "phone": "12345678",
    "email": "john@example.com",
    "message": "Request for quote for the following items.",
    "created_at": "01-03-2025",
    "id": 1,
    "is_paid": false,
    "total_amount": 1000,
    "product_previews_with_quantity": [
      {
        "id": 1,
        "name": "S7-1200",
        "part_number": "6ES7214-1AG40-0XB0",
        "manufacturer": { "id": 1, "name": "Siemens" },
        "image_url": "https://example.com/s7-1200.jpg",
        "quantity": 5
      }
    ]
  }
}
```

### POST `/admin/quotes`
**Request body**
```json
{
  "name": "John Doe",
  "company_name": "Tech Corp",
  "country_code": "SG",
  "phone": "12345678",
  "email": "john@example.com",
  "message": "Quote request message",
  "is_paid": false,
  "total_amount": 1000,
  "product_previews_with_quantity": [
    {
      "id": 1,
      "name": "S7-1200",
      "part_number": "6ES7214-1AG40-0XB0",
      "manufacturer": { "id": 1, "name": "Siemens" },
      "image_url": "https://example.com/s7-1200.jpg",
      "quantity": 5
    }
  ]
}
```

### PUT `/admin/quote/{quote_id}`
Same schema as POST `/admin/quotes`.

### DELETE `/admin/quote/{quote_id}`

### POST `/admin/blogs`
**Request body**
```json
{
  "title": "New Blog Post",
  "image_url": "https://example.com/blog.jpg",
  "published_by": "Admin",
  "created_at": "01-03-2025",
  "updated_at": "01-03-2025",
  "content": "This is the full content of the blog post in HTML or Markdown.",
  "categories": [{ "id": 1, "name": "Guide" }]
}
```

### PUT `/admin/blogs/{blog_id}`
Same schema as POST `/admin/blogs`.

### DELETE `/admin/blogs/{blog_id}`

### POST `/admin/jobs`
**Request body**
```json
{
  "title": "New Job",
  "country": "SG",
  "location": "Singapore",
  "job_type": "Full-time",
  "posted_date": "01-03-2025",
  "industry": "Automation",
  "requirements": "Requirements here...",
  "responsibilities": "Responsibilities here...",
  "description": "Description here...",
  "working_hours": "9am-6pm"
}
```

### PUT `/admin/jobs/{job_id}`
Same schema as POST `/admin/jobs`.

### DELETE `/admin/jobs/{job_id}`

### POST `/admin/categories`
**Request body**
```json
{ "name": "New Category" }
```

### PUT `/admin/categories/{category_id}`
**Request body**
```json
{ "name": "Updated Category" }
```

### DELETE `/admin/categories/{category_id}`

### POST `/admin/manufacturers`
**Request body**
```json
{ "name": "New Manufacturer" }
```

### PUT `/admin/manufacturers/{manufacturer_id}`
**Request body**
```json
{ "name": "Updated Manufacturer" }
```

### DELETE `/admin/manufacturers/{manufacturer_id}`

### POST `/admin/countries`
**Request body**
```json
{ "name": "New Country", "code": "+00" }
```

### PUT `/admin/countries/{country_id}`
**Request body**
```json
{ "name": "Updated Country", "code": "+01" }
```

### DELETE `/admin/countries/{country_id}`

### GET `/admin/approvals?approval_id={[Optional]approval_id}&approval_type={[Optional]approval_type}&is_approved={[Optional]is_approved}&page={page}&per_page={per_page}`

**Response 200**
```json
{
  "page": 1,
  "per_page": 10,
  "total": 1,
  "approval_previews": [
    {
      "type": "POST Quote",
      "payload": "{\"quote_id\": 1}",
      "is_approved": false,
      "requester": "user@example.com",
      "request_date": "01-03-2025",
      "attachment_url": "https://example.com/quote.pdf"
    }
  ]
}
```

### POST `/admin/approvals`
**Content-Type**: `multipart/form-data`
**Request body**
- `payload`: JSON string matching `ApprovalRequest`
- `attachment`: (optional file)

`payload` schema:
```json
{
  "type": "POST Quote",
  "payload": "{\"quote_id\": 1, \"amount\": 1000}",
  "is_approved": false,
  "requester": "user@example.com",
  "request_date": "01-03-2025"
}
```

### DELETE `/admin/approvals/{approval_id}`

### PUT `/admin/approvals/{approval_id}/approve`

### PUT `/admin/approvals/{approval_id}/reject`

---

## Logging

### GET `/admin/log/{log_type}?date={YYYY-MM-DD}`
- `log_type`: `web`, `error`, `admin`, `debug`
- Returns a log file for download or redirects to storage.
