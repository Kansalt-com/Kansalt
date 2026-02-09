#!/usr/bin/env python3
"""Debug script to test job fetching."""
import sys
from pathlib import Path
import json

project_root = str(Path(__file__).parent)
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from services.job_fetcher import (
    fetch_all_jobs, _expand_search_terms, SOURCES, _safe_call, _filter_by_location
)
from utils.logger import get_logger

logger = get_logger(__name__)

# Load skills database
with open("data/skills.json", "r", encoding="utf-8") as f:
    skills_db = json.load(f)

print("Testing job fetch...")

# Test raw scraper calls
print("\n=== Raw scraper test ===")
search_terms = _expand_search_terms([], skills_db, "Python Developer", [])
print(f"Search terms: {search_terms}")

total_jobs = 0
for source_name, fn in SOURCES:
    query_string = " ".join(search_terms[:3]) if search_terms else ""
    jobs = _safe_call(fn, query_string)
    print(f"{source_name}: {len(jobs)} jobs")
    total_jobs += len(jobs)

print(f"Total raw jobs: {total_jobs}")

# Now test full fetch with debugging
print("\n=== Full fetch_all_jobs (no location filter) ===")
jobs = fetch_all_jobs(
    selected_skills=[],
    skills_db=skills_db,
    job_profile="Python Developer",
    locations=[],  # Don't filter by location
    min_match=0,  # No minimum match
)
print(f"Final results: {len(jobs)} jobs")
if jobs:
    print(f"Sample: {jobs[0].get('title')} @ {jobs[0].get('company')}")
