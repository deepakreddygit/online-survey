import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = 'your_secret_key'
    DATABASE = os.path.join(BASE_DIR, 'site.db')  # SQLite for development
    # Uncomment below for PostgreSQL
    # DATABASE = "postgresql://username:password@localhost/your_database"
