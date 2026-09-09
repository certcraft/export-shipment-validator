# Export Shipment Control

A validation MVP for testing a lightweight workflow for identifying cross-document discrepancies in export shipments.

## Overview

Export Shipment Control combines:
- A structured Excel shipment-control workbook
- A free workbook download
- A free user guide
- A free concierge shipment-audit request
- Django-based request storage and tracking
- An internal validation dashboard
- Django authentication for internal dashboard access

The goal is to validate the problem and user demand **before** investing in an automated document-comparison engine.

**Status:** Validation MVP — local testing complete; deployment preparation in progress.

## Why This Exists

Export documentation workflows contain multiple documents with overlapping shipment information, including Commercial Invoice, Packing List, Bill of Lading, container information, weights, quantities, buyer/consignee information, ports, and HS codes.

Inconsistent information across documents can create rework, clarification, operational delays, and additional coordination.

This project tests whether a structured discrepancy-checking workflow is useful enough for export and logistics professionals to adopt.

## What We're Testing

### 1. Self-Service Validation

Will export/logistics professionals download and use a structured Excel workbook to identify inconsistencies in their shipment documents?

### 2. Concierge Audit

Will users voluntarily submit shipment documents for a manually reviewed discrepancy audit?

The validation process is intended to gather evidence about:
- Actual usage
- Recurring problems
- User feedback
- Frequency of discrepancies
- Feature requests
- Repeat usage
- Willingness to pay

## Current Product Flow

```text
Landing Page
     |
     +---------------------+
     |                     |
     v                     v
Download Workbook     Request Free Audit
     |                     |
     v                     v
Download Event       Audit Request Form
     |                     |
     +----------+----------+
                |
                v
         Django Database
                |
                v
         Internal Admin
                |
         +------+------+
         |      |      |
        NEW  PROCESSING COMPLETED
                |
                v
       Manual Audit Workflow
```

## Current Features

### Public Website
- Landing page
- Product/problem explanation
- Free workbook download
- Free user guide download
- Free audit request form
- Audit request success page

### Workbook Download

The Django application serves the Excel validation workbook and records each download event.

Download events currently record:
- Session key
- Download timestamp

A download event is **not** treated as a unique person or confirmed lead.

### Free Audit Requests

Users can submit:
- Email
- Shipment reference
- Commercial Invoice
- Packing List
- Draft Bill of Lading
- Optional notes

Each request is stored in the Django database with a status.

Current workflow:

```text
NEW -> PROCESSING -> COMPLETED
```

### Internal Validation Dashboard

The dashboard is protected using Django authentication.

It currently displays:
- Workbook downloads
- Download leads
- Total audit requests
- New audit requests
- Processing audit requests
- Completed audit requests

Local URLs:

```text
Homepage:             http://127.0.0.1:8000/
Admin:                http://127.0.0.1:8000/admin/
Validation dashboard: http://127.0.0.1:8000/validation-dashboard/
Login:                http://127.0.0.1:8000/accounts/login/
```

## Excel Validation Workbook

The Excel workbook is the primary validation instrument. It helps users structure shipment information and identify potential discrepancies across documents.

Core workbook areas:
1. Shipment Master
2. Document Checklist
3. Logistics Log
4. Manual Check
5. Exception Log

It supports manual review of:
- Buyer / consignee
- Quantity
- Gross weight
- Container number
- HS code
- Port
- VGM-related checks
- Document completion status

The workbook is **not the final automated product**. It is being used to validate the workflow before automation.

Potential future workflow:

```text
Upload Documents
       |
Extract Shipment Data
       |
Cross-Document Comparison
       |
Exception Detection
       |
Human Review
       |
Exception Report
```

The automated comparison engine has intentionally not been built yet.

## Technology

Current stack:
- Python
- Django
- SQLite
- HTML / CSS
- Microsoft Excel / XLSX
- openpyxl for workbook-related development
- python-dotenv for environment configuration

## Project Structure

```text
export_validator/
|
+-- config/
|   +-- settings.py
|   +-- urls.py
|   +-- asgi.py
|   +-- wsgi.py
|
+-- validator/
|   +-- migrations/
|   +-- templates/
|   |   +-- registration/
|   |   |   +-- login.html
|   |   +-- validator/
|   |       +-- home.html
|   |       +-- audit_request.html
|   |       +-- audit_success.html
|   |       +-- validation_dashboard.html
|   +-- admin.py
|   +-- apps.py
|   +-- forms.py
|   +-- models.py
|   +-- tests.py
|   +-- urls.py
|   +-- views.py
|
+-- downloads/
|   +-- Export Shipment Control Workbook FINAL v7.xlsx
|   +-- Export_Shipment_Control_User_Guide.pdf
|
+-- .gitignore
+-- manage.py
+-- requirements.txt
```

Local-only files such as `.env`, `venv/`, `db.sqlite3`, and uploaded audit documents are intentionally excluded from version control.

## Django Models

### DownloadLead
Stores lead information when a lead record is explicitly created:
- `name`
- `email`
- `company_or_role`
- `created_at`

The current workbook download endpoint records `DownloadEvent` objects. It does **not** automatically create a `DownloadLead` when someone downloads the workbook.

### DownloadEvent
Records workbook download activity:
- `session_key`
- `downloaded_at`

The session key helps distinguish activity within browser sessions but should not be interpreted as a unique human/user count.

### AuditRequest
Stores submitted audit requests:
- `email`
- `shipment_reference`
- `invoice_file`
- `packing_list_file`
- `bl_file`
- `notes`
- `status`
- `created_at`

Current status values:

```text
NEW
PROCESSING
COMPLETED
```

## Local Setup

### 1. Clone the repository

```bash
git clone <REPOSITORY-URL>
cd export-shipment-validator
```

### 2. Create and activate a virtual environment

Windows:

```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure the environment

Create a `.env` file in the project root:

```text
SECRET_KEY=your-secret-key
```

Do not commit `.env` to Git.

### 5. Run migrations

```bash
python manage.py migrate
```

### 6. Create an administrator account

```bash
python manage.py createsuperuser
```

### 7. Run the development server

```bash
python manage.py runserver
```

Then open:

```text
http://127.0.0.1:8000/
```

## Environment Configuration

Sensitive configuration is kept outside source code using environment variables.

The project loads the local environment file with:

```python
load_dotenv(BASE_DIR / ".env")
```

and reads the secret using:

```python
SECRET_KEY = os.getenv("SECRET_KEY")
```

The `.env` file must never be committed to Git.

## Deployment Status

The application has been tested locally.

Verified workflows include:
- Homepage
- Workbook download
- User guide download
- Download event recording
- Audit request submission
- File upload storage
- Audit request in Django Admin
- Dashboard authentication
- Dashboard metrics
- Audit status workflow

**Public deployment is not yet complete.**

Before public deployment, production configuration still needs to be completed.

## Data Handling and Privacy

This application accepts commercial shipment documents during the audit workflow.

Before public launch, the following controls must be finalized:
- Define a document retention period
- Determine when uploaded documents are automatically deleted
- Ensure uploaded files are not publicly browsable
- Restrict access to uploaded documents
- Add an appropriate privacy notice
- Review information stored in the database
- Implement file-type validation
- Implement file-size limits
- Review production security settings
- Configure production email delivery if required

Until these controls are finalized, the audit-upload functionality should be treated as a **validation/development workflow**, not a production-grade document processing service.

## Security

The project uses Django authentication to protect the internal validation dashboard.

Production deployment must also address:
- `DEBUG`
- `ALLOWED_HOSTS`
- Production `SECRET_KEY`
- HTTPS
- Secure session cookies
- Secure CSRF cookies
- HSTS where appropriate
- Uploaded-file access controls
- Secret/environment management
- Production email configuration if required

Run Django's deployment checks with:

```bash
python manage.py check --deploy
```

## Validation Metrics

The project is designed to measure:
- Workbook downloads
- Download activity
- Audit requests
- Audit request completion
- Repeat requests
- Recurring discrepancy types
- User feedback
- Product feature requests
- Explicit payment interest

These metrics provide evidence for deciding whether further product development is justified.

## Product Development Philosophy

This project follows a **validation-first approach**.

We are intentionally avoiding premature development of:
- OCR pipelines
- AI document extraction
- Automated document comparison
- Complex SaaS dashboards
- Large ERP integrations
- Extensive workflow automation

The next major product investment should only happen after evidence from real users demonstrates that the underlying problem is sufficiently valuable.

## Project Phases

| Phase | Status | Description |
|---|---|---|
| 1 — Excel Prototype | Done | Workbook built, tested, and refined |
| 2 — Django Foundation | Done | Project, database, models, admin and website foundation |
| 3 — Validation Funnel | Done | Workbook download, audit request and internal dashboard |
| 4 — Deployment Preparation | Current | Production configuration and deployment |
| 5 — Real-User Validation | Next | Test with real export/logistics professionals |
| 6 — Automated Validation | Conditional | Build document comparison only if demand is demonstrated |
| 7 — Productization | Later | Develop the validated workflow into a scalable product |

## Current Objective

The immediate objective is **not to build more features**.

```text
Deploy
  |
Test Public Version
  |
Recruit First Real Users
  |
Observe Actual Usage
  |
Collect Feedback
  |
Identify Repeated Problems
  |
Test Willingness to Pay
  |
Decide Whether to Automate
```

If real-world evidence does not support the problem or willingness to pay, the project should be changed, narrowed, or stopped rather than expanded based only on assumptions.

## Future Product Direction

If validation produces sufficient evidence, the likely product direction is a lightweight shipment-document discrepancy checker.

Potential future workflow:

```text
Upload Invoice
      |
Upload Packing List
      |
Upload Draft B/L
      |
Extract Fields
      |
Cross-Document Comparison
      |
Identify Exceptions
      |
Review Findings
      |
Generate Exception Report
```

Potential integrations may eventually include relevant export, logistics, or business systems. Integrations will only be prioritized after the core workflow has been validated.

## Contact

**Samim Craft**

Email: `certcraft25@gmail.com`

## Project Principle

> **Validate the problem before automating the solution.**
