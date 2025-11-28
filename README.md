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
* Users rate projects using multiple scoring criteria.
* Encourages detailed feedback and fair evaluation.

### 📊 Score Calculation
* Aggregates all weighted scores.
* Outputs:
  * **Best in Category**
  * **Overall Top Project**

### 🚀 Performance & Background Tasks
* **Redis Caching:** The "Top Projects" leaderboard is cached for 5 minutes to ensure instant load times.
* **Asynchronous Emails:** Rating a project triggers a background email notification via **Celery**, preventing UI freeze.
* **Scheduled Cleanup:** **Celery Beat** runs a nightly job (at 00:00) to clean up old or stale data.

### 💬 Feedback & Comments
* Students can leave comments explaining their score.

### 🛠 Admin Dashboard
Admins can manage Projects, Criteria, Users, Ratings, and Comments.

---

## 🏗 Architecture & Tech Stack

This project uses a robust, containerized architecture to handle high concurrency and background processing.

* **Backend Framework:** Django (Python 3.11)
* **API:** Django Rest Framework (DRF)
* **Database:** PostgreSQL
* **Cache & Message Broker:** Redis (Dockerized)
* **Task Queue:** Celery (Dockerized)
* **Scheduler:** Celery Beat (Dockerized)
* **Environment:** VS Code (Git Bash on Windows)

### 🐳 Docker Configuration
The project uses `docker-compose` to orchestrate services locally:
* **Redis Service:** Handles caching and message brokering on port `6379`.
* **Celery Worker:** Consumes tasks from Redis to send emails.
* **Celery Beat:** Schedules periodic maintenance tasks.

---

## ☁️ Deployment Configuration (Render)

To optimize for Cloud Free Tiers (specifically Render.com), this project uses custom shell scripts to bundle services.

### 📜 `build.sh` (The Build Command)
Runs automatically during the deployment phase. It prepares the environment by:
1. Installing Python dependencies (`pip install`).
2. Collecting static files (`collectstatic`) for WhiteNoise serving.
3. Applying database migrations (`migrate`).

### 📜 `start.sh` (The Entrypoint)
A custom script that overcomes the "Single Service" limitation of free tiers. It runs three processes concurrently in a single container:
1. **Celery Worker:** Starts the background task processor.
2. **Celery Beat:** Starts the periodic task scheduler.
3. **Gunicorn:** Starts the Django web server (bound to `$PORT`).

---

## 🚧 Challenges & Solutions

Building this advanced architecture came with significant technical hurdles. Here is how they were resolved:

### 1. The Python 3.14 Compatibility Issue
* **Challenge:** Initially started with Python 3.14 (Experimental). The `kombu` library (used by Celery) failed to establish network connections on Windows due to threading changes in this pre-release version, causing `WinError 10061`.
* **Solution:** Downgraded the environment to **Python 3.11 (Stable)**. This instantly resolved the socket connection issues and stabilized the Django-Redis link.

### 2. Windows & Docker Networking
* **Challenge:** Django running locally on Windows could not talk to Redis running inside Docker.
* **Solution:**
  * Configured `docker-compose.yaml` to explicitly forward ports (`6379:6379`).
  * Updated `settings.py` to use `127.0.0.1` instead of `localhost` to avoid IPv6 resolution conflicts.

### 3. API Versioning & Testing
* **Challenge:** Implementing API versioning (`/api/v1/`) broke existing unit tests that relied on old URL paths.
* **Solution:** Refactored the test suite to use updated paths and adapted assertions to handle the new **Pagination** format.

---

## 🗂 ERD (Entity Relationship Diagram)

```text
1. THE VOTER                  2. THE SCORE CARD
+------------------+           +-------------------+
|      USER        |           |     CRITERIA      |
+------------------+           +-------------------+
| PK user_id       |           | PK criteria_id    |
| username         |           | name              |
| password         |           | (e.g. Design)     |
+--------+---------+           +---------+---------+
         |                               |
         | 1 user gives                  | 1 criteria is used
         | many ratings                  | in many ratings
         |                               |
         v                               v
  +-------------------------------------------+
  |                RATING                     |
  |         (The "Pivot" Table)               |
  +-------------------------------------------+
  | PK rating_id                              |
  | FK user_id      (Who voted?)              |
  | FK project_id   (For what app?)           |
  | FK criteria_id  (On what basis?)          |
  | score           (e.g., 8/10)              |
  +----------------------+--------------------+
                         ^
                         |
                         | 1 project gets
                         | many ratings
                         |
                  +-------+-------+
                  |    PROJECT    |
                  +---------------+
                  | PK project_id |
                  | name          |
                  | description   |
                  +-------+-------+
                          ^
                          |
                          |
                  +-------+-------+
                  |    COMMENT    |
                  +---------------+
                  | PK comment_id |
                  | FK user_id    |
                  | FK project_id |
                  | content       |
                  +---------------+

📁 Project Structure


project-nexus-backend/
├── env/                 (Virtual Environment - Python 3.11)
├── core/                (Main App Logic & ViewSets)
├── polling_system/      (Django Project Settings)
├── docker-compose.yaml  (Docker Services Config)
├── Dockerfile           (Container Build Instructions)
├── build.sh             (Render Build Script)
├── start.sh             (Render Start Script - Bundles Gunicorn & Celery)
├── manage.py            (Django CLI Utility)
├── requirements.txt     (Dependencies)
└── README.md            (This file)

docker compose up

3. Backend Setup (Django)
Open a new terminal:

# Activate virtual environment
source env/Scripts/activate

# Install dependencies
pip install -r requirements.txt

# Run Migrations
python manage.py migrate

# Create Superuser
python manage.py createsuperuser

# Start Server
python manage.py runserver

This is a great addition. Documenting your deployment scripts shows that you understand DevOps and how to manage production environments on a budget.I have added a new section called ☁️ Deployment Configuration to the README. It clearly explains why you have these scripts (handling the Free Tier limitation).Here is the final, complete README. You can overwrite your file with this:Markdown# Project Nexus Backend 🐍

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
* Users rate projects using multiple scoring criteria.
* Encourages detailed feedback and fair evaluation.

### 📊 Score Calculation
* Aggregates all weighted scores.
* Outputs:
  * **Best in Category**
  * **Overall Top Project**

### 🚀 Performance & Background Tasks
* **Redis Caching:** The "Top Projects" leaderboard is cached for 5 minutes to ensure instant load times.
* **Asynchronous Emails:** Rating a project triggers a background email notification via **Celery**, preventing UI freeze.
* **Scheduled Cleanup:** **Celery Beat** runs a nightly job (at 00:00) to clean up old or stale data.

### 💬 Feedback & Comments
* Students can leave comments explaining their score.

### 🛠 Admin Dashboard
Admins can manage Projects, Criteria, Users, Ratings, and Comments.

---

## 🏗 Architecture & Tech Stack

This project uses a robust, containerized architecture to handle high concurrency and background processing.

* **Backend Framework:** Django (Python 3.11)
* **API:** Django Rest Framework (DRF)
* **Database:** PostgreSQL
* **Cache & Message Broker:** Redis (Dockerized)
* **Task Queue:** Celery (Dockerized)
* **Scheduler:** Celery Beat (Dockerized)
* **Environment:** VS Code (Git Bash on Windows)

### 🐳 Docker Configuration
The project uses `docker-compose` to orchestrate services locally:
* **Redis Service:** Handles caching and message brokering on port `6379`.
* **Celery Worker:** Consumes tasks from Redis to send emails.
* **Celery Beat:** Schedules periodic maintenance tasks.

---

## ☁️ Deployment Configuration (Render)

To optimize for Cloud Free Tiers (specifically Render.com), this project uses custom shell scripts to bundle services.

### 📜 `build.sh` (The Build Command)
Runs automatically during the deployment phase. It prepares the environment by:
1. Installing Python dependencies (`pip install`).
2. Collecting static files (`collectstatic`) for WhiteNoise serving.
3. Applying database migrations (`migrate`).

### 📜 `start.sh` (The Entrypoint)
A custom script that overcomes the "Single Service" limitation of free tiers. It runs three processes concurrently in a single container:
1. **Celery Worker:** Starts the background task processor.
2. **Celery Beat:** Starts the periodic task scheduler.
3. **Gunicorn:** Starts the Django web server (bound to `$PORT`).

---

## 🚧 Challenges & Solutions

Building this advanced architecture came with significant technical hurdles. Here is how they were resolved:

### 1. The Python 3.14 Compatibility Issue
* **Challenge:** Initially started with Python 3.14 (Experimental). The `kombu` library (used by Celery) failed to establish network connections on Windows due to threading changes in this pre-release version, causing `WinError 10061`.
* **Solution:** Downgraded the environment to **Python 3.11 (Stable)**. This instantly resolved the socket connection issues and stabilized the Django-Redis link.

### 2. Windows & Docker Networking
* **Challenge:** Django running locally on Windows could not talk to Redis running inside Docker.
* **Solution:**
  * Configured `docker-compose.yaml` to explicitly forward ports (`6379:6379`).
  * Updated `settings.py` to use `127.0.0.1` instead of `localhost` to avoid IPv6 resolution conflicts.

### 3. API Versioning & Testing
* **Challenge:** Implementing API versioning (`/api/v1/`) broke existing unit tests that relied on old URL paths.
* **Solution:** Refactored the test suite to use updated paths and adapted assertions to handle the new **Pagination** format.

---

## 🗂 ERD (Entity Relationship Diagram)

```text
1. THE VOTER                  2. THE SCORE CARD
+------------------+           +-------------------+
|      USER        |           |     CRITERIA      |
+------------------+           +-------------------+
| PK user_id       |           | PK criteria_id    |
| username         |           | name              |
| password         |           | (e.g. Design)     |
+--------+---------+           +---------+---------+
         |                               |
         | 1 user gives                  | 1 criteria is used
         | many ratings                  | in many ratings
         |                               |
         v                               v
  +-------------------------------------------+
  |                RATING                     |
  |         (The "Pivot" Table)               |
  +-------------------------------------------+
  | PK rating_id                              |
  | FK user_id      (Who voted?)              |
  | FK project_id   (For what app?)           |
  | FK criteria_id  (On what basis?)          |
  | score           (e.g., 8/10)              |
  +----------------------+--------------------+
                         ^
                         |
                         | 1 project gets
                         | many ratings
                         |
                  +-------+-------+
                  |    PROJECT    |
                  +---------------+
                  | PK project_id |
                  | name          |
                  | description   |
                  +-------+-------+
                          ^
                          |
                          |
                  +-------+-------+
                  |    COMMENT    |
                  +---------------+
                  | PK comment_id |
                  | FK user_id    |
                  | FK project_id |
                  | content       |
                  +---------------+
📁 Project StructurePlaintextproject-nexus-backend/
├── env/                 (Virtual Environment - Python 3.11)
├── core/                (Main App Logic & ViewSets)
├── polling_system/      (Django Project Settings)
├── docker-compose.yaml  (Docker Services Config)
├── Dockerfile           (Container Build Instructions)
├── build.sh             (Render Build Script)
├── start.sh             (Render Start Script - Bundles Gunicorn & Celery)
├── manage.py            (Django CLI Utility)
├── requirements.txt     (Dependencies)
└── README.md            (This file)
🚀 Installation & Setup1. PrerequisitesPython 3.11Docker Desktop (Running)2. Infrastructure Setup (Docker)Start Redis and Celery containers:Bashdocker compose up
3. Backend Setup (Django)Open a new terminal:Bash# Activate virtual environment
source env/Scripts/activate

# Install dependencies
pip install -r requirements.txt

# Run Migrations
python manage.py migrate

# Create Superuser
python manage.py createsuperuser

# Start Server
python manage.py runserver
🧪 API EndpointsThese endpoints have been tested and verified.Base URL: http://127.0.0.1:8000/apiMethodEndpointDescriptionPOST/auth/jwt/create/Login: Obtain JWT Access & Refresh tokens.GET/v1/projects/List Projects: Get a paginated list of all projects.POST/v1/projects/Create Project: Add a new project to the database.POST/v1/projects/{id}/ratings/Rate Project: Submit a score (triggers Celery email task).POST/v1/projects/{id}/comments/Comment: Add feedback to a specific project.GET/v1/projects/top/Leaderboard: Get cached list of top-rated projects.