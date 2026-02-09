"""
SQLite database connection and session management.
"""
import os
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from sqlmodel import SQLModel, create_engine

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./job_aggregator.db")

# Use check_same_thread=False for SQLite to allow multi-threaded access (needed for scrapers)
engine = create_engine(
    DATABASE_URL,
    echo=False,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def init_db():
    """Create all tables."""
    SQLModel.metadata.create_all(engine)


def get_db_session():
    """Dependency for getting a DB session."""
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()
