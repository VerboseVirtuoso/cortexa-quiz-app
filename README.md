# Cortexa – Dynamic Quiz Web Application

Cortexa is a dynamic quiz web application built using Django.  
It allows users to create, manage, and attempt quizzes with automatic scoring and user authentication.

---

## 🚀 Features

- User Registration & Login System
- Create, Update, Delete Quizzes (Full CRUD)
- Add Multiple Questions with Multiple Options
- Automatic Score Calculation
- User Dashboard
- Role-based Access (Only quiz creators can edit/delete)
- Responsive and modern UI

---

## 🛠 Tech Stack

- Backend: Django (Python)
- Frontend: HTML, CSS
- Database: SQLite (Development)
- Authentication: Django Built-in Auth System

---

## 📂 Project Structure

```
config/        → Django project configuration
quiz/          → Main quiz application
templates/     → HTML templates
static/        → CSS files
manage.py      → Django management file
```

---

## ⚙️ Installation & Setup (Local)

1. Clone the repository:
   ```
   git clone <repository-url>
   ```

2. Navigate into the project folder:
   ```
   cd project-folder
   ```

3. Create a virtual environment:
   ```
   python -m venv venv
   ```

4. Activate the environment:
   ```
   venv\Scripts\activate
   ```

5. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

6. Apply migrations:
   ```
   python manage.py migrate
   ```

7. Run the development server:
   ```
   python manage.py runserver
   ```

8. Open in browser:
   ```
   http://127.0.0.1:8000/
   ```

---

## 📌 Notes

- This project was developed as an academic submission.
- Future upgrades may include PostgreSQL support and production deployment.

---

## 👨‍💻 Author

Abhinav Vinod
Django Web Development Project – 2026

