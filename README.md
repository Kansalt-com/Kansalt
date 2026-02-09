# 🚀 Kansalt - Premium Remote Job Aggregator

Welcome to **Kansalt**, a modern SaaS dashboard for discovering remote jobs worldwide.

## ✨ Features

- 🔍 **Smart Search**: Filter by role, skills, location, and posting date
- 🌍 **Multi-Source**: Aggregates from diverse job boards and APIs
- 📊 **Match Scoring**: Get personalized match % for each job
- 📄 **Resume Tools**: Upload resume to generate tailored applications
- 🎨 **Modern UI**: Dark-theme SaaS dashboard with responsive design
- 🚀 **Cloud Ready**: Deploy to Render.com, Railway, or your own server

## 🎯 Quick Start

### Local Development (5 min)

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Run app
streamlit run app/main.py

# 3. Open browser
# → http://localhost:8501
```

### Docker (10 min)

```bash
# Start with one command
docker-compose up

# → http://localhost:8501
```

### Cloud Deployment (15 min)

See **[README_DEPLOY.md](README_DEPLOY.md)** for step-by-step Render.com deployment.

**Live Demo:** https://kansalt.onrender.com

## 📁 Project Structure

```
job_aggregator_portal/
├── app/
│   └── main.py              # Streamlit UI
├── services/
│   ├── __init__.py
│   ├── skill_engine.py      # Strict skill matching
│   ├── resume_parser.py     # Extract text from PDF/DOCX
│   ├── document_builder.py  # Generate tailored resumes/letters
│   └── job_fetcher.py       # Orchestrator (fetch, score, rank)
├── scrapers/
│   ├── __init__.py
│   ├── common.py            # Utilities (job_code, date parsing, etc.)
│   ├── remotive_api.py
│   ├── arbeitnow_api.py
│   ├── himalayas_api.py
│   ├── rss_common.py        # RSS base parser
│   └── rss_feeds.py         # 8 RSS feed implementations
├── db/
│   ├── __init__.py
│   ├── models.py            # SQLModel schemas (Job, User, Resume, Cache)
│   └── database.py          # DB connection
├── utils/
│   ├── __init__.py
│   ├── logger.py            # Logging setup
│   └── cache.py             # File-based cache manager
├── data/
│   └── skills.json          # Skill database (IT + Non-IT, 50+ skills)
├── logs/
│   └── app.log              # Application logs
├── cache/                   # Cache files (auto-generated)
├── job_aggregator.db        # SQLite database (auto-created)
├── requirements.txt         # Dependencies
├── test_scrapers.py         # Scraper validation tests
└── README.md                # This file
```

## 🚀 Quick Start

### 1. Clone & Setup

```bash
# Clone the repo
git clone <repo_url>
cd job_aggregator_portal

# Create virtual environment
python -m venv venv

# Activate venv
# On Windows:
venv\Scripts\activate
# On Mac/Linux:
source venv/bin/activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Initialize Database

```bash
python -c "from db import init_db; init_db()"
```

### 4. Run Tests (Optional)

```bash
python test_scrapers.py
```

Expected output:
```
✓ Remotive API: 20+ jobs
✓ ArbeitNow API: 15+ jobs
✓ Himalayas API: 10+ jobs
✓ We Work Remotely RSS: 50+ jobs
... (and more)

RESULTS: 35 passed, 0 failed | Sources: 35+
```

### 5. Run the Application

```bash
streamlit run app/main.py
```

The app will open at `http://localhost:8501`

## 💡 Usage Guide

### Search for Jobs

1. **Choose a search strategy**:
   - Enter a **Job Profile** (e.g., "DevOps Engineer")
   - OR select **Skills** from IT/Non-IT categories
   - OR add custom skills (comma-separated)
   - Mix and match!

2. **Set filters**:
   - **Location**: Remote, US, UK, Canada, etc.
   - **Date Posted**: Last 24h, 1 week, 2 weeks, 1 month
   - **Min Match %**: Show only jobs matching X% of criteria
   - **Results Per Page**: 25, 50, or 100

3. **Customize ranking**:
   - Adjust **Match vs Freshness** weights (default 60/40)

4. **Click "Search Jobs"** and browse results

### Upload Resume & Generate Documents

1. **Upload your resume** (PDF or DOCX) in the sidebar
   - Automatically extracts: name, email, phone
   - Stored in session state

2. **From results, click "📄 Resume"** for any job
   - Generates tailored resume with:
     - Job-relevant keywords injected
     - Skills reordered by relevance
     - Professional summary rewritten
   - ATS-safe formatting (Calibri, 11pt)
   - Download with naming: `{Name}_{JobCode}_Resume.docx`

3. **Click "📧 Cover Letter"** for any job
   - Generates 4-paragraph letter with:
     - Job title + company name
     - Relevant skills highlighted
     - Professional tone
   - Download with naming: `{Name}_{JobCode}_CoverLetter.docx`

### Guest vs Logged-In Users

- **Guest**: Full search + resume generation (no login required)
- **Logged-In**: (Feature ready for future implementation)
  - Save resume to profile
  - Track application history

## �️ Technical Architecture

### Skill Matching
- **Strict word-boundary matching** prevents false positives
- Prevents matching "scribe" in "describe" or "go" in "language"
- Supports multi-word terms ("ci/cd", "prior authorization")
- Configurable via `SHORT_OK` and `SHORT_BLOCK` lists

### Job Scoring
1. **Match Score** (0-100): % of user's search terms found in job
2. **Freshness Score** (0-100): Time-decay (100 if ≤24h, ~70 if 1w, ~30 if 1m)
3. **Rank Score**: Weighted combination (user-adjustable)

### Performance
- **Parallel fetching**: ThreadPoolExecutor with 30+ workers (concurrent API/RSS calls)
- **Caching**: 20-min TTL file-based cache to reduce repeated fetches
- **Deduplication**: By job_code + URL + title+company
- **Database-ready**: SQLModel for future persistence

### Resume Generation
- **No data fabrication**: Only tailors, never invents experience
- **ATS-safe**: Calibri font, 11pt, no tables/images
- **Smart keyword injection**: Extracts top 20 keywords from job posting
- **Clean output**: Removes URLs, garbage, HTML tags

## 🔧 Configuration

### Skill Categories

Edit `data/skills.json` to add/remove skills:

```json
{
  "categories": {
    "IT": {
      "DevOps": {"label": "DevOps", "aliases": ["devops", "infra"]},
      ...
    },
    "Healthcare": {...},
    "BPO": {...}
  }
}
```

### Cache TTL

Edit `utils/cache.py`:
```python
CACHE_TTL_MINUTES = 20  # Change to desired minutes
```

### Logging

Logs are written to `logs/app.log` with rotating handler (10MB per file, 5 backups).

## 📝 API Schema

All jobs normalized to:

```json
{
  "job_code": "remotive_api_abc12345",
  "title": "DevOps Engineer",
  "company": "TechCorp",
  "location": "Remote",
  "is_remote": true,
  "posted_at_iso": "2024-01-10T14:30:00+00:00",
  "posted_at_human": "2 days ago",
  "source_name": "Remotive API",
  "apply_url": "https://remotive.com/jobs/...",
  "description_text": "Plain text job description...",
  "tags": ["Python", "Docker", "AWS"]
}
```

## 🧪 Testing

### Run Scraper Tests

```bash
python test_scrapers.py
```

Validates:
- Each scraper returns jobs
- All required fields present
- Data types correct
- At least one working source before production

### Manual Testing

```bash
# Test skill matching
python -c "
from services import SkillMatcher
import json
with open('data/skills.json') as f:
    db = json.load(f)
skills = SkillMatcher.infer_skills_strict('I have 5 years Python and Docker', db)
print(f'Detected: {skills}')
"
```

## 🚨 Troubleshooting

| Issue | Solution |
|-------|----------|
| ImportError: "No module named 'streamlit'" | Run `pip install -r requirements.txt` |
| "No jobs found" | Check logs: `tail -f logs/app.log` |
| Resume parsing fails | Ensure PDF/DOCX is valid and not corrupted |
| Skills not matching | Edit `data/skills.json` to add aliases |
| Slow search | Wait for cache TTL (20 min) or manually clear `cache/` folder |
| DB errors | Delete `job_aggregator.db` and reinit: `python -c "from db import init_db; init_db()"` |

## 📦 Dependencies

- **streamlit** 1.28+ - Web UI framework
- **requests** 2.31+ - HTTP client
- **feedparser** 6.0+ - RSS parsing
- **PyPDF2** 3.16+ - PDF text extraction
- **python-docx** 0.8+ - DOCX generation
- **sqlmodel** 0.0.14+ - ORM (SQLAlchemy + Pydantic)
- **sqlalchemy** 2.0+ - Database toolkit
- **bcrypt** 4.0+ - Password hashing (future auth)
- **pydantic** 2.0+ - Data validation

## 🔒 Privacy & Security

- **No account required**: Guest mode fully supported
- **No data tracking**: Session state only (cleared on browser close)
- **Passwords**: Hashed with bcrypt (when auth is implemented)
- **HTTPS-ready**: Can be deployed behind reverse proxy
- **Logs**: Contain only non-sensitive info (job counts, error types)

## 🚀 Future Enhancements

- [ ] Full auth system (login/register/profile)
- [ ] Save jobs to profile (bookmarks)
- [ ] Application history & tracking
- [ ] Email notifications for new matching jobs
- [ ] AI-powered cover letter generation
- [ ] Resume analytics (keyword matching score)
- [ ] Mobile app (React Native)

## 📞 Support

- **Bug reports**: Check `logs/app.log` for details
- **Scraper issues**: Run `python test_scrapers.py` to identify which source failed
- **Questions**: See examples in this README

## 📄 License

MIT License - Free to use and modify

---

**Made with ❤️ for job seekers everywhere. No Indeed, LinkedIn, or Naukri. Just pure, free job aggregation.**
