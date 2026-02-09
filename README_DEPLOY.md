# 🚀 Kansalt Deployment Guide

Complete step-by-step guide to deploy Kansalt to production.

## Table of Contents

1. [Local Development](#local-development)
2. [Docker Setup](#docker-setup)
3. [Deploy to Render.com](#deploy-to-rendercom)
4. [Troubleshooting](#troubleshooting)

---

## Local Development

### Prerequisites

- Python 3.11+
- pip or conda
- Git

### Setup

```bash
# 1. Clone repository (or extract)
cd job_aggregator_portal

# 2. Create virtual environment
python -m venv .venv

# 3. Activate virtual environment
# On Windows:
.venv\Scripts\activate
# On macOS/Linux:
source .venv/bin/activate

# 4. Install dependencies
pip install -r requirements.txt

# 5. Run setup (if needed)
python setup.py

# 6. Start Streamlit app
streamlit run app/main.py
```

Your app will be available at: **http://localhost:8501**

---

## Docker Setup

### Prerequisites

- Docker installed ([Download](https://www.docker.com/products/docker-desktop))
- Docker Compose

### Build & Run Locally

```bash
# 1. Build Docker image
docker build -t kansalt:latest .

# 2. Run with Docker
docker run -p 8501:8501 kansalt:latest

# OR use Docker Compose (easier)
docker-compose up --build
```

App will be available at: **http://localhost:8501**

### Test Docker Image

```bash
# Check if container is running
docker ps

# View logs
docker logs <container_id>

# Stop container
docker stop <container_id>

# Push to Docker Hub (optional for CI/CD)
docker tag kansalt:latest yourname/kansalt:latest
docker push yourname/kansalt:latest
```

---

## Deploy to Render.com

### Step 1: Prepare Your Repository

The repo must be on GitHub (public or private). File structure must include:

```
job_aggregator_portal/
├── app/
│   └── main.py
├── services/
│   ├── __init__.py
│   ├── job_fetcher.py
│   ├── job_normalizer.py
│   ├── skill_engine.py
│   ├── resume_parser.py
│   └── document_builder.py
├── scrapers/
│   ├── __init__.py
│   ├── remotive_api.py
│   ├── arbeitnow_api.py
│   ├── himalayas_api.py
│   └── rss_feeds.py
├── db/
│   ├── __init__.py
│   ├── database.py
│   └── models.py
├── utils/
│   ├── __init__.py
│   ├── cache.py
│   └── logger.py
├── data/
│   └── skills.json
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
├── render.yaml
├── .env.example
└── .streamlit/
    └── config.toml
```

### Step 2: Create GitHub Repo

```bash
# 1. Initialize git (if not already)
git init

# 2. Add all files
git add .

# 3. Commit
git commit -m "Initial commit: Kansalt job aggregator"

# 4. Create repo on GitHub.com, then:
git remote add origin https://github.com/YOUR_USERNAME/job_aggregator_portal.git
git branch -M main
git push -u origin main
```

### Step 3: Deploy on Render.com

**Option A: Using Blueprint (Recommended)**

1. Go to https://render.com
2. Sign up / Log in
3. Click **"New" → "Blueprint"**
4. Select your GitHub repository
5. Authorize GitHub access
6. Render will auto-detect `render.yaml` and deploy
7. Wait 2-3 minutes for build/deploy
8. Your app will be live at: **https://kansalt.onrender.com** (or custom domain)

**Option B: Manual Setup**

1. Go to https://render.com
2. Click **"New" → "Web Service"**
3. Connect your GitHub repository
4. Fill in settings:
   - **Name:** `kansalt`
   - **Environment:** `Python 3`
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `streamlit run app/main.py --server.port=$PORT --server.address=0.0.0.0`
   - **Plan:** Free (or paid for better performance)
5. Add environment variables:
   ```
   STREAMLIT_SERVER_HEADLESS=true
   STREAMLIT_LOGGER_LEVEL=info
   STREAMLIT_SERVER_ENABLE_XSRF_PROTECTION=true
   ```
6. Click **Deploy**
7. Wait for build to complete (2-3 min)
8. Get your live URL from the dashboard

### Step 4: Configure Domain (Optional)

1. In Render dashboard, go to your service
2. Click **Settings → Custom Domains**
3. Add your domain (e.g., `kansalt.io`)
4. Update DNS records as instructed

---

## Environment Variables

Create a `.env` file locally (copy from `.env.example`):

```bash
cp .env.example .env
```

Edit `.env` with your settings:

```env
STREAMLIT_SERVER_PORT=8501
STREAMLIT_SERVER_ADDRESS=0.0.0.0
STREAMLIT_LOGGER_LEVEL=info
STREAMLIT_SERVER_HEADLESS=true
STREAMLIT_SERVER_ENABLE_XSRF_PROTECTION=true
```

For **Render.com**, add these as environment variables in the dashboard (no `.env` file needed).

---

## Health Checks

Render uses this endpoint to verify your app is running:

```
GET /_stcore/health
```

This is built into Streamlit. If you see health check failures, check logs for errors.

---

## Troubleshooting

### App Won't Start Locally

```bash
# Clear Streamlit cache
rm -rf ~/.streamlit/

# Reinstall dependencies
pip install --upgrade -r requirements.txt

# Run with debug
streamlit run app/main.py --logger.level=debug
```

### Docker Build Fails

```bash
# Check Python version
python --version  # Should be 3.11+

# Clean Docker cache
docker system prune -a

# Rebuild
docker build --no-cache -t kansalt:latest .
```

### Render.com Deployment Issues

1. **Build fails:**
   - Check build logs in Render dashboard
   - Ensure `requirements.txt` has all dependencies
   - Verify `Dockerfile` and `render.yaml` syntax

2. **App crashes after deploy:**
   - Check logs: `Render Dashboard → Logs`
   - Common issues:
     - Missing environment variables
     - Port conflicts
     - File path issues (use absolute paths)

3. **Port issues:**
   - Render assigns `PORT` env var automatically
   - Ensure start command uses `$PORT`

4. **Health check failing:**
   - Streamlit takes 30-60s to start
   - Check if CPU/memory is low
   - Increase Render plan if needed

### Streamlit Warnings in Logs

These are normal:
```
WARNING: Streamlit works best when served over HTTPS
```

### Database Errors

```bash
# Ensure database file can be created
# Use SQLite (file-based), not in-memory
# Render has ephemeral filesystem, so use volumes or cloud DB if needed
```

### Resume Upload Not Working

- Check file size (max 100MB in config)
- Ensure PDF/DOCX library imports work
- Test locally first with Docker

---

## Monitoring & Logs

### Local

```bash
# Run with verbose logging
streamlit run app/main.py --logger.level=debug

# Monitor Docker
docker logs -f <container_id>
```

### Render.com

1. Dashboard → Your service
2. Click **Logs** tab
3. Filter by date/time
4. Check for errors (red text)

---

## Rollback

If deployment breaks:

```bash
# Git rollback to previous version
git log --oneline  # Find commit
git revert <commit_id>
git push

# Render auto-redeploys on push
# Wait for build to complete
```

---

## Performance Tips

- Use Streamlit caching (`@st.cache_resource`, `@st.cache_data`)
- Lazy-load heavy components
- Use CDN for static assets (if any)
- Monitor API response times
- Profile with: `streamlit run app/main.py --logger.level=debug`

---

## Support & Resources

- **Streamlit Docs:** https://docs.streamlit.io
- **Render Docs:** https://render.com/docs
- **Python Docs:** https://docs.python.org
- **Docker Docs:** https://docs.docker.com

---

## Quick Cheat Sheet

```bash
# Local
streamlit run app/main.py

# Docker local
docker-compose up

# GitHub push
git push origin main

# Render deploy (auto on push if connected)

# Check live app
curl https://kansalt.onrender.com/_stcore/health
```

---

## Summary

| Method | Time | Difficulty | Cost |
|--------|------|-----------|------|
| Local | 5 min | ⭐ Easy | Free |
| Docker Local | 10 min | ⭐⭐ Medium | Free |
| Render.com | 15 min | ⭐ Easy | Free (with paid options) |

**Recommended for production:** Render.com (Option A: Blueprint)

---

**Last Updated:** Feb 8, 2026
**Kansalt Version:** 1.0
