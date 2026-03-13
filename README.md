# Broadcast Company Engineering Team Registry
## 5COSC021W – Software Development Group Project

A Django web application for discovering and managing engineering teams at Broadcast Company.

---

## Quick Start (3 commands)

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Set up database & seed sample data
python manage.py migrate
python manage.py seed_data

# 3. Run the server
python manage.py runserver
```

Then open **http://127.0.0.1:8000**

---

## Login Credentials

| Role  | Username         | Password     |
|-------|-----------------|--------------|
| Admin | `admin`          | `admin123`   |
| User  | `alice.johnson`  | `password123`|
| User  | `bob.smith`      | `password123`|

**Admin panel:** http://127.0.0.1:8000/admin/

---

## Project Structure

```
broadcast_registry/
├── broadcast_registry/       # Django project settings
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── teams/                    # Core teams app
│   ├── models.py             # Department, Team, TeamMember, Repository, AuditLog
│   ├── views.py              # All team/dept/org-chart views
│   ├── forms.py
│   ├── admin.py              # Django admin config
│   ├── urls.py
│   └── management/commands/seed_data.py
├── users/                    # Auth app
│   ├── models.py             # CustomUser model
│   ├── views.py              # Register, login, profile, change password
│   ├── forms.py
│   └── urls.py
├── templates/
│   ├── base.html             # Shared layout with navbar & sidebar
│   ├── teams/                # All team templates
│   └── users/                # Auth templates
├── static/                   # CSS / JS assets
├── manage.py
└── requirements.txt
```

---

## Features Implemented

### User Authentication
- Self-registration (local accounts only)
- Secure login / logout
- Profile update (name, email, bio)
- Password change
- Session management

### Team Management
- Create / edit / disband teams
- Grid and list view modes
- Search by name, description, department, manager
- Filter by department and status
- Member management (add / remove)
- Code repository links

### Department Management
- Create and edit departments
- Department overview with team counts

### Organisation Chart
- Interactive D3.js force-directed graph
- Filter by department
- Zoom and pan
- Click nodes to navigate to team page
- Upstream/downstream dependency arrows

### Audit Trail
- Every create/update/delete logged with timestamp, user, IP

### Django Admin Panel
- Full CRUD for all models
- Inline member and repository editing
- Audit log (read-only)

---

## Sample Data (seeded)

**3 Departments:**
- Streaming Platform (CDN & Delivery, Video Encoding, Player & Playback)
- Data & Analytics (Data Pipelines, Business Intelligence, ML & Recommendations)
- Mobile & Web (iOS App, Android App, Web Frontend)

**9 Teams** — each with ≥5 engineers, a manager, Slack channel, email, and code repos

**Team dependencies:**
- Player & Playback → depends on CDN & Delivery + Video Encoding
- iOS / Android / Web → each depend on Player & Playback
- BI + ML → both depend on Data Pipelines

---

## Individual Task Allocation (Group of 5 suggested split)

| Member | Feature Area |
|--------|-------------|
| 1 | Team CRUD + Search |
| 2 | Department Management + Org Chart |
| 3 | User Auth (Register/Login/Profile) |
| 4 | Audit Log + Admin panel customisation |
| 5 | Member management + Repository links |

---

## Tech Stack

- **Backend:** Python 3.x + Django 4.2
- **Database:** SQLite (db.sqlite3)
- **Frontend:** Bootstrap 5.3 + Bootstrap Icons + D3.js v7
- **Auth:** Django built-in auth + custom user model
