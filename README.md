# AttendEase - Attendance Management System

AttendEase is a simple web-based attendance management system built using Django. It allows faculty members to record student attendance, review previous attendance sessions, correct attendance records, and identify students whose attendance falls below 75%.

The project was developed as a practical solution for managing attendance in an educational environment while keeping the workflow simple and easy to use.

## Features

- User authentication with login and logout
- Faculty-based attendance management
- Record attendance as Present or Absent
- Subject and section-based attendance
- View previous attendance sessions
- View individual attendance records for a session
- Correct previously recorded attendance
- Prevent duplicate attendance sessions for the same subject, section, and date
- Calculate subject-wise attendance percentage
- Identify students with attendance below 75%
- Simple dashboard showing students, subjects, and attendance sessions

## Tech Stack

### Backend
- Python
- Django

### Frontend
- HTML
- CSS
- Django Template Language

### Database
- SQLite

### Tools
- Git
- GitHub
- VS Code

## Project Structure

```text
attendease/
│
├── attendance/
│   ├── migrations/
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── urls.py
│   └── views.py
│
├── templates/
│   └── attendance/
│       ├── base.html
│       ├── home.html
│       ├── login.html
│       ├── dashboard.html
│       ├── mark_attendance.html
│       ├── history.html
│       ├── session_detail.html
│       ├── edit_attendance.html
│       └── low_attendance.html
│
├── manage.py
├── requirements.txt
└── README.md
```

## Main Modules

### Student

Stores information related to students, including the associated Django user, roll number, department, and section.

### Faculty

Stores faculty information and connects a faculty member with a Django user and department.

### Subject

Represents subjects handled by faculty members.

### Attendance Session

Represents one attendance session for a particular subject, faculty member, section, and date.

### Attendance Record

Stores the attendance status of an individual student for an attendance session.

Attendance status is stored as:

- `P` - Present
- `A` - Absent

## Application Workflow

### 1. Authentication

A user logs into the system using Django authentication.

Protected pages require authentication before they can be accessed.

### 2. Dashboard

After login, the dashboard displays basic information such as:

- Total students
- Total subjects
- Total attendance sessions

It also provides quick access to the major attendance operations.

### 3. Mark Attendance

A faculty member selects a subject and section.

Students are displayed with two attendance options:

- Present
- Absent

The selected attendance records are stored when the faculty member submits the form.

### 4. Attendance History

Previously created attendance sessions can be viewed from the Attendance History page.

Each session displays information such as:

- Date
- Subject
- Section
- Faculty
- Number of student records

### 5. Attendance Correction

Faculty members can open an attendance session and modify an incorrect attendance record.

For example:

```text
Present -> Absent
```

or:

```text
Absent -> Present
```

The corrected value is then saved to the database.

### 6. Low Attendance Report

The application calculates attendance percentage using:

```text
Attendance Percentage =
(Present Classes / Total Classes) * 100
```

If a student's subject-wise attendance is below 75%, the student is displayed in the Low Attendance Report.

## Validation and Edge Cases

The application includes basic validation for common attendance-management problems.

### Authentication

Attendance pages require the user to be logged in.

### Faculty Authorization

Only users associated with a Faculty record can mark attendance.

### Subject Ownership

A faculty member can mark attendance only for subjects assigned to them.

### Duplicate Attendance

The system checks whether attendance has already been recorded for the same:

- Subject
- Faculty
- Section
- Date

This prevents accidental duplicate attendance sessions.

### Attendance Correction Authorization

A faculty member cannot modify an attendance record belonging to another faculty member's session.

### Invalid Attendance Status

Only `P` and `A` are accepted as valid attendance statuses.

### No Classes Conducted

Subjects with no attendance records are skipped while calculating the low-attendance report, avoiding division by zero.

## Architecture

AttendEase follows Django's Model-View-Template architecture.

```text
Browser
   |
   v
Django URL
   |
   v
View
   |
   +----> Model ----> SQLite Database
   |
   v
Template
   |
   v
HTML Response
```

### Model

Handles application data and database relationships.

### View

Contains the application logic, validation, attendance calculations, and request handling.

### Template

Displays the user interface using HTML, CSS, and Django Template Language.

## Design Decisions

### Django

Django was selected because it provides built-in support for authentication, ORM, routing
