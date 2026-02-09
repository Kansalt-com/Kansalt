"""
Unit tests for job normalization and pagination utilities.
"""
import pytest
from datetime import datetime, timezone, timedelta
from services.job_normalizer import (
    format_time_ago, normalize_job, compute_pagination
)


class TestFormatTimeAgo:
    """Test time ago formatting."""
    
    def test_just_now(self):
        """Test very recent timestamps."""
        now = datetime.now(timezone.utc)
        result = format_time_ago(now)
        assert result == "Just now"
    
    def test_minutes_ago(self):
        """Test minutes ago."""
        past = datetime.now(timezone.utc) - timedelta(minutes=15)
        result = format_time_ago(past)
        assert "mins ago" in result or "min ago" in result
    
    def test_hours_ago(self):
        """Test hours ago."""
        past = datetime.now(timezone.utc) - timedelta(hours=2)
        result = format_time_ago(past)
        assert "hours ago" in result or "hour ago" in result
    
    def test_days_ago(self):
        """Test days ago."""
        past = datetime.now(timezone.utc) - timedelta(days=3)
        result = format_time_ago(past)
        assert "days ago" in result or "day ago" in result
    
    def test_none_input(self):
        """Test None input."""
        result = format_time_ago(None)
        assert result == "—"
    
    def test_invalid_input(self):
        """Test invalid input."""
        result = format_time_ago("not a date")
        # Should try to parse and either succeed or return "—"
        assert isinstance(result, str)


class TestNormalizeJob:
    """Test job normalization."""
    
    def test_basic_normalization(self):
        """Test basic job normalization."""
        raw_job = {
            "job_code": "test_123",
            "title": "Senior Developer",
            "company": "TechCorp",
            "location": "Remote",
            "source_name": "Test Source",
            "match_score": 85,
            "apply_url": "https://example.com/apply",
        }
        
        normalized = normalize_job(raw_job)
        
        assert normalized["job_code"] == "test_123"
        assert normalized["title"] == "Senior Developer"
        assert normalized["company"] == "TechCorp"
        assert normalized["location"] == "Remote"
        assert normalized["match_percent"] == 85
        assert normalized["posted_ago"] == "—"  # No date provided
    
    def test_missing_fields_use_defaults(self):
        """Test that missing fields use sensible defaults."""
        raw_job = {}
        normalized = normalize_job(raw_job)
        
        assert normalized["job_code"] == "unknown"
        assert normalized["title"] == "Untitled"
        assert normalized["company"] == "Unknown"
        assert normalized["location"] == "Remote"
        assert normalized["match_percent"] == 0
        assert normalized["posted_ago"] == "—"
    
    def test_date_parsing(self):
        """Test date parsing from various fields."""
        now = datetime.now(timezone.utc)
        iso_date = now.isoformat()
        
        raw_job = {
            "posted_at": iso_date,
            "job_code": "test",
            "title": "Test Job",
        }
        
        normalized = normalize_job(raw_job)
        assert normalized["posted_ago"] != "—"
        assert "ago" in normalized["posted_ago"] or "Just now" in normalized["posted_ago"]
    
    def test_whitespace_trimming(self):
        """Test that strings are trimmed."""
        raw_job = {
            "title": "  Senior Developer  ",
            "company": "  TechCorp  ",
            "job_code": "test",
        }
        
        normalized = normalize_job(raw_job)
        assert normalized["title"] == "Senior Developer"
        assert normalized["company"] == "TechCorp"


class TestComputePagination:
    """Test pagination calculation."""
    
    def test_no_items(self):
        """Test pagination with no items."""
        result = compute_pagination(0, 1, 25)
        
        assert result["total_pages"] == 0
        assert result["current_page"] == 1
        assert result["start_num"] == 0
        assert result["end_num"] == 0
        assert result["is_first_page"] is True
        assert result["is_last_page"] is True
        assert result["display_text"] == "No jobs"
    
    def test_single_page(self):
        """Test pagination with items < page_size."""
        result = compute_pagination(13, 1, 25)
        
        assert result["total_pages"] == 1
        assert result["current_page"] == 1
        assert result["start_num"] == 1
        assert result["end_num"] == 13
        assert result["display_text"] == "Showing 1–13 of 13"
        assert result["is_first_page"] is True
        assert result["is_last_page"] is True
    
    def test_multiple_pages(self):
        """Test pagination with multiple pages."""
        result = compute_pagination(100, 2, 25)
        
        assert result["total_pages"] == 4
        assert result["current_page"] == 2
        assert result["start_num"] == 26
        assert result["end_num"] == 50
        assert result["display_text"] == "Showing 26–50 of 100"
        assert result["is_first_page"] is False
        assert result["is_last_page"] is False
    
    def test_page_clamping(self):
        """Test that page is clamped to valid range."""
        # Page too high
        result = compute_pagination(100, 999, 25)
        assert result["current_page"] == 4
        assert result["is_last_page"] is True
        
        # Page too low
        result = compute_pagination(100, 0, 25)
        assert result["current_page"] == 1
        assert result["is_first_page"] is True
    
    def test_last_page_partial(self):
        """Test last page with partial results."""
        result = compute_pagination(75, 3, 25)
        
        assert result["total_pages"] == 3
        assert result["current_page"] == 3
        assert result["start_num"] == 51
        assert result["end_num"] == 75
        assert result["display_text"] == "Showing 51–75 of 75"
        assert result["is_last_page"] is True


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
