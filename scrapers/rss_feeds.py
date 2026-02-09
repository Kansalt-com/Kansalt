"""RSS feed scrapers for multiple job boards."""

from typing import List
from scrapers.rss_common import RSSFeedParser
from scrapers.common import make_job_code
from utils.logger import get_logger

logger = get_logger(__name__)


def fetch_wwr_rss(query: str = "") -> List[dict]:
    """We Work Remotely RSS feed."""
    jobs = RSSFeedParser.parse_feed(
        "https://weworkremotely.com/remote-jobs/feed",
        "We Work Remotely"
    )
    for job in jobs:
        job["job_code"] = make_job_code("wwr_rss", job["apply_url"])
    return jobs


def fetch_remotive_rss(query: str = "") -> List[dict]:
    """Remotive RSS feed."""
    jobs = RSSFeedParser.parse_feed(
        "https://remotive.io/remote-jobs/feed",
        "Remotive RSS"
    )
    for job in jobs:
        job["job_code"] = make_job_code("remotive_rss", job["apply_url"])
    return jobs


def fetch_jobscollider_rss(query: str = "") -> List[dict]:
    """Jobs Collider RSS feed."""
    jobs = RSSFeedParser.parse_feed(
        "https://feeds.jobscollider.com/feed",
        "Jobs Collider"
    )
    for job in jobs:
        job["job_code"] = make_job_code("jobscollider_rss", job["apply_url"])
    return jobs


def fetch_jobalign_rss(query: str = "") -> List[dict]:
    """JobAlign RSS feed."""
    jobs = RSSFeedParser.parse_feed(
        "https://jobalign.com/remote-jobs/feed",
        "JobAlign"
    )
    for job in jobs:
        job["job_code"] = make_job_code("jobalign_rss", job["apply_url"])
    return jobs


def fetch_workingviral_rss(query: str = "") -> List[dict]:
    """WorkingViral RSS feed."""
    jobs = RSSFeedParser.parse_feed(
        "https://workingviral.com/feeds/remote-jobs",
        "WorkingViral"
    )
    for job in jobs:
        job["job_code"] = make_job_code("workingviral_rss", job["apply_url"])
    return jobs


def fetch_jobicy_rss(query: str = "") -> List[dict]:
    """JobIcy RSS feed."""
    jobs = RSSFeedParser.parse_feed(
        "https://jobicy.com/?feed=rss2",
        "JobIcy"
    )
    for job in jobs:
        job["job_code"] = make_job_code("jobicy_rss", job["apply_url"])
    return jobs


def fetch_remoteca_rss(query: str = "") -> List[dict]:
    """RemoteCA RSS feed."""
    jobs = RSSFeedParser.parse_feed(
        "https://remote.ca/feed",
        "Remote.CA"
    )
    for job in jobs:
        job["job_code"] = make_job_code("remoteca_rss", job["apply_url"])
    return jobs


def fetch_authenticjobs_rss(query: str = "") -> List[dict]:
    """Authentic Jobs RSS feed."""
    jobs = RSSFeedParser.parse_feed(
        "https://www.authenticjobs.com/feed/",
        "Authentic Jobs"
    )
    for job in jobs:
        job["job_code"] = make_job_code("authenticjobs_rss", job["apply_url"])
    return jobs

