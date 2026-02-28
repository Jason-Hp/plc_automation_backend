# PLC Automation Backend API Endpoints

Base URL: `http://localhost:8000`

All endpoints below are under `/api`.

## Header rules (applies to every endpoint)

- `lang`: optional, default `en`
- `country`: optional, default `SG`
- `Authorization`: required for all `/api/admin/*` endpoints **except** `/api/admin/login`

---

## Health Route

### GET `/api/health`
**Headers**
```json
{
  "lang": "en (optional)",
  "country": "SG (optional)"
}
```

**Request body**
```json
{}
```

**Response 200**
```json
{
  "status": "ok"
}
```

---

## Forms Routes

### POST `/api/enquiry`
**Headers**
```json
{
  "lang": "en (optional)",
  "country": "SG (optional)"
}
```

**Request body (application/json)**
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

**Response 200**
```json
{
  "message": "Your query has been submitted successfully."
}
```

### POST `/api/quote`
**Headers**
```json
{
  "lang": "en (optional)",
  "country": "SG (optional)",
  "Content-Type": "multipart/form-data"
}
```

**Request body (multipart/form-data)**
- `payload` (json string)
- `attachment` (file, optional)

`payload` JSON schema:
```json
{
  "name": "John Doe",
  "company_name": "ACME Industrial",
  "country_code": "65",
  "phone": "98765432",
  "email": "john@acme.com",
  "message": "Need quote",
  "product_previews_with_quantity": [
    {
      "id": 1,
      "name": "SIMATIC S7-1500 CPU",
      "part_number": "CPU-1510",
      "manufacturer": {
        "id": 1,
        "name": "Siemens"
      },
      "image_url": "https://cdn.example.com/products/cpu-1510.jpg",
      "quantity": 1
    }
  ]
}
```

**Response 200**
```json
{
  "message": "Your enquiry has been submitted successfully."
}
```

### POST `/api/newsletter`
**Headers**
```json
{
  "lang": "en (optional)",
  "country": "SG (optional)"
}
```

**Request body (application/json)**
```json
{
  "email": "subscriber@example.com"
}
```

**Response 200**
```json
{
  "message": "Thank you for subscribing."
}
```
---

## Product Routes

### GET `/api/products?page=1&per_page=30&category=<optional>&search=<optional>`
**Headers**
```json
{
  "lang": "en (optional)",
  "country": "SG (optional)"
}
```

**Request body**
```json
{}
```

**Response 200**
```json
{
  "product_previews": [
    {
      "id": 1,
      "name": "SIMATIC S7-1500 CPU",
      "part_number": "CPU-1510",
      "manufacturer": {
        "id": 1,
        "name": "Siemens"
      },
      "image_url": "https://cdn.example.com/products/cpu-1510.jpg"
    }
  ],
  "page": 1,
  "per_page": 30,
  "total": 1
}
```

### GET `/api/products/{product_id}`
**Headers**
```json
{
  "lang": "en (optional)",
  "country": "SG (optional)"
}
```

**Request body**
```json
{}
```

**Response 200**
```json
{
  "id": 1,
  "name": "SIMATIC S7-1500 CPU",
  "part_number": "CPU-1510",
  "manufacturer": {
    "id": 1,
    "name": "Siemens"
  },
  "image_url": "https://cdn.example.com/products/cpu-1510.jpg",
  "stock": true,
  "description": "Sample PLC CPU for wiring cabinets."
}
```

**Response 404**
```json
{
  "detail": "Product not found"
}
```

---

## Info Routes

### GET `/api/faqs`
**Headers**
```json
{
  "lang": "en (optional)",
  "country": "SG (optional)"
}
```

**Request body**
```json
{}
```

**Response 200**
```json
[
  {
    "id": 1,
    "question": "What is PLC automation?",
    "answer": "..."
  }
]
```

### GET `/api/contact-info`
**Headers**
```json
{
  "lang": "en (optional)",
  "country": "SG (optional)"
}
```

**Request body**
```json
{}
```

**Response 200**
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

### GET `/api/contact-info/{country}`
**Headers**
```json
{
  "lang": "en (optional)",
  "country": "SG (optional)"
}
```

**Request body**
```json
{}
```

**Response 200**
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

**Response 404**
```json
{
  "detail": "Contact info not found"
}
```

### GET `/api/categories`
**Headers**
```json
{
  "lang": "en (optional)",
  "country": "SG (optional)"
}
```

**Request body**
```json
{}
```

**Response 200**
```json
[
  {
    "id": 1,
    "name": "PLC Systems"
  }
]
```

### GET `/api/manufacturers`
**Headers**
```json
{
  "lang": "en (optional)",
  "country": "SG (optional)"
}
```

**Request body**
```json
{}
```

**Response 200**
```json
[
  {
    "id": 1,
    "name": "Siemens"
  }
]
```

### GET `/api/countries`
**Headers**
```json
{
  "lang": "en (optional)",
  "country": "SG (optional)"
}
```

**Request body**
```json
{}
```

**Response 200**
```json
[
  {
    "id": 1,
    "name": "Singapore",
    "code": "SG"
  }
]
```

---

## Blog Routes

### POST `/api/blogs/?page=1&per_page=10`
**Headers**
```json
{
  "lang": "en (optional)",
  "country": "SG (optional)"
}
```

**Request body**
```json
{
  "search": "PLC",
  "categories": [
    {
      "id": 1,
      "name": "Guide"
    }
  ]
}
```

**Response 200**
```json
{
  "page": 1,
  "per_page": 10,
  "total": 1,
  "blog_previews": [
    {
      "id": 1,
      "title": "How to select a PLC",
      "categories": [
        {
          "id": 1,
          "name": "Guide"
        }
      ],
      "image_url": "https://cdn.example.com/blogs/plc-guide.jpg",
      "published_by": "PLC Automation",
      "created_at": "01-01-2025",
      "updated_at": "02-01-2025"
    }
  ]
}
```

### GET `/api/blogs/{blogId}`
**Headers**
```json
{
  "lang": "en (optional)",
  "country": "SG (optional)"
}
```

**Request body**
```json
{}
```

**Response 200**
```json
{
  "id": 1,
  "title": "How to select a PLC",
  "categories": [
    {
      "id": 1,
      "name": "Guide"
    }
  ],
  "image_url": "https://cdn.example.com/blogs/plc-guide.jpg",
  "published_by": "PLC Automation",
  "created_at": "01-01-2025",
  "updated_at": "02-01-2025",
  "content": "..."
}
```

**Response 404**
```json
{
  "detail": "Blog not found"
}
```

---

## Search Routes

### GET `/api/semantic-search?query=<required>&top_k=10`
**Headers**
```json
{
  "lang": "en (optional)",
  "country": "SG (optional)"
}
```

**Request body**
```json
{}
```

**Response 200**
```json
[
  {
    "id": 1,
    "name": "SIMATIC S7-1500 CPU",
    "part_number": "CPU-1510",
    "manufacturer": {
      "id": 1,
      "name": "Siemens"
    },
    "image_url": "https://cdn.example.com/products/cpu-1510.jpg"
  }
]
```

---

## Job Routes

### GET `/api/jobs/`
**Headers**
```json
{
  "lang": "en (optional)",
  "country": "SG (optional)"
}
```

**Request body**
```json
{}
```

**Response 200**
```json
[
  {
    "id": 1,
    "title": "PLC Engineer",
    "country": "SG",
    "location": "Singapore",
    "job_type": "Full-time",
    "posted_date": "01-01-2025"
  }
]
```

### GET `/api/jobs/{job_id}`
**Headers**
```json
{
  "lang": "en (optional)",
  "country": "SG (optional)"
}
```

**Request body**
```json
{}
```

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
  "working_hours": "Mon-Fri 9AM-6PM"
}
```

### POST `/api/jobs/{job_id}/application`
**Headers**
```json
{
  "lang": "en (optional)",
  "country": "SG (optional)",
  "Content-Type": "multipart/form-data"
}
```

**Request body (multipart/form-data)**
- `payload` (json string)
- `resume` (file, required)

`payload` JSON schema:
```json
{
  "first_name": "Jane",
  "last_name": "Doe",
  "email": "jane@example.com",
  "country_code": "65",
  "phone": "91234567",
  "experience": "5 years"
}
```

**Response 200**
```json
{
  "message": "Application submitted successfully."
}
```

---

## Admin Routes

> All admin endpoints below require:
>
> `Authorization: Bearer <token>`

### POST `/api/admin/login`
**Headers**
```json
{
  "lang": "en (optional)",
  "country": "SG (optional)"
}
```

**Request body (application/json)**
```json
{
  "username": "admin",
  "password": "password"
}
```

**Response 200**
```json
"<jwt_token>"
```

**Response 401**
```json
{
  "detail": "Invalid credentials"
}
```

### POST `/api/admin/products/batch`
**Headers**
```json
{
  "lang": "en (optional)",
  "country": "SG (optional)",
  "Authorization": "Bearer <token>",
  "Content-Type": "multipart/form-data"
}
```

**Request body (multipart/form-data)**
- `csv_file` (file, required, `.csv`)

**Response 200**
```json
{
  "processed": 12,
  "message": "CSV processed (placeholder)."
}
```

### POST `/api/admin/products`
**Headers**
```json
{
  "lang": "en (optional)",
  "country": "SG (optional)",
  "Authorization": "Bearer <token>"
}
```

**Query params**
- `country_ids` (required, repeatable integer values)

**Request body (application/json)**
```json
{
  "id": 2,
  "name": "Relay Module",
  "part_number": "RM-100",
  "manufacturer": {
    "id": 2,
    "name": "BrandX"
  },
  "image_url": "https://cdn.example.com/products/relay-module.jpg",
  "stock": true,
  "description": "Industrial relay"
}
```

**Response 200**
```json
{
  "message": "Product uploaded successfully."
}
```

### PUT `/api/admin/products/{product_id}`
**Headers**
```json
{
  "lang": "en (optional)",
  "country": "SG (optional)",
  "Authorization": "Bearer <token>"
}
```

**Query params**
- `country_ids` (required, repeatable integer values)

**Request body (application/json)**
```json
{
  "id": 2,
  "name": "Relay Module",
  "part_number": "RM-100",
  "manufacturer": {
    "id": 2,
    "name": "BrandX"
  },
  "image_url": "https://cdn.example.com/products/relay-module.jpg",
  "stock": true,
  "description": "Industrial relay"
}
```

**Response 200**
```json
{
  "message": "Product updated successfully."
}
```

### DELETE `/api/admin/products/{product_id}`
**Headers**
```json
{
  "lang": "en (optional)",
  "country": "SG (optional)",
  "Authorization": "Bearer <token>"
}
```

**Request body**
```json
{}
```

**Response 200**
```json
{
  "message": "Product deleted successfully."
}
```

### POST `/api/admin/broadcast-newsletter`
**Headers**
```json
{
  "lang": "en (optional)",
  "country": "SG (optional)",
  "Authorization": "Bearer <token>",
  "Content-Type": "multipart/form-data"
}
```

**Request body (multipart/form-data)**
- `payload` (json string)
- `attachments` (file list, optional)

`payload` JSON schema:
```json
{
  "subject": "Monthly updates",
  "content": "New products available"
}
```

**Response 200**
```json
{
  "message": "Newsletter broadcasted."
}
```

### POST `/api/admin/faqs`
**Headers**
```json
{
  "lang": "en (optional)",
  "country": "SG (optional)",
  "Authorization": "Bearer <token>"
}
```

**Request body (application/json)**
```json
[
  {
    "question": "What is PLC?",
    "answer": "Programmable Logic Controller"
  }
]
```

**Response 200**
```json
{
  "message": "FAQs uploaded successfully."
}
```

### PUT `/api/admin/faqs/{faq_id}`
**Headers**
```json
{
  "lang": "en (optional)",
  "country": "SG (optional)",
  "Authorization": "Bearer <token>"
}
```

**Request body (application/json)**
```json
{
  "question": "Updated question",
  "answer": "Updated answer"
}
```

**Response 200**
```json
{
  "message": "FAQ updated successfully."
}
```

### DELETE `/api/admin/faqs/{faq_id}`
**Headers**
```json
{
  "lang": "en (optional)",
  "country": "SG (optional)",
  "Authorization": "Bearer <token>"
}
```

**Request body**
```json
{}
```

**Response 200**
```json
{
  "message": "FAQ deleted successfully."
}
```

### POST `/api/admin/contact-info`
**Headers**
```json
{
  "lang": "en (optional)",
  "country": "SG (optional)",
  "Authorization": "Bearer <token>"
}
```

**Request body (application/json)**
```json
{
  "address": "1 Example Street",
  "phone": "+65 6000 0000",
  "email": "info@example.com",
  "working_hours": "Mon-Fri 9AM-6PM",
  "country": "SG"
}
```

**Response 200**
```json
{
  "message": "Contact info uploaded successfully."
}
```

### PUT `/api/admin/contact-info/{contact_id}`
**Headers**
```json
{
  "lang": "en (optional)",
  "country": "SG (optional)",
  "Authorization": "Bearer <token>"
}
```

**Request body (application/json)**
```json
{
  "address": "1 Example Street",
  "phone": "+65 6000 0000",
  "email": "info@example.com",
  "working_hours": "Mon-Fri 9AM-6PM",
  "country": "SG"
}
```

**Response 200**
```json
{
  "message": "Contact info updated successfully."
}
```

### DELETE `/api/admin/contact-info/{contact_id}`
**Headers**
```json
{
  "lang": "en (optional)",
  "country": "SG (optional)",
  "Authorization": "Bearer <token>"
}
```

**Request body**
```json
{}
```

**Response 200**
```json
{
  "message": "Contact info deleted successfully."
}
```

### POST `/api/admin/blogs`
**Headers**
```json
{
  "lang": "en (optional)",
  "country": "SG (optional)",
  "Authorization": "Bearer <token>"
}
```

**Request body (application/json)**
```json
{
  "blog": {
    "id": 1,
    "title": "How to select a PLC",
    "categories": [
      {
        "id": 1,
        "name": "Guide"
      }
    ],
    "image_url": "https://cdn.example.com/blog.jpg",
    "published_by": "PLC Automation",
    "created_at": "01-01-2025",
    "updated_at": "01-01-2025",
    "content": "Long article body"
  },
  "categories": [
    {
      "id": 1,
      "name": "Guide"
    }
  ]
}
```

**Response 200**
```json
{
  "message": "Blog uploaded successfully."
}
```

### PUT `/api/admin/blogs/{blog_id}`
**Headers**
```json
{
  "lang": "en (optional)",
  "country": "SG (optional)",
  "Authorization": "Bearer <token>"
}
```

**Request body (application/json)**
```json
{
  "blog": {
    "id": 1,
    "title": "How to select a PLC",
    "categories": [
      {
        "id": 1,
        "name": "Guide"
      }
    ],
    "image_url": "https://cdn.example.com/blog.jpg",
    "published_by": "PLC Automation",
    "created_at": "01-01-2025",
    "updated_at": "01-01-2025",
    "content": "Long article body"
  },
  "categories": [
    {
      "id": 1,
      "name": "Guide"
    }
  ]
}
```

**Response 200**
```json
{
  "message": "Blog updated successfully."
}
```

### DELETE `/api/admin/blogs/{blog_id}`
**Headers**
```json
{
  "lang": "en (optional)",
  "country": "SG (optional)",
  "Authorization": "Bearer <token>"
}
```

**Request body**
```json
{}
```

**Response 200**
```json
{
  "message": "Blog deleted successfully."
}
```

### POST `/api/admin/jobs`
**Headers**
```json
{
  "lang": "en (optional)",
  "country": "SG (optional)",
  "Authorization": "Bearer <token>"
}
```

**Request body (application/json)**
```json
{
  "title": "PLC Engineer",
  "country": "SG",
  "location": "Singapore",
  "job_type": "Full-time",
  "posted_date": "01-01-2025",
  "industry": "Automation",
  "requirements": "...",
  "responsibilities": "...",
  "description": "...",
  "working_hours": "Mon-Fri 9AM-6PM"
}
```

**Response 200**
```json
{
  "message": "Job uploaded successfully."
}
```

### PUT `/api/admin/jobs/{job_id}`
**Headers**
```json
{
  "lang": "en (optional)",
  "country": "SG (optional)",
  "Authorization": "Bearer <token>"
}
```

**Request body (application/json)**
```json
{
  "title": "PLC Engineer",
  "country": "SG",
  "location": "Singapore",
  "job_type": "Full-time",
  "posted_date": "01-01-2025",
  "industry": "Automation",
  "requirements": "...",
  "responsibilities": "...",
  "description": "...",
  "working_hours": "Mon-Fri 9AM-6PM"
}
```

**Response 200**
```json
{
  "message": "Job updated successfully."
}
```

### DELETE `/api/admin/jobs/{job_id}`
**Headers**
```json
{
  "lang": "en (optional)",
  "country": "SG (optional)",
  "Authorization": "Bearer <token>"
}
```

**Request body**
```json
{}
```

**Response 200**
```json
{
  "message": "Job deleted successfully."
}
```

### POST `/api/admin/categories`
**Headers**
```json
{
  "lang": "en (optional)",
  "country": "SG (optional)",
  "Authorization": "Bearer <token>"
}
```

**Request body (application/json)**
```json
{
  "name": "PLC Systems"
}
```

**Response 200**
```json
{
  "message": "Category uploaded successfully."
}
```

### PUT `/api/admin/categories/{category_id}`
**Headers**
```json
{
  "lang": "en (optional)",
  "country": "SG (optional)",
  "Authorization": "Bearer <token>"
}
```

**Request body (application/json)**
```json
{
  "name": "PLC Systems"
}
```

**Response 200**
```json
{
  "message": "Category updated successfully."
}
```

### DELETE `/api/admin/categories/{category_id}`
**Headers**
```json
{
  "lang": "en (optional)",
  "country": "SG (optional)",
  "Authorization": "Bearer <token>"
}
```

**Request body**
```json
{}
```

**Response 200**
```json
{
  "message": "Category deleted successfully."
}
```

### POST `/api/admin/manufacturers`
**Headers**
```json
{
  "lang": "en (optional)",
  "country": "SG (optional)",
  "Authorization": "Bearer <token>"
}
```

**Request body (application/json)**
```json
{
  "name": "Siemens"
}
```

**Response 200**
```json
{
  "message": "Manufacturer uploaded successfully."
}
```

### PUT `/api/admin/manufacturers/{manufacturer_id}`
**Headers**
```json
{
  "lang": "en (optional)",
  "country": "SG (optional)",
  "Authorization": "Bearer <token>"
}
```

**Request body (application/json)**
```json
{
  "name": "Siemens"
}
```

**Response 200**
```json
{
  "message": "Manufacturer updated successfully."
}
```

### DELETE `/api/admin/manufacturers/{manufacturer_id}`
**Headers**
```json
{
  "lang": "en (optional)",
  "country": "SG (optional)",
  "Authorization": "Bearer <token>"
}
```

**Request body**
```json
{}
```

**Response 200**
```json
{
  "message": "Manufacturer deleted successfully."
}
```

### POST `/api/admin/countries`
**Headers**
```json
{
  "lang": "en (optional)",
  "country": "SG (optional)",
  "Authorization": "Bearer <token>"
}
```

**Request body (application/json)**
```json
{
  "name": "Singapore",
  "code": "SG"
}
```

**Response 200**
```json
{
  "message": "Country uploaded successfully."
}
```

### PUT `/api/admin/countries/{country_id}`
**Headers**
```json
{
  "lang": "en (optional)",
  "country": "SG (optional)",
  "Authorization": "Bearer <token>"
}
```

**Request body (application/json)**
```json
{
  "name": "Singapore",
  "code": "SG"
}
```

**Response 200**
```json
{
  "message": "Country updated successfully."
}
```

### DELETE `/api/admin/countries/{country_id}`
**Headers**
```json
{
  "lang": "en (optional)",
  "country": "SG (optional)",
  "Authorization": "Bearer <token>"
}
```

**Request body**
```json
{}
```

**Response 200**
```json
{
  "message": "Country deleted successfully."
}
```

### GET `/api/admin/quotes?search=<optional>&page=1&per_page=10`
**Headers**
```json
{
  "lang": "en (optional)",
  "country": "SG (optional)",
  "Authorization": "Bearer <token>"
}
```

**Request body**
```json
{}
```

**Response 200**
```json
{
  "page": 1,
  "per_page": 10,
  "total": 1,
  "quotes": [
    {
      "id": 1,
      "name": "John Doe",
      "company_name": "ACME Industrial",
      "country_code": "65",
      "phone": "98765432",
      "email": "john@acme.com",
      "message": "Need quote",
      "created_at": "2026-01-01T00:00:00+00:00",
      "is_paid": false,
      "total_amount": 0,
      "product_previews_with_quantity": [
        {
          "id": 1,
          "name": "SIMATIC S7-1500 CPU",
          "part_number": "CPU-1510",
          "manufacturer": {
            "id": 1,
            "name": "Siemens"
          },
          "image_url": "https://cdn.example.com/products/cpu-1510.jpg",
          "quantity": 2
        }
      ]
    }
  ]
}
```

### GET `/api/admin/quote/{quote_id}`
**Headers**
```json
{
  "lang": "en (optional)",
  "country": "SG (optional)",
  "Authorization": "Bearer <token>"
}
```

**Request body**
```json
{}
```

**Response 200**
```json
{
  "id": 1,
  "name": "John Doe",
  "company_name": "ACME Industrial",
  "country_code": "65",
  "phone": "98765432",
  "email": "john@acme.com",
  "message": "Need quote",
  "created_at": "2026-01-01T00:00:00+00:00",
  "is_paid": false,
  "total_amount": 0,
  "product_previews_with_quantity": [
    {
      "id": 1,
      "name": "SIMATIC S7-1500 CPU",
      "part_number": "CPU-1510",
      "manufacturer": {
        "id": 1,
        "name": "Siemens"
      },
      "image_url": "https://cdn.example.com/products/cpu-1510.jpg",
      "quantity": 2
    }
  ]
}
```

### POST `/api/admin/quotes`
**Headers**
```json
{
  "lang": "en (optional)",
  "country": "SG (optional)",
  "Authorization": "Bearer <token>"
}
```

**Request body (application/json)**
```json
{
  "name": "John Doe",
  "company_name": "ACME Industrial",
  "country_code": "65",
  "phone": "98765432",
  "email": "john@acme.com",
  "message": "Need quote",
  "is_paid": false,
  "total_amount": 0,
  "product_previews_with_quantity": [
    {
      "id": 1,
      "name": "SIMATIC S7-1500 CPU",
      "part_number": "CPU-1510",
      "manufacturer": {
        "id": 1,
        "name": "Siemens"
      },
      "image_url": "https://cdn.example.com/products/cpu-1510.jpg",
      "quantity": 2
    }
  ]
}
```

**Response 200**
```json
{
  "message": "Quote added successfully."
}
```

### PUT `/api/admin/quote/{quote_id}`
**Headers**
```json
{
  "lang": "en (optional)",
  "country": "SG (optional)",
  "Authorization": "Bearer <token>"
}
```

**Request body (application/json)**
```json
{
  "name": "John Doe",
  "company_name": "ACME Industrial",
  "country_code": "65",
  "phone": "98765432",
  "email": "john@acme.com",
  "message": "Updated quote request",
  "is_paid": true,
  "total_amount": 500,
  "product_previews_with_quantity": [
    {
      "id": 1,
      "name": "SIMATIC S7-1500 CPU",
      "part_number": "CPU-1510",
      "manufacturer": {
        "id": 1,
        "name": "Siemens"
      },
      "image_url": "https://cdn.example.com/products/cpu-1510.jpg",
      "quantity": 1
    }
  ]
}
```

**Response 200**
```json
{
  "message": "Quote updated successfully."
}
```

### DELETE `/api/admin/quote/{quote_id}`
**Headers**
```json
{
  "lang": "en (optional)",
  "country": "SG (optional)",
  "Authorization": "Bearer <token>"
}
```

**Request body**
```json
{}
```

**Response 200**
```json
{
  "message": "Quote deleted successfully."
}
```

### GET `/api/admin/admin_logs?date=<optional: YYYY-MM-DD>`
**Headers**
```json
{
  "lang": "en (optional)",
  "country": "SG (optional)",
  "Authorization": "Bearer <token>"
}
```

**Request body**
```json
{}
```

**Response 200**
- Downloads `admin_logs_<date>.log`

**Response 403**
```json
{
  "detail": "Only admin can access logs."
}
```

**Response 404**
```json
{
  "detail": "Log file for <date> not found."
}
```

### GET `/api/admin/approvals?approval_id=<optional>&approval_type=<optional>&is_approved=<optional>&page=1&per_page=10`
**Headers**
```json
{
  "lang": "en (optional)",
  "country": "SG (optional)",
  "Authorization": "Bearer <token>"
}
```

**Request body**
```json
{}
```

**Response 200**
```json
{
  "page": 1,
  "per_page": 10,
  "total": 1,
  "approvals": [
    {
      "id": 1,
      "type": "UPDATE-Product",
      "payload": "{\"product_id\": 1, \"field\": \"price\", \"new_value\": 500}",
      "is_approved": false,
      "requester": "updater_1",
      "request_date": "2026-01-01",
      "attachment_url": "https://cdn.example.com/uploads/change.pdf"
    }
  ]
}
```

### POST `/api/admin/approvals`
**Headers**
```json
{
  "lang": "en (optional)",
  "country": "SG (optional)",
  "Authorization": "Bearer <token>"
}
```

**Request body (application/json)**
```json
{
  "type": "ADD_Product",
  "payload": "{\"product_id\": 1, \"field\": \"price\", \"new_value\": 500}",
  "is_approved": false,
  "requester": "(auto-filled from token)",
  "request_date": "(auto-filled by server)",
  "attachment_url": "(auto-filled when attachment is saved)"
}
```

**Optional attachment**
- `attachment` (file)

**Response 200**
```json
{
  "message": "Approval added successfully."
}
```

### DELETE `/api/admin/approvals/{approval_id}`
**Headers**
```json
{
  "lang": "en (optional)",
  "country": "SG (optional)",
  "Authorization": "Bearer <token>"
}
```

**Request body**
```json
{}
```

**Response 200**
```json
{
  "message": "Approval deleted successfully."
}
```

### PUT `/api/admin/approvals/{approval_id}/approve`
**Headers**
```json
{
  "lang": "en (optional)",
  "country": "SG (optional)",
  "Authorization": "Bearer <token>"
}
```

**Request body**
```json
{}
```

**Response 200**
```json
{
  "message": "Approval approved successfully."
}
```

### PUT `/api/admin/approvals/{approval_id}/reject`
**Headers**
```json
{
  "lang": "en (optional)",
  "country": "SG (optional)",
  "Authorization": "Bearer <token>"
}
```

**Request body**
```json
{}
```

**Response 200**
```json
{
  "message": "Approval rejected successfully."
}
```

---

