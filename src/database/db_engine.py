from sqlalchemy import create_engine
from src.config import settings

DATABASE_URL = settings.FORMAT_DATABASE_URL

db_engine = create_engine(
    DATABASE_URL,
    pool_size=10,
    max_overflow=20,
    pool_timeout=30,
    pool_recycle=1800
)