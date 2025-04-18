import dotenv
import os

dotenv.load_dotenv()

ENVIRONMENT = os.getenv("ENVIRONMENT", "production").strip().lower()
if ENVIRONMENT == "production":
    from .production import *
elif ENVIRONMENT == "development":
    from .development import *
