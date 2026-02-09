"""
Job fetcher orchestrator with multi-source aggregation, deduplication, scoring, and ranking.
"""
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone, timedelta
from typing import List, Optional, Set
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
    terms = []

    # Add selected skill labels
    for skill in selected_skills:
        terms.append(skill)
        # Add aliases from skills DB
        all_skills_flat = []
        for category in skills_db.get("categories", {}).values():
            for label, skill_info in category.items():
                if label == skill:
                    aliases = skill_info.get("aliases", [])
                    if isinstance(aliases, list):
                        terms.extend(aliases)
                    break

    # Add job profile tokens
    if job_profile:
        terms.append(job_profile)
        # Split profile into tokens
        import re
        tokens = re.findall(r"[a-z0-9\+\#\./-]+", job_profile.lower())
        terms.extend(tokens)

    # Add manual terms
    terms.extend(manual_terms)

    # Normalize and deduplicate
    cleaned, seen = [], set()
    for t in terms:
        t = str(t).strip().lower() if t else ""
        if len(t) >= 2 and t not in seen:
            seen.add(t)
            cleaned.append(t)

    return cleaned


def _score_job(
    job: dict,
    search_terms: List[str],
    job_profile: str,
    skills_db: dict,
) -> dict:
    """
    Score job based on:
    1. Match score: % of search terms found
    2. Freshness score: time-decay based on posted_at
    """
    title = job.get("title", "") or ""
    description = job.get("description_text", "") or ""
    company = job.get("company", "") or ""
    tags = job.get("tags", []) or []

    tags_text = " ".join([str(t) for t in tags if isinstance(t, str)])
    full_text = f"{title} {description} {company} {tags_text}".lower()

    # Profile gating: if profile is specified, prefer jobs with profile tokens, but don't filter out completely
    if job_profile:
        job_profile_lower = job_profile.lower()
        title_desc = f"{title} {description}".lower()
        has_profile_match = job_profile_lower in title_desc
        if not has_profile_match:
            # Check individual tokens
            import re
            profile_tokens = re.findall(r"[a-z0-9\+\#\./-]+", job_profile_lower)
            has_profile_match = any(token in title_desc for token in profile_tokens if len(token) > 2)
        
        # Don't gate based on profile alone - let skill matching determine relevance
        # (profile_match will be used for ranking preference)

    # Skill matching
    matched = set()
    for term in search_terms:
        if SkillMatcher.contains_term(full_text, term):
            matched.add(term)

    match_score = int(round((len(matched) / max(1, len(set(search_terms)))) * 100)) if search_terms else 0

    # Infer additional skills from description if no tags
    if not tags:
        inferred = SkillMatcher.infer_skills_strict(full_text, skills_db)
        job["tags"] = inferred

    # Freshness score
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

    # Sort by rank descending
    jobs.sort(key=lambda x: x.get("rank_score", 0), reverse=True)
    return jobs


def _filter_by_date(jobs: List[dict], date_filter: str) -> List[dict]:
    """Filter jobs by posted date."""
    if not date_filter or date_filter == "all":
        return jobs

    now = datetime.now(timezone.utc)
    cutoff_map = {
        "24h": now - timedelta(days=1),
        "1w": now - timedelta(days=7),
        "2w": now - timedelta(days=14),
        "1m": now - timedelta(days=30),
    }

    cutoff = cutoff_map.get(date_filter)
    if not cutoff:
        return jobs

    filtered = []
    for job in jobs:
        if not job.get("posted_at_iso"):
            continue  # Skip jobs without dates
        try:
            dt = datetime.fromisoformat(job["posted_at_iso"].replace("Z", "+00:00"))
            if dt.tzinfo is None:
                dt = dt.replace(tzinfo=timezone.utc)
            if dt >= cutoff:
                filtered.append(job)
        except Exception:
            continue

    return filtered


def _filter_by_location(jobs: List[dict], locations: List[str]) -> List[dict]:
    """Filter jobs by location."""
    if not locations or "all" in [loc.lower() for loc in locations]:
        return jobs

    locations_lower = [loc.lower() for loc in locations]
    filtered = []

    for job in jobs:
        job_location = job.get("location", "").lower()
        is_remote = job.get("is_remote", False)

        # Remote matches if job is remote OR location is remote
        if "remote" in locations_lower:
            if is_remote or "remote" in job_location:
                filtered.append(job)
                continue

        # Otherwise check exact location match
        if any(loc in job_location for loc in locations_lower if loc != "remote"):
            filtered.append(job)

    return filtered


def fetch_all_jobs(
    selected_skills: List[str],
    skills_db: dict,
    job_profile: str = "",
    locations: Optional[List[str]] = None,
    manual_terms: Optional[List[str]] = None,
    date_filter: str = "all",
    min_match: int = 0,
    max_results: int = 200,
    match_weight: int = 60,
    freshness_weight: int = 40,
    stream_callback = None,
) -> List[dict]:
    """
    Main orchestrator: fetch from all sources, deduplicate, score, rank.
    Optional stream_callback for real-time results: callback(jobs_so_far, source_name)
    """
    # Validate input
    if not selected_skills and not job_profile.strip() and not manual_terms:
        logger.warning("No search criteria provided")
        return []

    logger.info(
        f"Starting job fetch: skills={selected_skills}, profile={job_profile}, "
        f"locations={locations}, manual_terms={manual_terms}"
    )

    # Expand search terms
    search_terms = _expand_search_terms(selected_skills, skills_db, job_profile, manual_terms or [])

    # Check cache
    cache_key = f"jobs_{hash(tuple(sorted(search_terms)))}"
    cached_jobs = CacheManager.get(cache_key)
    if cached_jobs:
        logger.info(f"Using cached jobs (key: {cache_key})")
        return cached_jobs[:max_results]

    # Parallel fetch from all sources with streaming
    all_jobs = []
    seen: Set[str] = set()
    unique_jobs = []
    scored_jobs = []
    
    # Use first search term or empty string
    query_string = search_terms[0] if search_terms else ""
    
    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = {executor.submit(_safe_call, fn, query_string): name for name, fn in SOURCES}
        
        for future in as_completed(futures):
            try:
                source_name = futures[future]
                jobs = future.result() or []
                
                # Process jobs from this source immediately
                for job in jobs:
                    unique_id = job.get("job_code") or (job.get("apply_url") + "_" + job.get("title"))
                    if unique_id not in seen:
                        seen.add(unique_id)
                        unique_jobs.append(job)
                        
                        # Score the job
                        scored_job = _score_job(job, search_terms, job_profile, skills_db)
                        if scored_job.get("match_score", 0) >= min_match:
                            scored_jobs.append(scored_job)
                
                # Stream callback for UI update
                if stream_callback and scored_jobs:
                    ranked = _rank_jobs(scored_jobs[-len(jobs):] if len(scored_jobs) >= len(jobs) else scored_jobs, match_weight, freshness_weight)
                    stream_callback(scored_jobs, source_name)
                    
            except Exception as e:
                logger.error(f"Scraper execution error: {e}")

    logger.info(f"Fetched {len(all_jobs)} jobs from all sources (before dedup)")
    logger.info(f"After dedup: {len(unique_jobs)} unique jobs")
    logger.info(f"After scoring (min_match={min_match}): {len(scored_jobs)} jobs")

    # Rank all scored jobs
    ranked_jobs = _rank_jobs(scored_jobs, match_weight, freshness_weight)

    # Filter by date
    date_filtered = _filter_by_date(ranked_jobs, date_filter)
    logger.info(f"After date filter ({date_filter}): {len(date_filtered)} jobs")

    # Filter by location
    location_filtered = _filter_by_location(date_filtered, locations or ["remote"])
    logger.info(f"After location filter: {len(location_filtered)} jobs")

    # Limit to max_results
    final_jobs = location_filtered[:max_results]

    # Cache results
    CacheManager.set(cache_key, final_jobs, ttl_minutes=20)

    logger.info(f"Final results: {len(final_jobs)} jobs")
    return final_jobs
