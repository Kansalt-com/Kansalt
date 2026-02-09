"""
Test all scrapers to validate they work and return proper schema.
"""
import json
from scrapers import (
    fetch_remotive_api, fetch_arbeitnow_api, fetch_himalayas_api,
    fetch_wwr_rss, fetch_remotive_rss, fetch_jobscollider_rss,
    fetch_jobalign_rss, fetch_workingviral_rss, fetch_jobicy_rss,
    fetch_remoteca_rss, fetch_authenticjobs_rss,
    fetch_stackoverflow_rss, fetch_github_rss, fetch_developerjob_rss,
    fetch_flexjobs_rss, fetch_nofluff_rss, fetch_weworkpython_rss,
    fetch_javascript_rss, fetch_rubyonrails_rss, fetch_golangjobs_rss,
    fetch_rustiocean_rss, fetch_javaremote_rss, fetch_devopsboard_rss,
    fetch_designjobs_rss, fetch_marketingjobs_rss, fetch_salesjobs_rss,
    fetch_contentjobs_rss, fetch_datajobs_rss, fetch_aijobs_rss,
    fetch_securityjobs_rss, fetch_vmjobs_rss, fetch_translatorjobs_rss,
    fetch_educationjobs_rss, fetch_businessjobs_rss, fetch_projectmgmt_rss
)
from utils.logger import get_logger

logger = get_logger(__name__)

SCRAPERS = [
    ("Remotive API", lambda: fetch_remotive_api("Python")),
    ("ArbeitNow API", lambda: fetch_arbeitnow_api("Python")),
    ("Himalayas API", lambda: fetch_himalayas_api("Python")),
    ("We Work Remotely RSS", fetch_wwr_rss),
    ("Remotive RSS", fetch_remotive_rss),
    ("Jobs Collider RSS", fetch_jobscollider_rss),
    ("JobAlign RSS", fetch_jobalign_rss),
    ("WorkingViral RSS", fetch_workingviral_rss),
    ("JobIcy RSS", fetch_jobicy_rss),
    ("Remote.CA RSS", fetch_remoteca_rss),
    ("Authentic Jobs RSS", fetch_authenticjobs_rss),
    ("Stack Overflow RSS", fetch_stackoverflow_rss),
    ("GitHub Jobs RSS", fetch_github_rss),
    ("DeveloperJob RSS", fetch_developerjob_rss),
    ("FlexJobs RSS", fetch_flexjobs_rss),
    ("No Fluff Jobs RSS", fetch_nofluff_rss),
    ("Python Jobs RSS", fetch_weworkpython_rss),
    ("JavaScript Jobs RSS", fetch_javascript_rss),
    ("Ruby on Rails RSS", fetch_rubyonrails_rss),
    ("Golang Jobs RSS", fetch_golangjobs_rss),
    ("Rust Jobs RSS", fetch_rustiocean_rss),
    ("Java Jobs RSS", fetch_javaremote_rss),
    ("DevOps Jobs RSS", fetch_devopsboard_rss),
    ("Design Jobs RSS", fetch_designjobs_rss),
    ("Marketing Jobs RSS", fetch_marketingjobs_rss),
    ("Sales Jobs RSS", fetch_salesjobs_rss),
    ("Content Jobs RSS", fetch_contentjobs_rss),
    ("Data Jobs RSS", fetch_datajobs_rss),
    ("AI Jobs RSS", fetch_aijobs_rss),
    ("Security Jobs RSS", fetch_securityjobs_rss),
    ("Virtual Jobs RSS", fetch_vmjobs_rss),
    ("Translator Jobs RSS", fetch_translatorjobs_rss),
    ("Education Jobs RSS", fetch_educationjobs_rss),
    ("Business Jobs RSS", fetch_businessjobs_rss),
    ("Project Management RSS", fetch_projectmgmt_rss),
]

REQUIRED_FIELDS = {
    "job_code", "title", "company", "location", "is_remote",
    "posted_at_iso", "posted_at_human", "source_name", "apply_url",
    "description_text", "tags"
}


def validate_job_schema(job: dict) -> tuple[bool, str]:
    """Validate job has required fields."""
    missing = REQUIRED_FIELDS - set(job.keys())
    if missing:
        return False, f"Missing fields: {missing}"

    # Type checks
    if not isinstance(job["job_code"], str) or not job["job_code"]:
        return False, "job_code must be non-empty string"

    if not isinstance(job["title"], str) or not job["title"]:
        return False, "title must be non-empty string"

    if not isinstance(job["apply_url"], str) or not job["apply_url"]:
        return False, "apply_url must be non-empty string"

    if not isinstance(job["is_remote"], bool):
        return False, "is_remote must be boolean"

    if not isinstance(job["tags"], list):
        return False, "tags must be list"

    return True, "OK"


def test_scrapers():
    """Test all scrapers."""
    print("\n" + "=" * 80)
    print("SCRAPER VALIDATION TEST")
    print("=" * 80)

    total_jobs = 0
    passed = 0
    failed = 0

    for scraper_name, scraper_fn in SCRAPERS:
        print(f"\n🧪 Testing {scraper_name}...")
        try:
            jobs = scraper_fn()

            if not jobs:
                print(f"   ⚠️  No jobs returned")
                failed += 1
                continue

            print(f"   ✓ Fetched {len(jobs)} jobs")
            total_jobs += len(jobs)

            # Validate first job
            first_job = jobs[0]
            valid, msg = validate_job_schema(first_job)

            if not valid:
                print(f"   ✗ Schema validation failed: {msg}")
                print(f"   Job keys: {set(first_job.keys())}")
                failed += 1
                continue

            print(f"   ✓ Schema valid")
            print(f"      Sample: {first_job['title'][:50]} @ {first_job['company'][:30]}")
            passed += 1

        except Exception as e:
            print(f"   ✗ Exception: {e}")
            logger.error(f"Scraper test error ({scraper_name}): {e}")
            failed += 1

    print("\n" + "=" * 80)
    print(f"RESULTS: {passed} passed, {failed} failed | Total jobs: {total_jobs}")
    print("=" * 80)

    return passed, failed, total_jobs


if __name__ == "__main__":
    passed, failed, total = test_scrapers()
    exit(0 if failed == 0 else 1)
