"""
SQLModel database schemas for Job Aggregator Portal.
"""
from datetime import datetime
from typing import Optional
from sqlmodel import SQLModel, Field, Column, String


class JobBase(SQLModel):
    """Base job schema."""
    job_code: str = Field(unique=True, index=True)  # source_hash(url)
    title: str
    company: str
    location: str
    is_remote: bool = False
    posted_at_iso: Optional[str] = None  # ISO timestamp
    posted_at_human: Optional[str] = None  # "2 days ago"
    source_name: str
    apply_url: str
    description_text: str = Field(sa_column=Column(String, nullable=True))
    tags: Optional[str] = None  # JSON list of skills
    source_fetch_time: datetime = Field(default_factory=datetime.utcnow)
    cached: bool = False


class Job(JobBase, table=True):
    """Job table."""
    __tablename__ = "jobs"
    id: Optional[int] = Field(default=None, primary_key=True)


class UserBase(SQLModel):
    """Base user schema."""
    email: str = Field(unique=True, index=True)
    full_name: str
    is_active: bool = True


class User(UserBase, table=True):
    """User table."""
    __tablename__ = "users"
    id: Optional[int] = Field(default=None, primary_key=True)
    hashed_password: str
    created_at: datetime = Field(default_factory=datetime.utcnow)


class ResumeBase(SQLModel):
    """Base resume schema."""
    user_id: int = Field(foreign_key="users.id")
    original_text: str
    parsed_name: str
    parsed_email: str
    parsed_phone: str


class Resume(ResumeBase, table=True):
    """Resume table."""
    __tablename__ = "resumes"
    id: Optional[int] = Field(default=None, primary_key=True)
    uploaded_at: datetime = Field(default_factory=datetime.utcnow)


class CacheBase(SQLModel):
    """Base cache schema."""
    cache_key: str = Field(unique=True, index=True)
    cache_value: str  # JSON string
    expires_at: datetime


class Cache(CacheBase, table=True):
    """Cache table."""
    __tablename__ = "cache"
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
