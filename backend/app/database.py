import os
import logging
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv

# Load environment variables from backend/.env if present
load_dotenv()

logger = logging.getLogger("cognitive_metrics.database")

raw_db_url = os.getenv("DATABASE_URL", "").strip()

# Normalize PostgreSQL URL for SQLAlchemy / psycopg2
# Neon often provides strings starting with postgres:// or postgresql://
if raw_db_url:
    if raw_db_url.startswith("postgres://"):
        DATABASE_URL = raw_db_url.replace("postgres://", "postgresql://", 1)
    else:
        DATABASE_URL = raw_db_url
    
    # Ensure sslmode=require for Neon if not already specified
    if "neon.tech" in DATABASE_URL and "sslmode" not in DATABASE_URL:
        separator = "&" if "?" in DATABASE_URL else "?"
        DATABASE_URL = f"{DATABASE_URL}{separator}sslmode=require"
        
    engine_kwargs = {
        "pool_pre_ping": True,     # Automatically reconnect dropped serverless connections
        "pool_recycle": 300,       # Recycle connections every 5 mins for Neon sleep cycles
        "pool_size": 10,
        "max_overflow": 20,
    }
    logger.info("Using configured Neon PostgreSQL database.")
else:
    # Graceful local fallback if DATABASE_URL is not yet provided in .env
    DATABASE_URL = "sqlite:///./cognitive_metrics.db"
    engine_kwargs = {"connect_args": {"check_same_thread": False}}
    logger.warning("DATABASE_URL not set in backend/.env. Using local SQLite fallback for development.")

engine = create_engine(DATABASE_URL, **engine_kwargs)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    """FastAPI dependency for yielding database sessions."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
