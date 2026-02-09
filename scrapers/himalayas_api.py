"""
TheHimalayas API scraper.
"""
import requests
from typing import List
from scrapers.common import make_job_code, parse_iso_date, relative_time
from utils.logger import get_logger

logger = get_logger(__name__)


def fetch_himalayas_api(query: str) -> List[dict]:
    """
    Fetch jobs from TheHimalayas API.
    API: https://api.thehimalayas.com/jobs
    """
    try:
        url = "https://api.thehimalayas.com/jobs"
        params = {"search": query} if query else {}

        response = requests.get(url, params=params, timeout=15)
        response.raise_for_status()

        data = response.json()
        jobs = []

        for job_data in data.get("jobs", []):
            try:
                posted_at_iso = parse_iso_date(job_data.get("pub_date"))
                posted_at_human = relative_time(posted_at_iso)

                job_obj = {
                    "job_code": make_job_code("himalayas_api", job_data.get("link", "")),
                    "title": job_data.get("title", "").strip(),
                    "company": job_data.get("company_name", "").strip(),
                    "location": job_data.get("location", "").strip() or "Remote",
                    "is_remote": "remote" in job_data.get("location", "").lower(),
                    "posted_at_iso": posted_at_iso,
                    "posted_at_human": posted_at_human,
                    "source_name": "The Himalayas",
                    "apply_url": job_data.get("link", ""),
                    "description_text": job_data.get("description", "").strip(),
                    "tags": job_data.get("tags", []) or [],
                }
                jobs.append(job_obj)
            except Exception as e:
                logger.warning(f"Himalayas: error parsing job: {e}")
                continue

        logger.info(f"Himalayas API: fetched {len(jobs)} jobs")
        return jobs

    except Exception as e:
        logger.error(f"Himalayas API error: {e}")
        return []
