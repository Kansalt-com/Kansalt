#!/usr/bin/env python
"""
Setup script to initialize database and directories.
"""

import sys
from pathlib import Path


def _ok(message: str) -> None:
    print(f"[OK] {message}")


def _err(message: str) -> None:
    print(f"[ERROR] {message}")


log_dir = Path("logs")
log_dir.mkdir(exist_ok=True)
_ok(f"Logs directory: {log_dir}")

cache_dir = Path("cache")
cache_dir.mkdir(exist_ok=True)
_ok(f"Cache directory: {cache_dir}")

try:
    from db import init_db

    init_db()
    _ok("Database initialized")
except Exception as exc:
    _err(f"Database init failed: {exc}")
    sys.exit(1)

if not Path("data/skills.json").exists():
    _err("data/skills.json not found")
    sys.exit(1)

_ok("Skills database found")

print("\nSetup complete.")
print("\nNext steps:")
print("1. Run scrapers test:  python test_scrapers.py")
print("2. Start app:          streamlit run app/main.py")
