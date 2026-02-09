"""
Common RSS feed parsing utilities.
"""
import feedparser
from typing import Optional
from scrapers.common import parse_iso_date, relative_time, clean_text
from utils.logger import get_logger

logger = get_logger(__name__)


class RSSFeedParser:
    """Common RSS feed parser."""

    @staticmethod
    def parse_feed(feed_url: str, source_name: str) -> list:
        """
        Parse RSS feed and return normalized jobs.
        """
        try:
            feed = feedparser.parse(feed_url)

            if feed.bozo:
                logger.warning(f"RSS feed parsing warning for {source_name}: {feed.bozo_exception}")

            jobs = []
            for entry in feed.entries[:100]:  # Limit to 100 entries
                try:
                    title = entry.get("title", "").strip()
                    if not title:
                        continue

                    # Try to extract company
                    company = ""
                    if "author" in entry:
                        company = entry["author"].strip()
                    elif "source" in entry:
                        company = entry["source"].get("title", "").strip()

                    # Description
                    description = ""
                    if "summary" in entry:
                        description = clean_text(entry["summary"])
                    elif "description" in entry:
                        description = clean_text(entry["description"])

                    # Published date
                    posted_at_iso = None
                    if "published" in entry:
                        posted_at_iso = parse_iso_date(entry["published"])
                    elif "updated" in entry:
                        posted_at_iso = parse_iso_date(entry["updated"])

                    posted_at_human = relative_time(posted_at_iso)

                    job_obj = {
                        "title": title,
                        "company": company,
                        "location": "Remote",  # Most RSS feeds are remote
                        "is_remote": True,
                        "posted_at_iso": posted_at_iso,
                        "posted_at_human": posted_at_human,
                        "source_name": source_name,
                        "apply_url": entry.get("link", ""),
                        "description_text": description,
                        "tags": [],
                    }

                    jobs.append(job_obj)

                except Exception as e:
                    logger.warning(f"RSS entry parse error for {source_name}: {e}")
                    continue

            logger.info(f"RSS {source_name}: fetched {len(jobs)} jobs")
            return jobs

        except Exception as e:
            logger.error(f"RSS feed error for {source_name}: {e}")
            return []
