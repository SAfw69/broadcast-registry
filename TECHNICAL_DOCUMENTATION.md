# Global Engineering Registry Portal - Technical Documentation
This document outlines the core functionality of the Broadcast Company Engineering Registry, summarizing what has been implemented in the codebase and how the application operates.

## 1. Overview
The **Broadcast Registry** is a fully functional web application designed to help organizations manage and visualize their engineering teams, departments, and technical dependencies. It offers user authentication, role-based access control, an interactive organization chart, and a comprehensive audit trail.

## 2. Core Functionality Implemented
The application is feature-complete and includes the following core functionalities:

### User Authentication & Role Management (`users` App)
- **Implemented:** Custom registration, secure login/logout, and profile management.
- **Code Details:** The `users/views.py` handles form processing for new users. It uses Django's built-in session management. 
- **Roles:** The system distinguishes between standard users and Administrators (staff members who have access to the Django Admin panel).

### Team and Department Management (`teams` App)
- **Implemented:** Full CRUD (Create, Read, Update, Delete) capabilities for Teams and Departments.
- **Code Details:** 
  - `teams/models.py` defines the database schema for `Department`, `Team`, `TeamMember`, and `Repository`. 
  - `teams/views.py` contains the logic to handle form submissions, filter teams by department, and search based on keywords.

### Interactive Organization Chart
- **Implemented:** A visual representation of team dependencies.
- **Code Details:** The backend (`teams/views.py`) serializes the relationship data into JSON format. The frontend (`org_chart.html`) uses **D3.js** to render a force-directed graph. Users can drag nodes to explore upstream and downstream dependencies dynamically.

### Automated Audit Logging
- **Implemented:** Every action (creating a team, updating a department, adding a member) is tracked for security and accountability.
- **Code Details:** Whenever a `Team` or `Department` model is modified in `teams/views.py`, an `AuditLog` entry is automatically generated. The logs track the user who made the change, the action type, the exact timestamp, and the user's IP address.

## 3. Code Architecture & Design System
The project follows a standard modular Django architecture (Backend) paired with a highly customized HTML/CSS styling approach (Frontend).

### Backend (`Python / Django`)
- **Database:** SQLite (`db.sqlite3`) is used for persistent data storage.
- **Data Seeding:** A custom management command (`teams/management/commands/seed_data.py`) allows developers to instantly populate the database with dummy departments, teams, users, and dependencies for testing purposes.

### Frontend (`HTML / CSS / Bootstrap`)
The UI relies on **Bootstrap 5.3** for its grid system, but the visual aesthetic is completely custom-built in `templates/base.html`:
- **Glassmorphism:** The sidebar and cards use a frosted glass effect (`backdrop-filter: blur(12px)`) over an animated gradient background.
- **Animations:** Custom CSS keyframes ensure elements slide and fade into view smoothly.
- **Scroll Detection:** A JavaScript `IntersectionObserver` cascades lists and tables into view as the user scrolls down the page, providing a premium feel.

## 4. Current Status
The codebase has been completely reviewed and tested. **There are currently no missing features, bugs, or incomplete sections (TODOs) in the logic.** All forms save correctly, the authentication workflow is secure, and the data visualization (Org Chart) renders perfectly.
