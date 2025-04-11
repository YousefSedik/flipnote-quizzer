import os
from dotenv import load_dotenv

load_dotenv()
DEBUG = True
CSRF_TRUSTED_ORIGINS = [
    "http://localhost:8080",
]
CORS_ALLOWED_ORIGINS = [
    "http://localhost:8080",
]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.getenv("DB_NAME"),
        "USER": os.getenv("DB_USER"),
        "PASSWORD": os.getenv("DB_PASSWORD"),
        "HOST": os.getenv("DB_HOST"),
        "PORT": os.getenv("DB_PORT"),
    }
}
