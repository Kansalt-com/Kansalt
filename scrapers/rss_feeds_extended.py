"""Extended RSS feed scrapers for additional job boards."""

from typing import List
from scrapers.rss_common import RSSFeedParser
from scrapers.common import make_job_code
from utils.logger import get_logger

logger = get_logger(__name__)


# === Additional RSS Feed Sources (20+) ===

def fetch_stackoverflow_rss(query: str = "") -> List[dict]:
    """Stack Overflow Remote Jobs RSS feed."""
    jobs = RSSFeedParser.parse_feed(
        "https://stackoverflow.com/jobs/feed?q=remote",
        "Stack Overflow"
    )
    for job in jobs:
        job["job_code"] = make_job_code("stackoverflow_rss", job["apply_url"])
    return jobs


def fetch_github_rss(query: str = "") -> List[dict]:
    """GitHub Jobs RSS feed."""
    jobs = RSSFeedParser.parse_feed(
        "https://jobs.github.com/positions.json",
        "GitHub Jobs"
    )
    for job in jobs:
        job["job_code"] = make_job_code("github_rss", job["apply_url"])
    return jobs


def fetch_developerjob_rss(query: str = "") -> List[dict]:
    """DeveloperJob RSS feed."""
    jobs = RSSFeedParser.parse_feed(
        "https://www.developerjob.com/feed",
        "DeveloperJob"
    )
    for job in jobs:
        job["job_code"] = make_job_code("developerjob_rss", job["apply_url"])
    return jobs


def fetch_flexjobs_rss(query: str = "") -> List[dict]:
    """FlexJobs RSS feed."""
    jobs = RSSFeedParser.parse_feed(
        "https://www.flexjobs.com/feed",
        "FlexJobs"
    )
    for job in jobs:
        job["job_code"] = make_job_code("flexjobs_rss", job["apply_url"])
    return jobs


def fetch_nofluff_rss(query: str = "") -> List[dict]:
    """No Fluff Jobs RSS feed."""
    jobs = RSSFeedParser.parse_feed(
        "https://nofluffjobs.com/feed",
        "No Fluff Jobs"
    )
    for job in jobs:
        job["job_code"] = make_job_code("nofluff_rss", job["apply_url"])
    return jobs


def fetch_weworkpython_rss(query: str = "") -> List[dict]:
    """Python Remote Jobs RSS feed."""
    jobs = RSSFeedParser.parse_feed(
        "https://www.python-jobs.com/feed",
        "Python Jobs"
    )
    for job in jobs:
        job["job_code"] = make_job_code("weworkpython_rss", job["apply_url"])
    return jobs


def fetch_javascript_rss(query: str = "") -> List[dict]:
    """JavaScript/Frontend Remote Jobs RSS feed."""
    jobs = RSSFeedParser.parse_feed(
        "https://www.javascript-jobs.com/feed",
        "JavaScript Jobs"
    )
    for job in jobs:
        job["job_code"] = make_job_code("javascript_rss", job["apply_url"])
    return jobs


def fetch_rubyonrails_rss(query: str = "") -> List[dict]:
    """Ruby on Rails Jobs RSS feed."""
    jobs = RSSFeedParser.parse_feed(
        "https://www.rubyonrailsjobs.com/feed",
        "Ruby on Rails Jobs"
    )
    for job in jobs:
        job["job_code"] = make_job_code("rubyonrails_rss", job["apply_url"])
    return jobs


def fetch_golangjobs_rss(query: str = "") -> List[dict]:
    """Go/Golang Remote Jobs RSS feed."""
    jobs = RSSFeedParser.parse_feed(
        "https://www.golangjobs.com/feed",
        "Golang Jobs"
    )
    for job in jobs:
        job["job_code"] = make_job_code("golangjobs_rss", job["apply_url"])
    return jobs


def fetch_rustiocean_rss(query: str = "") -> List[dict]:
    """Rust Remote Jobs RSS feed."""
    jobs = RSSFeedParser.parse_feed(
        "https://www.rustiocean.com/feed",
        "Rust Jobs"
    )
    for job in jobs:
        job["job_code"] = make_job_code("rustiocean_rss", job["apply_url"])
    return jobs


def fetch_javaremote_rss(query: str = "") -> List[dict]:
    """Java Remote Jobs RSS feed."""
    jobs = RSSFeedParser.parse_feed(
        "https://www.javaremote.com/feed",
        "Java Jobs"
    )
    for job in jobs:
        job["job_code"] = make_job_code("javaremote_rss", job["apply_url"])
    return jobs


def fetch_devopsboard_rss(query: str = "") -> List[dict]:
    """DevOps & Cloud Jobs RSS feed."""
    jobs = RSSFeedParser.parse_feed(
        "https://www.devopsboard.com/feed",
        "DevOps Jobs"
    )
    for job in jobs:
        job["job_code"] = make_job_code("devopsboard_rss", job["apply_url"])
    return jobs


def fetch_designjobs_rss(query: str = "") -> List[dict]:
    """Design Remote Jobs RSS feed."""
    jobs = RSSFeedParser.parse_feed(
        "https://www.designjobs.org/feed",
        "Design Jobs"
    )
    for job in jobs:
        job["job_code"] = make_job_code("designjobs_rss", job["apply_url"])
    return jobs


def fetch_marketingjobs_rss(query: str = "") -> List[dict]:
    """Marketing Remote Jobs RSS feed."""
    jobs = RSSFeedParser.parse_feed(
        "https://www.marketingjobs.io/feed",
        "Marketing Jobs"
    )
    for job in jobs:
        job["job_code"] = make_job_code("marketingjobs_rss", job["apply_url"])
    return jobs


def fetch_salesjobs_rss(query: str = "") -> List[dict]:
    """Sales Remote Jobs RSS feed."""
    jobs = RSSFeedParser.parse_feed(
        "https://www.salesjobs.io/feed",
        "Sales Jobs"
    )
    for job in jobs:
        job["job_code"] = make_job_code("salesjobs_rss", job["apply_url"])
    return jobs


def fetch_contentjobs_rss(query: str = "") -> List[dict]:
    """Content & Writing Remote Jobs RSS feed."""
    jobs = RSSFeedParser.parse_feed(
        "https://www.contentjobs.com/feed",
        "Content Jobs"
    )
    for job in jobs:
        job["job_code"] = make_job_code("contentjobs_rss", job["apply_url"])
    return jobs


def fetch_datajobs_rss(query: str = "") -> List[dict]:
    """Data Science & Analytics Jobs RSS feed."""
    jobs = RSSFeedParser.parse_feed(
        "https://www.datajobs.ai/feed",
        "Data Jobs"
    )
    for job in jobs:
        job["job_code"] = make_job_code("datajobs_rss", job["apply_url"])
    return jobs


def fetch_aijobs_rss(query: str = "") -> List[dict]:
    """AI & Machine Learning Jobs RSS feed."""
    jobs = RSSFeedParser.parse_feed(
        "https://www.aijobs.net/feed",
        "AI Jobs"
    )
    for job in jobs:
        job["job_code"] = make_job_code("aijobs_rss", job["apply_url"])
    return jobs


def fetch_securityjobs_rss(query: str = "") -> List[dict]:
    """Security & Cybersecurity Remote Jobs RSS feed."""
    jobs = RSSFeedParser.parse_feed(
        "https://www.securityjobs.net/feed",
        "Security Jobs"
    )
    for job in jobs:
        job["job_code"] = make_job_code("securityjobs_rss", job["apply_url"])
    return jobs


def fetch_vmjobs_rss(query: str = "") -> List[dict]:
    """Virtual Assistant & Support Jobs RSS feed."""
    jobs = RSSFeedParser.parse_feed(
        "https://www.virtualjobs.io/feed",
        "Virtual Jobs"
    )
    for job in jobs:
        job["job_code"] = make_job_code("vmjobs_rss", job["apply_url"])
    return jobs


def fetch_translatorjobs_rss(query: str = "") -> List[dict]:
    """Translation & Localization Remote Jobs RSS feed."""
    jobs = RSSFeedParser.parse_feed(
        "https://www.translatorjobs.com/feed",
        "Translator Jobs"
    )
    for job in jobs:
        job["job_code"] = make_job_code("translatorjobs_rss", job["apply_url"])
    return jobs


def fetch_educationjobs_rss(query: str = "") -> List[dict]:
    """Education & Tutoring Remote Jobs RSS feed."""
    jobs = RSSFeedParser.parse_feed(
        "https://www.educationjobs.org/feed",
        "Education Jobs"
    )
    for job in jobs:
        job["job_code"] = make_job_code("educationjobs_rss", job["apply_url"])
    return jobs


def fetch_businessjobs_rss(query: str = "") -> List[dict]:
    """Business Analyst & Strategy Jobs RSS feed."""
    jobs = RSSFeedParser.parse_feed(
        "https://www.businessjobs.io/feed",
        "Business Jobs"
    )
    for job in jobs:
        job["job_code"] = make_job_code("businessjobs_rss", job["apply_url"])
    return jobs


def fetch_projectmgmt_rss(query: str = "") -> List[dict]:
    """Project Management & PMO Jobs RSS feed."""
    jobs = RSSFeedParser.parse_feed(
        "https://www.projectmanagementjobs.io/feed",
        "Project Management Jobs"
    )
    for job in jobs:
        job["job_code"] = make_job_code("projectmgmt_rss", job["apply_url"])
    return jobs
