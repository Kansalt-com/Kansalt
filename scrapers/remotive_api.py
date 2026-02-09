"""
Remotive API scraper.
"""
import requests
from typing import List
from scrapers.common import make_job_code, parse_iso_date, relative_time
from utils.logger import get_logger

logger = get_logger(__name__)


def fetch_remotive_api(query: str) -> List[dict]:
    """
    Fetch jobs from Remotive API.
    API: https://remotive.com/api/remote-jobs
    """
    try:
        url = "https://remotive.com/api/remote-jobs"
        params = {"search": query} if query else {}

        response = requests.get(url, params=params, timeout=15)
        response.raise_for_status()

        data = response.json()
        jobs = []

        for job_data in data.get("jobs", []):
            try:
                posted_at_iso = parse_iso_date(job_data.get("published_at"))
                posted_at_human = relative_time(posted_at_iso)

                job_obj = {
                    "job_code": make_job_code("remotive_api", job_data.get("url", "")),
                    "title": job_data.get("title", "").strip(),
                    "company": job_data.get("company_name", "").strip(),
                    "location": job_data.get("candidate_required_location", "Remote"),
                    "is_remote": True,
                    "posted_at_iso": posted_at_iso,
                    "posted_at_human": posted_at_human,
                    "source_name": "Remotive API",
                    "apply_url": job_data.get("url", ""),
                    "description_text": job_data.get("description", "").strip(),
                    "tags": job_data.get("tags", []) or [],
                }
                jobs.append(job_obj)
            except Exception as e:
                logger.warning(f"Remotive: error parsing job: {e}")
                continue

        logger.info(f"Remotive API: fetched {len(jobs)} jobs")
        return jobs

    except Exception as e:
        logger.error(f"Remotive API error: {e}")
        return []
