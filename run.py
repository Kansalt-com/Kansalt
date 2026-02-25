#!/usr/bin/env python
"""
Quick start script - initializes and runs the app.
"""
import subprocess
import sys
import os
from pathlib import Path

print("Job Aggregator Portal - Startup")
print("=" * 50)

# Check Python version
if sys.version_info < (3, 8):
    print("[ERROR] Python 3.8+ required")
    sys.exit(1)

print("[OK] Python version OK")

# Check venv
if sys.prefix == sys.base_prefix:
    print("[WARN] Not in virtual environment. Recommended: activate venv first")
    print("   Windows: venv\\Scripts\\activate")
    print("   Mac/Linux: source venv/bin/activate")

# Run setup
print("\nRunning setup...")
result = subprocess.run([sys.executable, "setup.py"], cwd=".", capture_output=True, text=True)
print(result.stdout)
if result.returncode != 0:
    print(f"Setup error:\n{result.stderr}")
    sys.exit(1)

# Optional: Test scrapers
test_choice = input("\nRun scraper tests? (y/n): ").lower().strip()
if test_choice == "y":
    print("\nTesting scrapers...")
    result = subprocess.run([sys.executable, "test_scrapers.py"], cwd=".", capture_output=True, text=True)
    print(result.stdout)
    if result.returncode != 0:
        print(f"Some scrapers failed:\n{result.stderr}")

# Start Streamlit
print("\n" + "=" * 50)
print("Starting Streamlit app...")
print("=" * 50)
print("App will open at: http://localhost:8501")
print("Press Ctrl+C to stop\n")

try:
    subprocess.run([sys.executable, "-m", "streamlit", "run", "app/main.py"], cwd=".")
except KeyboardInterrupt:
    print("\n\nApp stopped.")
    sys.exit(0)
