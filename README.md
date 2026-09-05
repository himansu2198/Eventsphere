# EventSphere — Smart Event Planning Platform with Resource Coordination System

A full-featured Django-based event management system built for college/campus events, developed as part of the Infosys Springboard Training Program. Supports two roles — Admin and Participant — with digital ticketing, QR-based check-in, venue conflict detection, budget tracking, and more.

---

## Table of Contents

- [Features](#features)
- [Tech Stack](#tech-stack)
- [System Architecture](#system-architecture)
- [Folder Structure](#folder-structure)
- [Setup & Installation](#setup--installation)
- [Running the Project](#running-the-project)
- [Environment Variables](#environment-variables)
- [Default Roles](#default-roles)
- [Project Status](#project-status)

---

## Features

### Core Event Management
- Event categories with images, priority, and status
- Full event lifecycle: create, edit, delete, status tracking, history log
- Venue registry with capacity, amenities, and booking conflict detection
- Registration deadlines and participant capacity limits, enforced automatically

### Participant & Ticketing
- Self-service and admin-managed participant registration
- Role-based registration (Participant, Volunteer, Speaker, VIP, Sponsor, etc.)
- Automatic QR ticket generation for attendance-tracked roles
- Webcam-based QR check-in scanner with manual code entry fallback
- Entry/Exit attendance tracking with duplicate check-in prevention
- Registration-status validation (only Confirmed registrations can check in)

### Vendor, Venue, Resource & Sponsor Management
- Vendor onboarding with contract documents, dates, and status tracking
- Venue management with facility chips, type, and availability status
- Resource/equipment inventory with allocation tracking and over-allocation prevention
- Sponsor directory with logo upload and sponsorship revenue tracking

### Budget & Financial Tracking
- Event-level budget allocation
- Expense recording with invoice upload and high-value approval workflow
- Live budget utilization dashboard

### Admin Dashboard
- Real-time stats, Chart.js analytics, activity feed
- Light/Dark theme customizer with persistent settings
- Live notification system

### Additional Features
- AI-powered FAQ chatbot (Groq API) for participant support
- CSV, Excel, and PDF export for events, members, and reports
- Django REST Framework API for categories, events, members, and vendors

---

## Tech Stack

| Layer | Technology |
|---|---|
| Backend | Python, Django 6, Django REST Framework |
| Frontend | HTML, CSS, Bootstrap 5, JavaScript |
| Database | SQLite |
| QR Codes | `qrcode` (generation), `html5-qrcode` (scanning) |
| Exports | `reportlab` (PDF), `openpyxl` (Excel) |
| AI Chatbot | Groq API |
| Tools | VS Code, Git, GitHub |

---

## System Architecture

EventSphere follows Django's **MVT (Model–View–Template)** architecture:

```text
                    USER / ADMIN
                         │
                         ▼
                  Web Interface
              (HTML / CSS / Bootstrap)
                         │
                         ▼
                   Django URLs
              (routes the request)
                         │
                         ▼
                  Django Views
        (business logic, validation, QR generation,
         venue conflict checks, budget calculations)
                         │
                         ▼
                  Django Models
         (Event, EventMember, Venue, Vendor, Sponsor,
              Expense, UserMark, Notification, etc.)
                         │
                         ▼
                 SQLite Database
```

**Flow explanation:**
1. A user or admin interacts with the browser-based interface.
2. The request hits Django's URL router, which maps it to the correct view function.
3. The view applies business logic — e.g. checking venue availability, validating registration deadlines, or generating a QR ticket.
4. The view queries or updates data through Django's ORM (Models), which maps directly to SQLite tables.
5. The response is rendered back through a template and returned to the browser.

This separation keeps routing, logic, and data cleanly isolated, making the codebase easier to debug, extend, and maintain.

---

## Folder Structure

```text
Event Registration Platform/
│
├── Eventregistration/              # Django project configuration
│   ├── settings.py                 # Project settings (apps, DB, static/media, Groq key)
│   ├── urls.py                     # Root URL routing
│   ├── wsgi.py
│   └── asgi.py
│
├── event/                          # Main Django app
│   ├── models.py                   # Database models (Event, Venue, Vendor, etc.)
│   ├── views.py                    # All view logic (admin + participant)
│   ├── urls.py                     # (included via project urls.py)
│   ├── decorators.py               # admin_required decorator
│   ├── utils.py                    # QR generation, notification helpers
│   ├── api_views.py                # REST API views
│   │
│   ├── templates/                  # HTML templates
│   │   ├── admin_base.html         # Shared admin layout (sidebar, navbar, customizer)
│   │   ├── dashboard.html
│   │   ├── event-list.html
│   │   ├── create-event.html
│   │   ├── vendor-list.html
│   │   ├── venue-list.html
│   │   ├── resource-list.html
│   │   ├── sponsor-list.html
│   │   ├── budget-overview.html
│   │   ├── qr-checkin.html
│   │   ├── reports.html
│   │   ├── chatbot-faq.html
│   │   ├── participant-dashboard.html
│   │   ├── participant-event-list.html
│   │   ├── participant-event-detail.html
│   │   ├── registration/
│   │   │   └── login.html
│   │   └── ... (40+ templates total)
│   │
│   └── static/
│       ├── css/
│       │   └── style.css           # Global stylesheet (design system, dark mode)
│       ├── js/
│       │   ├── customizer.js       # Theme customizer logic
│       │   └── app-utils.js        # Shared toast/table/form utilities
│       └── img/
│           └── avatar.jpeg         # Default avatar
│
├── media/                          # User-uploaded files (gitignored)
│   ├── avatars/
│   ├── category_images/
│   ├── event_images/
│   ├── qr_codes/
│   ├── vendor_contracts/
│   ├── expense_invoices/
│   └── sponsor_logos/
│
├── env/                            # Python virtual environment (gitignored)
├── db.sqlite3                      # SQLite database (gitignored)
├── .env                            # Environment variables (gitignored, holds GROQ_API_KEY)
├── .gitignore
├── manage.py
├── requirements.txt
└── README.md
```

---

## Setup & Installation

### 1. Clone the repository

```bash
git clone https://github.com/himansu2198/Eventsphere.git
cd Eventregistration
```

### 2. Open in VS Code

```bash
code .
```

### 3. Create and activate a virtual environment

```bash
python -m venv env
```

**Windows:**
```bash
env\Scripts\activate
```

**macOS/Linux:**
```bash
source env/bin/activate
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

If `requirements.txt` is missing, install manually:
```bash
pip install django djangorestframework qrcode pillow reportlab openpyxl groq python-decouple
```

### 5. Set up environment variables

Create a `.env` file in the project root:
GROQ_API_KEY=your_groq_api_key_here


### 6. Run database migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 7. Create an admin (superuser) account

```bash
python manage.py createsuperuser
```

---

## Running the Project

Start the development server:

```bash
python manage.py runserver
```

Visit the application at:

http://127.0.0.1:8000/


To run on a different port:
```bash
python manage.py runserver 8080
```

---

## Environment Variables

| Variable | Description |
|---|---|
| `GROQ_API_KEY` | API key for the FAQ chatbot (Groq). Get one free at [console.groq.com](https://console.groq.com) |

---

## Default Roles

| Role | Access |
|---|---|
| **Admin** | Full access — event/category/venue/vendor/resource/sponsor management, budget tracking, QR check-in, reports |
| **Participant** | Browse events, register, view QR tickets, access FAQ assistant |

Admin accounts are created via `createsuperuser` and assigned the `admin` role through the `Profile` model. Participants self-register via the signup page.

---

## Project Status

**Completed:**
- Full event lifecycle management with venue conflict detection
- QR-based digital ticketing and check-in with attendance tracking
- Vendor, venue, resource, and sponsor management
- Budget tracking with approval workflows
- CSV/Excel/PDF reporting
- AI-powered FAQ chatbot
- Light/Dark theme customizer

**Not yet implemented:**
- Background task processing (Celery/Redis) for scheduled email reminders
- Email notification delivery (currently in-app only)

---

## License

Built for educational purposes as part of the Infosys Springboard Training Program.
