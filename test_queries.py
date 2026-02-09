#!/usr/bin/env python3
"""Test scraper queries."""
import sys
from pathlib import Path

project_root = str(Path(__file__).parent)
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from scrapers.remotive_api import fetch_remotive_api

queries = [
    "",
    "Python",
    "python developer",
    "Python Developer",
    "python developer python developer",
]

for q in queries:
    print(f"\nQuery: '{q}'")
    try:
        jobs = fetch_remotive_api(q)
        print(f"  Result: {len(jobs)} jobs")
        if jobs:
            print(f"  Sample: {jobs[0]['title'][:50]}")
    except Exception as e:
        print(f"  Error: {e}")
