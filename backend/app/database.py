import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

# Create SQLAlchemy engine (connects Python to PostgreSQL)
engine = create_engine(DATABASE_URL, echo=True)

# Session maker -each request gets its own DB session
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

# Base class
Base = declarative_base()


# Dependency for FastAPI
def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()
