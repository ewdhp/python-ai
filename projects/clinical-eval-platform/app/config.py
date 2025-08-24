import os
from dotenv import load_dotenv

load_dotenv()

DB_URL = os.getenv("DB_URL", "sqlite:///./test.db")
LANG_DEFAULT = os.getenv("LANG_DEFAULT", "en")
