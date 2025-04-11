from dotenv import load_dotenv
import os

load_dotenv()

DEBUG = False

CORS_ALLOWED_ORIGINS = [
    "https://flipnote-quizzer-pro.lovable.app/",
]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.getenv("DB_NAME"),
        "USER": os.getenv("DB_USER"),
        "PASSWORD": os.getenv("DB_PASSWORD"),
        "HOST": os.getenv("DB_HOST"),
        "PORT": os.getenv("DB_PORT"),
        "OPTIONS": {"sslmode": "require"},
    }
}
