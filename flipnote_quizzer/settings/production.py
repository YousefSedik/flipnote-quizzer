from dotenv import load_dotenv
import os
from .base import *

load_dotenv()

DEBUG = False
CSRF_TRUSTED_ORIGINS = [
    "https://flipnote-quizzer-pro.lovable.app",
    "https://flipnote-quizzer-backend.azurewebsites.net",
]
CORS_ALLOWED_ORIGINS = [
    "https://flipnote-quizzer-pro.lovable.app",
]
MIDDLEWARE += [
    "whitenoise.middleware.WhiteNoiseMiddleware",
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
STATIC_ROOT = BASE_DIR / "staticfiles"
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
ALLOWED_HOSTS = [".azurewebsites.net"]
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"
