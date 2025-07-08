# Flipnote Quizzer

Flipnote Quizzer is a Django-based web application for creating, managing, and sharing quizzes. It supports both multiple-choice and written-answer questions, user authentication, quiz history, and AI-powered question extraction from documents.

## Features
- User registration, login, and profile management (email-based authentication)
- Create, update, delete, and view quizzes
- Support for Multiple Choice and Written questions
- Public and private quizzes
- Quiz view tracking and history
- Extract questions from PDF or TXT files using Gemini AI
- RESTful API with JWT authentication
- API documentation via Swagger and Redoc
- Admin dashboard

## Tech Stack
- Python
- Django
- Django REST Framework
- Google Gemini API (for question extraction)
- PostgreSQL

## Getting Started

### Prerequisites
- Python 3.8+
- PostgreSQL

### Installation
1. **Clone the repository:**
   ```bash
   git clone https://github.com/YousefSedik/flipnote-quizzer
   cd flipnote-quizzer
   ```
2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
3. **Configure environment variables:**
   - Copy `env-example` to `.env` and fill in the required values:
     ```bash
     cp env-example .env
     ```
   - Set your `SECRET_KEY`, database credentials, email settings, and `GEMINI_API_KEY`.
4. **Apply migrations:**
   ```bash
   python manage.py migrate
   ```
5. **Create a superuser (admin):**
   ```bash
   python manage.py createsuperuser
   ```
6. **Run the development server:**
   ```bash
   python manage.py runserver
   ```

### Production
To run with Gunicorn and Uvicorn workers (see `startup.txt`):
```bash
gunicorn flipnote_quizzer.asgi:application --bind=0.0.0.0:$PORT --workers=4 --worker-class=uvicorn.workers.UvicornWorker --timeout=120 --log-level debug --access-logfile -
```

## API Overview

### Authentication
- `POST /auth/login/` — Obtain JWT token
- `POST /auth/register/` — Register new user
- `POST /auth/token/refresh/` — Refresh JWT token
- `POST /auth/token/verify/` — Verify JWT token
- `GET /auth/profile/` — Get user profile (auth required)

### Quizzes
- `GET /quizzes` — List your quizzes (auth required)
- `POST /quizzes` — Create a quiz (auth required)
- `GET /quizzes/public` — List public quizzes
- `GET /quizzes/<uuid:pk>` — Retrieve, update, or delete a quiz (auth required, owner only for update/delete)
- `GET /questions/<uuid:pk>` — Get all questions for a quiz
- `POST /quizzes/<uuid:pk>/questions` — Add a question to a quiz (auth required, owner only)
- `DELETE /quizzes/<uuid:pk>/questions/<int:question_id>/<str:qtype>` — Delete a question (auth required, owner only)
- `GET /quizzes/history` — Get your recently viewed quizzes
- `POST /extract-questions` — Extract questions from uploaded PDF/TXT or text (auth required)
- `GET /quiz/search` — Search quizzes

### API Documentation
- Swagger UI: `/api/schema/swagger-ui/`
- Redoc: `/api/schema/redoc/`

## Running Tests
To run the test suite:
```bash
python manage.py test
```

## License
MIT License 