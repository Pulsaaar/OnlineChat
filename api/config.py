from dotenv import load_dotenv
import os

load_dotenv()

DB_HOST = os.environ.get("DB_HOST")
DB_PORT = os.environ.get("DB_PORT")
DB_USER = os.environ.get("DB_USER")
DB_PASS = os.environ.get("DB_PASS")
DB_NAME = os.environ.get("DB_NAME")
AUTH_SECRET = os.environ.get("AUTH_SECRET")
VER_SECRET = os.environ.get("VER_SECRET")
API_TOKEN = os.environ.get("API_TOKEN")
REDIS_URL = os.environ.get("REDIS_URL")