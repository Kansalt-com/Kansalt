"""
Streaming job fetcher for real-time results display.
Yields results as they arrive from sources.
"""
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import List, Optional, Generator, Set
from datetime import datetime, timezone, timedelta
from services.skill_engine import SkillMatcher
from scrapers.remotive_api import fetch_remotive_api
from scrapers.arbeitnow_api import fetch_arbeitnow_api
from scrapers.himalayas_api import fetch_himalayas_api
from scrapers.rss_feeds import (
    fetch_wwr_rss, fetch_remotive_rss, fetch_jobscollider_rss,
    fetch_jobalign_rss, fetch_workingviral_rss, fetch_jobicy_rss,
    fetch_remoteca_rss, fetch_authenticjobs_rss
)
from scrapers.rss_feeds_extended import (
    fetch_stackoverflow_rss, fetch_github_rss, fetch_developerjob_rss,
    fetch_flexjobs_rss, fetch_nofluff_rss, fetch_weworkpython_rss,
    fetch_javascript_rss, fetch_rubyonrails_rss, fetch_golangjobs_rss,
    fetch_rustiocean_rss, fetch_javaremote_rss, fetch_devopsboard_rss,
    fetch_designjobs_rss, fetch_marketingjobs_rss, fetch_salesjobs_rss,
    fetch_contentjobs_rss, fetch_datajobs_rss, fetch_aijobs_rss,
    fetch_securityjobs_rss, fetch_vmjobs_rss, fetch_translatorjobs_rss,
    fetch_educationjobs_rss, fetch_businessjobs_rss, fetch_projectmgmt_rss
)
from utils.cache import CacheManager
from utils.logger import get_logger

logger = get_logger(__name__)

# All scraper sources (30+ job boards)
SOURCES = [
    ("RemotiveAPI", fetch_remotive_api),
    ("ArbeitNow", fetch_arbeitnow_api),
    ("Himalayas", fetch_himalayas_api),
    ("WeworkRemotely", fetch_wwr_rss),
    ("RemotiveRSS", fetch_remotive_rss),
    ("JobsCollider", fetch_jobscollider_rss),
    ("JobAlign", fetch_jobalign_rss),
    ("WorkingViral", fetch_workingviral_rss),
    ("JobIcy", fetch_jobicy_rss),
    ("RemoteCA", fetch_remoteca_rss),
    ("AuthenticJobs", fetch_authenticjobs_rss),
    ("StackOverflow", fetch_stackoverflow_rss),
    ("GitHub", fetch_github_rss),
    ("DeveloperJob", fetch_developerjob_rss),
    ("FlexJobs", fetch_flexjobs_rss),
    ("NoFluffJobs", fetch_nofluff_rss),
    ("PythonJobs", fetch_weworkpython_rss),
    ("JavaScriptJobs", fetch_javascript_rss),
    ("RubyOnRails", fetch_rubyonrails_rss),
    ("GolangJobs", fetch_golangjobs_rss),
    ("RustJobs", fetch_rustiocean_rss),
    ("JavaJobs", fetch_javaremote_rss),
    ("DevOpsJobs", fetch_devopsboard_rss),
    ("DesignJobs", fetch_designjobs_rss),
    ("MarketingJobs", fetch_marketingjobs_rss),
    ("SalesJobs", fetch_salesjobs_rss),
    ("ContentJobs", fetch_contentjobs_rss),
    ("DataJobs", fetch_datajobs_rss),
    ("AIJobs", fetch_aijobs_rss),
    ("SecurityJobs", fetch_securityjobs_rss),
    ("VirtualJobs", fetch_vmjobs_rss),
    ("TranslatorJobs", fetch_translatorjobs_rss),
    ("EducationJobs", fetch_educationjobs_rss),
    ("BusinessJobs", fetch_businessjobs_rss),
    ("ProjectMgmtJobs", fetch_projectmgmt_rss),
]


def _safe_call(fn, query: str = "") -> List[dict]:
    """Safely call scraper with query, return empty list on error."""
    try:
        return fn(query) or []
    except Exception as e:
        logger.error(f"Scraper error: {type(e).__name__}: {e}")
        return []


def _expand_search_terms(
    selected_skills: List[str],
    skills_db: dict,
    job_profile: str,
    manual_terms: List[str],
) -> List[str]:
    """Expand search terms from skills + profile + manual input."""
    terms = set(manual_terms)
    
    for skill in selected_skills:
        if skill in skills_db.get("all_skills", []):
            terms.add(skill)
    
    if job_profile.strip():
        for word in job_profile.lower().split():
            if len(word) > 2:
                terms.add(word)
    
    return sorted(list(terms))


def _score_job(
    job: dict,
    search_terms: List[str],
    job_profile: str,
    skills_db: dict,
) -> dict:
    """Score a job based on search criteria."""
    title = job.get("title", "").lower()
    description = job.get("description_text", "").lower()
    tags = job.get("tags", [])
    full_text = f"{title} {description} {' '.join(tags)}".lower()

    profile_match = False
    if job_profile:
        job_profile_lower = job_profile.lower()
        title_desc = f"{title} {description}".lower()
        has_profile_match = job_profile_lower in title_desc
        if not has_profile_match:
            import re
            profile_tokens = re.findall(r"[a-z0-9\+\#\./-]+", job_profile_lower)
            has_profile_match = any(token in title_desc for token in profile_tokens if len(token) > 2)
        profile_match = has_profile_match

    matched = set()
    for term in search_terms:
        if SkillMatcher.contains_term(full_text, term):
            matched.add(term)

    match_score = int(round((len(matched) / max(1, len(set(search_terms)))) * 100)) if search_terms else 0

    if not tags:
        inferred = SkillMatcher.infer_skills_strict(full_text, skills_db)
        job["tags"] = inferred

    freshness = 10
    if job.get("posted_at_iso"):
        try:
            dt = datetime.fromisoformat(job["posted_at_iso"].replace("Z", "+00:00"))
            if dt.tzinfo is None:
                dt = dt.replace(tzinfo=timezone.utc)
            now = datetime.now(timezone.utc)
            days = max(0.0, (now - dt).total_seconds() / 86400.0)

            if days <= 1:
                freshness = 100
            elif days <= 7:
                freshness = int(100 - (days - 1) * 5)
            elif days <= 30:
                freshness = int(70 - (days - 7) * 1.7)
            else:
                freshness = max(0, int(30 - (days - 30) * 0.5))
        except Exception:
            freshness = 10

    job["match_score"] = match_score
    job["matched_skills"] = sorted(list(matched))
    job["freshness_score"] = freshness
    job["profile_match"] = profile_match

    return job


def _rank_jobs(
    jobs: List[dict],
    match_weight: int = 60,
    freshness_weight: int = 40,
) -> List[dict]:
    """Rank jobs by weighted combination of match + freshness."""
    for job in jobs:
        rank = int(
            (job.get("match_score", 0) * match_weight + job.get("freshness_score", 0) * freshness_weight) / 100
        )
        job["rank_score"] = rank
    return sorted(jobs, key=lambda x: (-x.get("rank_score", 0), -x.get("match_score", 0)))


def fetch_jobs_streaming(
    selected_skills: List[str],
    skills_db: dict,
    job_profile: str = "",
    locations: Optional[List[str]] = None,
    manual_terms: Optional[List[str]] = None,
    date_filter: str = "all",
    min_match: int = 0,
    match_weight: int = 60,
    freshness_weight: int = 40,
) -> Generator[tuple[str, List[dict]], None, None]:
    """
    Stream jobs as they arrive from sources.
    Yields: (source_name, jobs_list_so_far)
    """
    if not selected_skills and not job_profile.strip() and not manual_terms:
        logger.warning("No search criteria provided")
        return

    logger.info(
        f"Starting streaming job fetch: skills={selected_skills}, profile={job_profile}"
    )

    search_terms = _expand_search_terms(selected_skills, skills_db, job_profile, manual_terms or [])
    query_string = search_terms[0] if search_terms else ""
    
    seen: Set[str] = set()
    all_jobs = []
    scored_jobs = []
    
    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = {executor.submit(_safe_call, fn, query_string): name for name, fn in SOURCES}
        
        for future in as_completed(futures):
            try:
                source_name = futures[future]
                jobs = future.result() or []
                
                # Process jobs from this source
                new_jobs = []
                for job in jobs:
                    unique_id = job.get("job_code") or (job.get("apply_url") + "_" + job.get("title"))
                    if unique_id not in seen:
                        seen.add(unique_id)
                        
                        # Score the job
                        scored_job = _score_job(job, search_terms, job_profile, skills_db)
                        if scored_job.get("match_score", 0) >= min_match:
                            scored_jobs.append(scored_job)
                            new_jobs.append(scored_job)
                
                # Rank and yield current results
                if scored_jobs:
                    ranked = _rank_jobs(scored_jobs, match_weight, freshness_weight)
                    yield (source_name, ranked)
                    
            except Exception as e:
                logger.error(f"Scraper execution error: {e}")
