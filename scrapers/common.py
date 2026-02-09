"""
Common utilities for scrapers.
"""
import re
import hashlib
from datetime import datetime, timedelta, timezone
from typing import Optional
from utils.logger import get_logger

logger = get_logger(__name__)


def make_job_code(source: str, apply_url: str) -> str:
    """Generate stable unique job code from source + URL hash."""
    try:
        url_hash = hashlib.md5(apply_url.encode()).hexdigest()[:8]
        return f"{source}_{url_hash}".lower()
    except Exception as e:
        logger.error(f"Job code generation error: {e}")
        return f"{source}_{hash(apply_url)}".lower()


def parse_iso_date(date_str: Optional[str]) -> Optional[str]:
    """Parse various date formats into ISO 8601 string."""
    if not date_str:
        return None

    try:
        # Try ISO format first
        dt = datetime.fromisoformat(date_str.replace("Z", "+00:00"))
        return dt.isoformat()
    except Exception:
        pass

    try:
        # Try common formats
        formats = [
            "%Y-%m-%d",
            "%Y-%m-%dT%H:%M:%S",
            "%Y-%m-%d %H:%M:%S",
            "%d-%m-%Y",
            "%d/%m/%Y",
            "%B %d, %Y",
            "%b %d, %Y",
        ]
        for fmt in formats:
            try:
                dt = datetime.strptime(date_str.strip(), fmt)
                dt = dt.replace(tzinfo=timezone.utc)
                return dt.isoformat()
            except ValueError:
                continue
    except Exception:
        pass

    logger.debug(f"Could not parse date: {date_str}")
    return None


def relative_time(iso_date: Optional[str]) -> Optional[str]:
    """Convert ISO date to relative format (e.g., '2 days ago')."""
    if not iso_date:
        return None

    try:
        dt = datetime.fromisoformat(iso_date.replace("Z", "+00:00"))
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)

        now = datetime.now(timezone.utc)
        delta = now - dt

        seconds = delta.total_seconds()
        minutes = seconds / 60
        hours = minutes / 60
        days = hours / 24

        if seconds < 60:
            return f"{int(seconds)} seconds ago"
        elif minutes < 60:
            return f"{int(minutes)} minutes ago"
        elif hours < 24:
            return f"{int(hours)} hours ago"
        elif days < 7:
            return f"{int(days)} days ago"
        elif days < 30:
            weeks = int(days / 7)
            return f"{weeks} week{'s' if weeks > 1 else ''} ago"
        else:
            months = int(days / 30)
            return f"{months} month{'s' if months > 1 else ''} ago"

    except Exception as e:
        logger.error(f"Relative time conversion error: {e}")
        return None


def clean_text(text: Optional[str]) -> str:
    """Clean HTML, extra whitespace, garbage from text."""
    if not text:
        return ""

    # Remove HTML tags
    text = re.sub(r"<[^>]+>", " ", text)
    # Remove extra whitespace
    text = re.sub(r"\s+", " ", text)
    # Remove special chars but keep basic punctuation
    text = re.sub(r"[^\w\s\-.,!?:;'\"]", "", text)
    return text.strip()


def freshness_score(iso_date: Optional[str]) -> int:
    """
    Calculate freshness score (0-100).
    100: posted in last 24h
    ~70: 1 week old
    ~30: 1 month old
    """
    if not iso_date:
        return 10

    try:
        dt = datetime.fromisoformat(iso_date.replace("Z", "+00:00"))
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)

        now = datetime.now(timezone.utc)
        days = max(0.0, (now - dt).total_seconds() / 86400.0)

        if days <= 1:
            return 100
        elif days <= 7:
            return int(100 - (days - 1) * 5)
        elif days <= 30:
            return int(70 - (days - 7) * 1.7)
        else:
            return max(0, int(30 - (days - 30) * 0.5))

    except Exception as e:
        logger.error(f"Freshness score error: {e}")
        return 10
