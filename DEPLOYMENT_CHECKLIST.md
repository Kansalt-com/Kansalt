# ✅ Deployment Checklist

Complete checklist for preparing Kansalt for production deployment.

## Pre-Deployment (Local Testing)

- [ ] **Code Quality**
  - [ ] No syntax errors: `python -m py_compile app/main.py`
  - [ ] No import errors: Run app locally without errors
  - [ ] Test search functionality: Returns results
  - [ ] Test resume upload: PDF/DOCX parsing works
  - [ ] Test document generation: Downloads work

- [ ] **Configuration**
  - [ ] `.streamlit/config.toml` is valid
  - [ ] `.env.example` has all required variables
  - [ ] `requirements.txt` has all dependencies
  - [ ] `Dockerfile` is valid (can build)
  - [ ] `render.yaml` is valid YAML

- [ ] **Files Present**
  - [ ] `app/main.py` (modernUI)
  - [ ] `services/*.py` (all services)
  - [ ] `scrapers/*.py` (all scrapers)
  - [ ] `data/skills.json` (skills database)
  - [ ] `requirements.txt`
  - [ ] `Dockerfile`
  - [ ] `docker-compose.yml`
  - [ ] `render.yaml`
  - [ ] `README_DEPLOY.md`
  - [ ] `.env.example`
  - [ ] `.streamlit/config.toml`

- [ ] **Testing**
  - [ ] Local run works: `streamlit run app/main.py`
  - [ ] Docker build works: `docker build -t kansalt:latest .`
  - [ ] Docker compose works: `docker-compose up`
  - [ ] No errors in Streamlit output
  - [ ] UI loads and is responsive
  - [ ] Dark theme colors are correct

## GitHub Setup

- [ ] **Repository Created**
  - [ ] GitHub account exists
  - [ ] Repository name: `job_aggregator_portal` (or similar)
  - [ ] Repository visibility: Public (for free Render deployment)
  - [ ] Repository has Description: "Premium Remote Job Aggregator"

- [ ] **Git Configuration**
  - [ ] `.gitignore` created (excludes `__pycache__`, `.venv`, `*.pyc`, etc.)
  - [ ] Initial commit created: `git add . && git commit -m "Initial commit"`
  - [ ] Remote added: `git remote add origin https://github.com/YOUR_USER/YOUR_REPO.git`
  - [ ] Pushed to GitHub: `git push -u origin main`

- [ ] **GitHub Files Verified**
  - [ ] All Python files present on GitHub
  - [ ] `requirements.txt` present
  - [ ] `Dockerfile` present
  - [ ] `render.yaml` present
  - [ ] `README.md` has good description
  - [ ] `README_DEPLOY.md` present

## Render.com Deployment

- [ ] **Render Account**
  - [ ] Account created at https://render.com
  - [ ] Email verified
  - [ ] GitHub connected (OAuth)

- [ ] **Deployment via Blueprint (Recommended)**
  - [ ] Go to https://render.com/dashboard
  - [ ] Click **New** → **Blueprint**
  - [ ] Select GitHub repository
  - [ ] Authorize GitHub access
  - [ ] Confirm services auto-detected
  - [ ] Review environment variables
  - [ ] Click **Deploy Blueprint**
  - [ ] Wait for build (2-3 minutes)
  - [ ] Check Logs for errors
  - [ ] See "Live" status

- [ ] **Deployment via Web Service (Alternative)**
  - [ ] Go to https://render.com/dashboard
  - [ ] Click **New** → **Web Service**
  - [ ] Connect GitHub repository
  - [ ] Configure:
    - Name: `kansalt`
    - Environment: `Python 3`
    - Build Command: `pip install -r requirements.txt`
    - Start Command: `streamlit run app/main.py --server.port=$PORT --server.address=0.0.0.0`
    - Plan: Free tier
  - [ ] Add Environment Variables:
    ```
    STREAMLIT_SERVER_HEADLESS=true
    STREAMLIT_LOGGER_LEVEL=info
    ```
  - [ ] Click **Deploy**
  - [ ] Wait for build completion

## Post-Deployment Testing

- [ ] **Live App Accessible**
  - [ ] Visit app URL (e.g., https://kansalt.onrender.com)
  - [ ] Page loads without errors
  - [ ] Dark theme displays correctly
  - [ ] All text is visible and readable

- [ ] **Functionality Testing**
  - [ ] [ ] Search works (enter "Python" and search)
  - [ ] [ ] Results display correctly
  - [ ] [ ] Job cards show title, company, location, match %
  - [ ] [ ] Pagination works (if results > 25)
  - [ ] [ ] Apply button works (opens in new tab)
  - [ ] [ ] Filters update results correctly
  - [ ] [ ] Empty state shows when no results

- [ ] **Resume Features**
  - [ ] [ ] Resume upload field visible
  - [ ] [ ] PDF upload works
  - [ ] [ ] Document generation buttons appear
  - [ ] [ ] Resume/cover letter download works

- [ ] **Performance**
  - [ ] [ ] Page loads in < 3 seconds
  - [ ] [ ] Search completes in < 5 seconds
  - [ ] [ ] No console errors (check browser DevTools)
  - [ ] [ ] Health check endpoint works: `/_stcore/health`

- [ ] **Error Handling**
  - [ ] [ ] No filters set → Shows error message
  - [ ] [ ] Bad search → Shows empty state
  - [ ] [ ] Network error → Shows friendly message
  - [ ] [ ] File upload fails → Shows error

## Domain & Customization (Optional)

- [ ] **Custom Domain**
  - [ ] Domain purchased (e.g., kansalt.io)
  - [ ] DNS configured (if needed)
  - [ ] Added to Render dashboard
  - [ ] HTTPS working
  - [ ] Redirects working

- [ ] **Branding**
  - [ ] Logo visible in navbar
  - [ ] Brand colors correct
  - [ ] Footer visible with contact info
  - [ ] Page title updated in browser tab

## Monitoring & Maintenance

- [ ] **Render Dashboard**
  - [ ] Service shows "Live" status
  - [ ] No recent error logs
  - [ ] Build logs archived

- [ ] **Monitoring Setup** (Optional)
  - [ ] Email alerts configured
  - [ ] Uptime monitoring enabled
  - [ ] Performance metrics viewable

- [ ] **Documentation**
  - [ ] `README.md` reflects live URL
  - [ ] `README_DEPLOY.md` is accurate
  - [ ] Instructions tested by someone else
  - [ ] Troubleshooting guide complete

## After Deployment

- [ ] **Communication**
  - [ ] Share live link with users/team
  - [ ] Post on social media (optional)
  - [ ] Update project documentation
  - [ ] Add to portfolio/resume (if personal project)

- [ ] **Ongoing**
  - [ ] Monitor error logs weekly
  - [ ] Test app monthly
  - [ ] Update dependencies as needed
  - [ ] Gather user feedback
  - [ ] Plan v2 features

---

## Quick Checklist Summary

```
[ ] Code tested locally
[ ] Files committed to GitHub
[ ] GitHub repo public
[ ] Render account created
[ ] Blueprint deployed
[ ] App loads without errors
[ ] Search functionality works
[ ] Results display correctly
[ ] Apply button works
[ ] Resume upload works
[ ] No console errors
[ ] Live URL shared with team
```

---

## Rollback Plan

If deployment fails:

```bash
# 1. Check Render logs for errors
# Render Dashboard → Logs → Search for "ERROR"

# 2. Common fixes:
# - Add missing environment variables
# - Fix Python syntax errors
# - Check requirements.txt
# - Verify Dockerfile EXPOSE port

# 3. Rollback to previous version:
git revert <commit_id>
git push origin main
# Render auto-redeploys

# 4. Contact Render support if stuck
```

---

## Success Criteria

✅ All checks pass when:
- App loads: https://kansalt.onrender.com
- No errors in Render logs
- Search returns results
- UI renders in dark theme
- Apply button opens job link
- Resume upload works (if applicable)

---

**Deployment Date:** _______________

**Deployed By:** _______________

**Status:** [ ] In Progress  [ ] Deployed  [ ] Live  [ ] Issues Found

**Notes:** _______________________________________________

