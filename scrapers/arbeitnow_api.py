"""
ArbeitNow API scraper.
"""
import requests
from typing import List
from scrapers.common import make_job_code, parse_iso_date, relative_time
from utils.logger import get_logger

logger = get_logger(__name__)


def fetch_arbeitnow_api(query: str) -> List[dict]:
    """
    Fetch jobs from ArbeitNow API.
    API: https://www.arbeitnow.com/api/job-board-api/jobs
    """
    try:
        url = "https://www.arbeitnow.com/api/job-board-api/jobs"

        response = requests.get(url, timeout=15)
        response.raise_for_status()

        data = response.json()
        jobs = []
        query_lower = query.lower() if query else ""

        for job_data in data.get("data", []):
            try:
                # Basic filter
                if query_lower:
                    job_text = f"{job_data.get('title', '')} {job_data.get('company', '')}".lower()
                    if query_lower not in job_text:
                        continue

                posted_at_iso = parse_iso_date(job_data.get("posted_at"))
                posted_at_human = relative_time(posted_at_iso)

                job_obj = {
                    "job_code": make_job_code("arbeitnow_api", job_data.get("url", "")),
                    "title": job_data.get("title", "").strip(),
                    "company": job_data.get("company", "").strip(),
                    "location": job_data.get("location", "").strip() or "Remote",
                    "is_remote": "remote" in job_data.get("location", "").lower(),
                    "posted_at_iso": posted_at_iso,
                    "posted_at_human": posted_at_human,
                    "source_name": "ArbeitNow",
                    "apply_url": job_data.get("url", ""),
                    "description_text": job_data.get("description", "").strip(),
                    "tags": [],
                }
                jobs.append(job_obj)
            except Exception as e:
                logger.warning(f"ArbeitNow: error parsing job: {e}")
                continue

        logger.info(f"ArbeitNow API: fetched {len(jobs)} jobs")
        return jobs

    except Exception as e:
        logger.error(f"ArbeitNow API error: {e}")
        return []
