#!/usr/bin/env python3
"""Test scrapers directly."""
import sys
from pathlib import Path

project_root = str(Path(__file__).parent)
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from scrapers.remotive_api import fetch_remotive_api
from scrapers.rss_feeds import fetch_remotive_rss

print("Testing Remotive API with 'Python'...")
jobs = fetch_remotive_api("Python")
print(f"Got {len(jobs)} jobs")
if jobs:
    print(f"Sample: {jobs[0]}")

print("\nTesting Remotive RSS...")
jobs = fetch_remotive_rss()
print(f"Got {len(jobs)} jobs")
if jobs:
    print(f"Sample: {jobs[0]}")
