# PLC Automation Backend Refactor (FastAPI)

This folder contains a backend-only refactor of the legacy PHP site. The frontend is assumed to be handled by a React/Next.js application. The backend is designed to expose simple RESTful endpoints for forms, products, and admin workflows that were previously handled by PHP scripts.

## Goals
- Provide a clear backend boundary that a React/Next.js frontend can call.
- Replace PHP mail/form handlers with FastAPI endpoints.
- Keep implementation simple and RESTful.
- Leave placeholders and TODOs for database schema, credentials, and mail providers.

## Key Legacy PHP Mappings (Backend Only)
| Legacy PHP | Purpose | New Endpoint |
| --- | --- | --- |
| `mailContact.php` | Contact form | `POST /api/contact` |
| `mail.php` | Product enquiry form | `POST /api/enquiries` |
| `mailNewsletter.php` | Newsletter subscribe | `POST /api/newsletter` |
| `apply-job-mail.php` | Job application form + resume upload | `POST /api/job-applications` |
| `submit_quick_quote_form.php` | Quick quote form + attachment | `POST /api/quotes` |
| `getbrandsData.php` | Product listing + pagination | `GET /api/products` |
| `product_offer_csv.php` | Offer product CSV upload | `POST /api/admin/offer-products/upload` |

## Running Locally
```bash
cd refactor
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

## Configuration
The API uses environment variables. Copy `.env.example` to `.env` and fill in values.

## Notes / TODOs
- Database connections are abstracted in `app/repositories/`. Replace the in-memory placeholders with real SQL queries.
- Email sending uses SMTP placeholders in `app/services/email_service.py`. Replace with your provider.
- File storage for uploads is abstracted in `app/services/storage_service.py` (currently local disk). Swap in S3/GCS if needed.
- Authentication and admin protection are not implemented; add JWT or session auth if required.
