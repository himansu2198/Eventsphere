# Event Registration Platform

A full-featured Django-based event management system built for college/campus events, developed as part of the Infosys Springboard Training Program.

## Features

### Core Event Management
- Event categories with images, priority, and status
- Full event lifecycle: create, edit, delete, status tracking, history log
- Venue conflict detection and registered venue management (capacity, amenities, availability)
- Registration deadlines and participant capacity limits, enforced at registration time

### Participant & Member Management
- Admin-manual and self-service participant registration
- Role assignment (Participant, VIP, Speaker, Sponsor, Volunteer, Organizer, Judge, etc.)
- Department and academic year tracking
- Editable registration status (Pending / Confirmed / Waitlisted / Cancelled)
- QR code ticket generation on registration
- Webcam-based QR check-in scanner with manual fallback
- Attendance tracking (present/absent)

### Vendor, Venue, Resource & Sponsor Management
- Vendor onboarding with contract document upload, contract dates, and status tracking
- Venue registry with capacity and amenities
- Resource/equipment inventory with allocation tracking and over-allocation prevention
- Sponsor directory with logo upload, contact info, and linkable sponsorship records

### Budget & Financial Tracking
- Event-level budget allocation
- Expense recording with invoice upload
- High-value expense approval workflow (₹10,000+ threshold)
- Sponsorship revenue tracking (pledged/received)
- Live budget utilization dashboard

### Contact & Reporting
- Public contact form with database-backed inquiry storage
- Admin review dashboard for inquiries
- CSV export for Events, Members, and Contact Messages

### Admin Dashboard
- Real-time stats (categories, events, participants, vendors, budget)
- Chart.js analytics (registrations by category)
- Auto-generated activity feed and insights
- Dark mode with persistent theme customizer (sidebar/navbar colors, layout options)
- Live notification system with AJAX polling badge

### Authentication
- Separate admin and participant roles
- Centered, validated login/signup pages
- Password change via Django's built-in auth forms

### REST API
- Django REST Framework endpoints for categories, events, members, and vendors

## Tech Stack

- **Backend:** Django 6.0, Django REST Framework
- **Database:** SQLite (development)
- **Frontend:** Bootstrap 5, Bootstrap Icons, Chart.js, vanilla JS
- **QR Codes:** `qrcode` (generation), `html5-qrcode` (scanning)

## Setup

1. Clone the repository
```bash
   git clone https://github.com/himansu2198/Eventsphere.git
   cd Eventsphere
```

2. Create and activate a virtual environment
```bash
   python -m venv env
   env\Scripts\activate      # Windows
```

3. Install dependencies
```bash
   pip install -r requirements.txt
```

4. Run migrations
```bash
   python manage.py makemigrations
   python manage.py migrate
```

5. Create a superuser (for admin access)
```bash
   python manage.py createsuperuser
```

6. Run the development server
```bash
   python manage.py runserver
```

7. Visit `http://127.0.0.1:8000/`

## Project Status

This project is under active development. Not yet implemented:
- Background task processing (Celery/Redis) for email notifications and scheduled reminders
- PDF export for reports
- Native Excel (.xlsx) export (currently CSV, which opens in Excel)

## License

Built for educational purposes as part of the Infosys Springboard Training Program.