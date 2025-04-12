import dotenv
import os

dotenv.load_dotenv()

ENVIRONMENT = os.getenv("ENVIRONMENT", "").strip().lower()
if ENVIRONMENT == "production":
    from .production import *
elif ENVIRONMENT == "development":
    from .development import *
else:
    print("ensure that ENVIRONMENT is set to development OR production")
