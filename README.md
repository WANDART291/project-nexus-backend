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

* Student authentication (login & vote)
* Secure voting (1 user = 1 vote per project per criteria)

### 📚 Project Repository

Stores all student-submitted apps, such as:

* "Social Media Feed"
* "Job Platform"
* "Movie Recommendation App"

### 🗳 Criteria-Based Voting

* Users rate projects using multiple scoring criteria
* Encourages detailed feedback and fair evaluation

### 📊 Score Calculation

* Aggregates all weighted scores
* Outputs:

  * **Best in Category**
  * **Overall Top Project**

### 💬 Feedback & Comments

* Students can leave comments explaining their score

### 🛠 Admin Dashboard

Admins can manage:

* Projects
* Criteria
* Users
* Ratings
* Comments

---

## 🗂 ERD (Entity Relationship Diagram)

```
+-----------------------------------------------------------+
|                   PROJECT NEXUS ERD                       |
|               (Entity Relationship Diagram)               |
+-----------------------------------------------------------+

       1. THE VOTER                   2. THE SCORE CARD
    +------------------+            +-------------------+
    |      USER        |            |     CRITERIA      |
    +------------------+            +-------------------+
    | PK user_id       |            | PK criteria_id    |
    | username         |            | name              |
    | password         |            | (e.g. Design)     |
    +--------+---------+            +---------+---------+
             |                                |
             | 1 user gives                   | 1 criteria is used
             | many ratings                   | in many ratings
             |                                |
             v                                v
      +-------------------------------------------+
      |                 RATING                    |
      |          (The "Pivot" Table)              |
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
                     | text          |
                     +---------------+
```

---

## 🧰 Tech Stack

* **Backend:** Django
* **Database:** PostgreSQL
* **Environment:** VS Code (Git Bash)
* **Language:** Python

---

## 📁 Project Structure

```
project-nexus-backend/
├── env/                 (Virtual Environment)
├── core/                (Django Project Settings)
├── polling_system/      (Main App: Models, Views, Admin)
├── manage.py            (Django CLI Utility)
├── requirements.txt     (Dependencies)
└── README.md            (This file)
```

---

## 🚀 Installation (Beginner Friendly)

### 1. Navigate to your project folder

```
cd project-nexus-backend
```

### 2. Create and activate the virtual environment

```
python -m venv env
source env/Scripts/activate
```

### 3. Create a `.env` file

```
SECRET_KEY=your-secret-key-goes-here
DATABASE_URL=postgres://user:password@localhost:5432/project_nexusdb
```

### 4. Install dependencies

```
pip install -r requirements.txt
```

### 5. Run migrations

```
python manage.py makemigrations
python manage.py migrate
```

### 6. Create a Superuser

```
python manage.py createsuperuser
```

### 7. Start the development server

```
python manage.py runserver
```

---

## 🧪 API Endpoints (Coming Soon)

Future endpoints will include:

* **POST /api/login/** – Authenticate users
* **POST /api/projects/** – Add new project
* **GET /api/projects/** – List projects
* **POST /api/rate/** – Submit ratings
* **POST /api/comment/** – Add comments

---

## 🧠 Usage Instructions

### 🛠 Admin Panel

Access it at:

```
http://127.0.0.1:8000/admin/
```

Use your superuser credentials.

### Setup Data

1. Add **Criteria** (e.g., Innovation, UI/UX, Design)
2. Add **Projects**
3. Students submit ratings & comments

---

## 🤝 Collaboration & Contributions

This project is part of the **ALX Backend Curriculum**.
Contributions are welcome through:

* Pull Requests
* Issue Reporting
* Feature Suggestions

---

## 📝 License

This project is for educational purposes under ALX.

---

## 🙌 Acknowledgements

Thanks to the **ALX Backend Engineering Program** for guidance and hands-on architecture practices.
