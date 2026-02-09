#!/usr/bin/env python
"""
Setup script to initialize database and directories.
"""
import os
import sys
from pathlib import Path

# Ensure logs directory exists
log_dir = Path("logs")
log_dir.mkdir(exist_ok=True)
print(f"✓ Logs directory: {log_dir}")

# Ensure cache directory exists
cache_dir = Path("cache")
cache_dir.mkdir(exist_ok=True)
print(f"✓ Cache directory: {cache_dir}")

# Initialize database
try:
    from db import init_db
    init_db()
    print("✓ Database initialized")
except Exception as e:
    print(f"✗ Database init failed: {e}")
    sys.exit(1)

# Check if skills.json exists
if not Path("data/skills.json").exists():
    print("✗ data/skills.json not found!")
    sys.exit(1)

print("✓ Skills database found")

print("\n✅ Setup complete!")
print("\nNext steps:")
print("1. Run scrapers test:  python test_scrapers.py")
print("2. Start app:          streamlit run app/main.py")
