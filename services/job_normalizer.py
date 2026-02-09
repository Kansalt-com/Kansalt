"""
Job data normalization and formatting utilities.
"""
from datetime import datetime, timezone
from typing import Optional, Dict, Any
from dateutil import parser as date_parser
from utils.logger import get_logger

logger = get_logger(__name__)


def format_time_ago(date_obj: Optional[Any]) -> str:
    """
    Convert a date to human-readable "time ago" format.
    
    Args:
        date_obj: datetime, string, or None
        
    Returns:
        String like "2 hours ago", "3 days ago", or "—" if date is invalid
    """
    if not date_obj:
        return "—"
    
    try:
        # Parse if string
        if isinstance(date_obj, str):
            dt = date_parser.parse(date_obj)
        elif isinstance(date_obj, datetime):
            dt = date_obj
        else:
            return "—"
        
        # Make timezone-aware if needed
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        
        now = datetime.now(timezone.utc)
        diff = now - dt
        
        seconds = diff.total_seconds()
        
        # Handle various time periods
        if seconds < 60:
            return "Just now"
        elif seconds < 3600:
            mins = int(seconds / 60)
            return f"{mins} min ago" if mins == 1 else f"{mins} mins ago"
        elif seconds < 86400:
            hours = int(seconds / 3600)
            return f"{hours} hour ago" if hours == 1 else f"{hours} hours ago"
        elif seconds < 604800:  # 7 days
            days = int(seconds / 86400)
            return f"{days} day ago" if days == 1 else f"{days} days ago"
        elif seconds < 2592000:  # 30 days
            weeks = int(seconds / 604800)
            return f"{weeks} week ago" if weeks == 1 else f"{weeks} weeks ago"
        elif seconds < 31536000:  # 365 days
            months = int(seconds / 2592000)
            return f"{months} month ago" if months == 1 else f"{months} months ago"
        else:
            years = int(seconds / 31536000)
            return f"{years} year ago" if years == 1 else f"{years} years ago"
    
    except Exception as e:
        logger.debug(f"Error formatting time: {e}")
        return "—"


def normalize_job(raw_job: Dict[str, Any]) -> Dict[str, Any]:
    """
    Normalize a raw job object from any source into consistent UI format.
    
    Input fields checked (in order):
      - posted_at, date_posted, publication_date, created_at, timestamp
    
    Returns:
        {
            "posted_at_iso": str or None,
            "posted_ago": str,           # Human-readable "X ago"
            "job_code": str,
            "title": str,
            "company": str,
            "location": str,
            "source": str,
            "match_percent": int,        # 0-100
            "apply_url": str,
            "description": str,
            "tags": list,
            # Original fields preserved
            ...raw_job
        }
    """
    if not raw_job or not isinstance(raw_job, dict):
        return {}
    
    # Try to extract posted date from various fields
    posted_at_iso = None
    posted_raw = (
        raw_job.get("posted_at") or
        raw_job.get("date_posted") or
        raw_job.get("publication_date") or
        raw_job.get("created_at") or
        raw_job.get("timestamp")
    )
    
    if posted_raw:
        try:
            if isinstance(posted_raw, str):
                dt = date_parser.parse(posted_raw)
                posted_at_iso = dt.isoformat()
        except Exception as e:
            logger.debug(f"Could not parse date {posted_raw}: {e}")
    
    # Compute "time ago"
    posted_ago = format_time_ago(posted_at_iso or posted_raw)
    
    # Helper to sanitize strings
    def safe_str(val: Any, default: str = "—") -> str:
        if isinstance(val, str):
            return val.strip() if val.strip() else default
        return default
    
    # Build normalized job
    normalized = {
        "posted_at_iso": posted_at_iso,
        "posted_ago": posted_ago,
        "job_code": safe_str(raw_job.get("job_code"), "unknown"),
        "title": safe_str(raw_job.get("title"), "Untitled"),
        "company": safe_str(raw_job.get("company"), "Unknown"),
        "location": safe_str(raw_job.get("location"), "Remote"),
        "source": safe_str(raw_job.get("source_name") or raw_job.get("source"), "Unknown"),
        "match_percent": int(raw_job.get("match_score", 0)) if raw_job.get("match_score") else 0,
        "apply_url": safe_str(raw_job.get("apply_url"), ""),
        "description": safe_str(raw_job.get("description_text"), ""),
        "tags": raw_job.get("tags", []) or [],
    }
    
    # Preserve original fields
    normalized.update(raw_job)
    
    return normalized


def normalize_jobs(raw_jobs: list) -> list:
    """Normalize a list of raw jobs."""
    return [normalize_job(job) for job in raw_jobs]


def compute_pagination(total_items: int, page: int, page_size: int) -> Dict[str, Any]:
    """
    Compute correct pagination values.
    
    Args:
        total_items: Total number of items
        page: Current page (1-indexed)
        page_size: Items per page
        
    Returns:
        {
            "total_pages": int,
            "current_page": int,      # Clamped to valid range
            "start_idx": int,         # 0-indexed
            "end_idx": int,           # 0-indexed, exclusive
            "start_num": int,         # 1-indexed for display
            "end_num": int,           # 1-indexed for display
            "is_first_page": bool,
            "is_last_page": bool,
            "display_text": str,      # "Showing X–Y of Z" or "No jobs"
        }
    """
    if total_items == 0:
        return {
            "total_pages": 0,
            "current_page": 1,
            "start_idx": 0,
            "end_idx": 0,
            "start_num": 0,
            "end_num": 0,
            "is_first_page": True,
            "is_last_page": True,
            "display_text": "No jobs",
        }
    
    total_pages = (total_items + page_size - 1) // page_size
    current_page = max(1, min(page, total_pages))
    
    start_idx = (current_page - 1) * page_size
    end_idx = min(current_page * page_size, total_items)
    
    start_num = start_idx + 1
    end_num = end_idx
    
    display_text = f"Showing {start_num}–{end_num} of {total_items}"
    
    return {
        "total_pages": total_pages,
        "current_page": current_page,
        "start_idx": start_idx,
        "end_idx": end_idx,
        "start_num": start_num,
        "end_num": end_num,
        "is_first_page": current_page == 1,
        "is_last_page": current_page == total_pages,
        "display_text": display_text,
    }
