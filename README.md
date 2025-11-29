# Project Nexus Backend 🐍

## 📌 About Project Nexus

Project Nexus is a backend evaluation and voting system designed for **ALX students** to vote for the best peer projects. It promotes **fair and transparent judging** using a **criteria-based weighted rating system** instead of simple likes.

It supports judging for:

* Online Polling Systems
* Movie Recommendation Apps
* E-commerce Catalogues
* Job Platforms
* Social Media Feed Apps

The system evaluates projects using metrics such as **Innovation**, **Design**, **Code Quality**, and **UI/UX**.

---

## ✨ Features

### 🔐 User Management

* Student authentication (JWT-based).
* Secure voting (1 user = 1 vote per project per criteria).

### 📚 Project Repository

Stores all student-submitted apps, such as:

* "Social Media Feed"
* "Job Platform"
* "Movie Recommendation App"

### 🗳 Criteria-Based Voting

* Multi-criteria scoring.
* Detailed feedback supported.

### 📊 Score Calculation

* Weighted score aggregation.
* Determines:

  * **Top Project Overall**
  * **Top Project per Category**

### 🚀 Performance & Background Tasks

* **Redis Caching** for fast leaderboard loading.
* **Celery Worker** for asynchronous tasks.
* **Celery Beat** scheduled tasks (nightly cleanup).
* **Email notifications** triggered when a rating is submitted.

### 💬 Feedback & Comments

Students can comment on each project.

### 🛠 Admin Dashboard

Manage Projects, Criteria, Users, Comments, and Ratings.

---

## 🏗 Architecture & Tech Stack

* **Backend:** Django (Python 3.11)
* **API Layer:** Django REST Framework
* **Database:** PostgreSQL
* **Cache & Message Queue:** Redis
* **Background Tasks:** Celery + Celery Beat
* **Containers:** Docker / Docker Compose
* **Editor:** VS Code (Git Bash on Windows)

### 🐳 Docker Services

* **Redis** → caching + message queue
* **Celery Worker** → async tasks
* **Celery Beat** → scheduled tasks

---

## ☁️ Deployment Configuration (Render)

### 📜 `build.sh`

Executes during Render Build Phase:

1. Install dependencies
2. Collect static files
3. Apply database migrations

### 📜 `start.sh`

Handles multi-process execution inside a **single Render dyno**:

* Celery Worker
* Celery Beat
* Gunicorn (Django server)

---

## 🚧 Challenges & Solutions

### 🐍 Python 3.14 Issue

* Python 3.14 broke Celery/Kombu on Windows.
* **Solution:** Switched to Python **3.11**.

### 🐳 Docker Networking on Windows

* Redis in Docker couldn't talk to Django.
* **Solution:** Exposed correct ports + switched to `127.0.0.1`.

### 🔄 API Versioning Broke Tests

* Moving to `/api/v1/` required updating test URLs.
* **Solution:** Updated tests and adapted to DRF Pagination.

---

## 🗂 ERD (Entity Relationship Diagram)

```
USER 1---∞ RATING ∞---1 PROJECT
          |
          ∞
       CRITERIA
```

Comments also link to Users and Projects.

---

## 📁 Project Structure

```
project-nexus-backend/
├── env/                 
├── core/                # Main App Logic + TESTS DIRECTORY
│   ├── viewsets.py
│   ├── models.py
│   └── tests/           # <── All test cases are stored here
│        ├── test_auth.py
│        ├── test_project.py
│        ├── test_rating.py
│        ├── test_rating_unique.py
│        └── test_top_project.py
├── polling_system/
├── docker-compose.yaml
├── Dockerfile
├── build.sh
├── start.sh
├── manage.py
└── README.md
```

---

# 🧪 Testing

All automated tests for this project are located inside the **`core/tests/`** directory.

Example from your environment (matching screenshot):

```
core/
└── tests/
     ├── test_auth.py
     ├── test_project.py
     ├── test_rating.py
     ├── test_rating_unique.py
     └── test_top_project.py
```

### ✔️ Running Tests

Use Django’s built-in test runner:

```bash
python manage.py test core
```

### ✔️ Example Output (Your Environment)

```
Found 5 test(s).
Creating test database for alias 'default'...
System check identified no issues (0 silenced).
.....
----------------------------------------------------------------------
Ran 5 tests in 22.371s

OK
Destroying test database for alias 'default'...
```

All tests passed successfully.

---

## 🧪 Test Coverage Setup (Optional)

To generate a coverage report:

```bash
pip install coverage
coverage run manage.py test core
coverage html
```

This will create an `/htmlcov` folder containing a graphical HTML coverage report.

---

# 🚀 Installation & Setup

### 1. Start Infrastructure (Redis + Celery)

```bash
docker compose up
```

### 2. Backend Setup

```bash
source env/Scripts/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

---

# 🧵 API Endpoints (Verified)

| Method | Endpoint                          | Description                            |
| ------ | --------------------------------- | -------------------------------------- |
| POST   | `/auth/jwt/create/`               | Obtain JWT tokens                      |
| GET    | `/api/v1/projects/`               | List all projects                      |
| POST   | `/api/v1/projects/`               | Create a project                       |
| POST   | `/api/v1/projects/{id}/ratings/`  | Rate a project (Triggers Celery email) |
| POST   | `/api/v1/projects/{id}/comments/` | Add feedback                           |
| GET    | `/api/v1/projects/top/`           | Cached leaderboard                     |

---


