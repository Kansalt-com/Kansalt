"""
Job fetcher orchestrator with multi-source aggregation, deduplication, scoring, ranking,
and strict filtering to remove blog/editorial content (e.g., AuthenticJobs "how-to" posts).

KEY FIXES:
1) Query building: use job_profile as the main query (not just the first token).
2) Strict job-post validation: drop blog/articles/newsletters/etc before scoring.
3) Keep streaming snapshots while ALL sources are fetched (no early-return).
4) Cache only final aggregated results (prevents “Remotive-only cache” poisoning).
"""

from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone, timedelta
from typing import Callable, Dict, List, Optional, Set
import time
import re

from services.skill_engine import SkillMatcher
from scrapers.remotive_api import fetch_remotive_api
from scrapers.arbeitnow_api import fetch_arbeitnow_api
from scrapers.himalayas_api import fetch_himalayas_api
from scrapers.rss_feeds import (
    fetch_wwr_rss,
    fetch_remotive_rss,
    fetch_jobscollider_rss,
    fetch_jobalign_rss,
    fetch_workingviral_rss,
    fetch_jobicy_rss,
    fetch_remoteca_rss,
    fetch_authenticjobs_rss,
)
from scrapers.rss_feeds_extended import (
    fetch_stackoverflow_rss,
    fetch_github_rss,
    fetch_developerjob_rss,
    fetch_flexjobs_rss,
    fetch_nofluff_rss,
    fetch_weworkpython_rss,
    fetch_javascript_rss,
    fetch_rubyonrails_rss,
    fetch_golangjobs_rss,
    fetch_rustiocean_rss,
    fetch_javaremote_rss,
    fetch_devopsboard_rss,
    fetch_designjobs_rss,
    fetch_marketingjobs_rss,
    fetch_salesjobs_rss,
    fetch_contentjobs_rss,
    fetch_datajobs_rss,
    fetch_aijobs_rss,
    fetch_securityjobs_rss,
    fetch_vmjobs_rss,
    fetch_translatorjobs_rss,
    fetch_educationjobs_rss,
    fetch_businessjobs_rss,
    fetch_projectmgmt_rss,
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
    terms: List[str] = []

    for skill in selected_skills:
        terms.append(skill)
        cats = (skills_db or {}).get("categories", {}) or {}
        for category in cats.values():
            if not isinstance(category, dict):
                continue
            for label, skill_info in category.items():
                if label == skill:
                    aliases = (skill_info or {}).get("aliases", [])
                    if isinstance(aliases, list):
                        terms.extend([str(a) for a in aliases])
                    break

    if job_profile:
        terms.append(job_profile)
        tokens = re.findall(r"[a-z0-9\+\#\./-]+", job_profile.lower())
        terms.extend(tokens)

    terms.extend(manual_terms)

    cleaned: List[str] = []
    seen = set()
    for t in terms:
        t = str(t).strip().lower() if t else ""
        if len(t) >= 2 and t not in seen:
            seen.add(t)
            cleaned.append(t)

    return cleaned


def _build_query_string(search_terms: List[str], job_profile: str, manual_terms: List[str]) -> str:
    """
    Build a strong query for sources.
    FIX: previously you used only search_terms[0], which is too weak and causes junk matches.
    """
    profile = (job_profile or "").strip()
    if profile:
        return profile  # best query

    # fallback: join top terms (keep it short)
    terms = []
    for t in search_terms:
        if t and t not in terms:
            terms.append(t)
        if len(terms) >= 3:
            break

    if not terms and manual_terms:
        terms = [m.strip() for m in manual_terms if m.strip()][:3]

    return " ".join(terms).strip()


def _normalize_apply_url(job: dict) -> str:
    return (
        job.get("apply_url")
        or job.get("job_url")
        or job.get("url")
        or job.get("link")
        or ""
    )


def _is_real_job_post(job: dict) -> bool:
    """
    Strict validation to remove blog/editorial content.
    Designed to kill things like:
    - AuthenticJobs "How to..." posts
    - Editorial Staff company
    - /blog /how-to /guide URLs
    """
    title = (job.get("title") or "").strip()
    company = (job.get("company") or "").strip()
    url = _normalize_apply_url(job).strip()

    t = title.lower()
    c = company.lower()
    u = url.lower()

    # Must have a usable URL
    if not u or len(u) < 15:
        return False

    # Block obvious content URLs
    blocked_url_keywords = [
        "/blog",
        "/article",
        "/how-to",
        "/guide",
        "/tips",
        "/stories",
        "/newsletter",
        "/podcast",
        "/category",
        "/tag",
        "/news",
        "/insights",
    ]
    if any(k in u for k in blocked_url_keywords):
        return False

    # Block editorial pseudo-company
    if "editorial staff" in c:
        return False

    # Block content-style titles
    blocked_title_patterns = [
        "how to",
        "guide",
        "complete guide",
        "top ",
        "career transition",
        "revolution",
        "insights",
        "trends",
        "best ",
        "tips",
        "tutorial",
        "what is",
    ]
    if any(p in t for p in blocked_title_patterns):
        return False

    # Title should resemble a role (broad set)
    role_indicators = [
        "engineer",
        "developer",
        "manager",
        "designer",
        "editor",
        "video editor",
        "producer",
        "animator",
        "motion",
        "videographer",
        "analyst",
        "specialist",
        "lead",
        "architect",
        "consultant",
        "officer",
        "coordinator",
        "assistant",
        "executive",
        "writer",
        "content",
        "marketer",
        "marketing",
        "sales",
        "hr",
        "recruiter",
        "accountant",
    ]
    if not any(w in t for w in role_indicators):
        return False

    # Tiny descriptions are often blog excerpts (keep len low to not kill real short posts)
    desc = (job.get("description_text") or "").strip()
    if desc and len(desc) < 40:
        return False

    return True


def _score_job(job: dict, search_terms: List[str], job_profile: str, skills_db: dict) -> dict:
    """
    Score job based on:
    1) Match score: % of search terms found
    2) Freshness score: time-decay based on posted_at
    """
    title = job.get("title", "") or ""
    description = job.get("description_text", "") or ""
    company = job.get("company", "") or ""
    tags = job.get("tags", []) or []

    tags_text = " ".join([str(t) for t in tags if isinstance(t, str)])
    full_text = f"{title} {description} {company} {tags_text}".lower()

    matched = set()
    for term in search_terms:
        if SkillMatcher.contains_term(full_text, term):
            matched.add(term)

    match_score = int(round((len(matched) / max(1, len(set(search_terms)))) * 100)) if search_terms else 0

    # Infer tags if missing
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
    job["apply_url"] = _normalize_apply_url(job)
    return job


def _rank_jobs(jobs: List[dict], match_weight: int = 60, freshness_weight: int = 40) -> List[dict]:
    for job in jobs:
        rank = int(
            (job.get("match_score", 0) * match_weight + job.get("freshness_score", 0) * freshness_weight) / 100
        )
        job["rank_score"] = rank
    jobs.sort(key=lambda x: x.get("rank_score", 0), reverse=True)
    return jobs


def _filter_by_date(jobs: List[dict], date_filter: str) -> List[dict]:
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
        iso = job.get("posted_at_iso")
        if not iso:
            continue
        try:
            dt = datetime.fromisoformat(iso.replace("Z", "+00:00"))
            if dt.tzinfo is None:
                dt = dt.replace(tzinfo=timezone.utc)
            if dt >= cutoff:
                filtered.append(job)
        except Exception:
            continue
    return filtered


def _filter_by_location(jobs: List[dict], locations: List[str]) -> List[dict]:
    if not locations:
        return jobs

    locations_lower = [loc.lower().strip() for loc in locations if loc]
    if "all" in locations_lower:
        return jobs

    filtered = []
    for job in jobs:
        job_location = (job.get("location", "") or "").lower()
        is_remote = bool(job.get("is_remote", False))

        if "remote" in locations_lower:
            if is_remote or "remote" in job_location:
                filtered.append(job)
                continue

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
    stream_callback: Optional[Callable[[List[dict], str], None]] = None,
) -> List[dict]:
    """
    Fetch jobs from all sources.
    - Streams snapshots via stream_callback as sources complete.
    - Returns final aggregated jobs list after all sources complete.
    """
    manual_terms = manual_terms or []
    locations = locations or ["all"]

    if not selected_skills and not job_profile.strip() and not manual_terms:
        logger.warning("No search criteria provided")
        return []

    logger.info(
        f"Starting job fetch: skills={selected_skills}, profile={job_profile}, locations={locations}, manual_terms={manual_terms}"
    )

    search_terms = _expand_search_terms(selected_skills, skills_db, job_profile, manual_terms)
    query_string = _build_query_string(search_terms, job_profile, manual_terms)

    # More accurate cache key (includes locations/date/min_match)
    cache_key = f"jobs_{hash(tuple(sorted(search_terms)))}_{hash(tuple(sorted([l.lower() for l in locations])))}_{date_filter}_{min_match}"
    cached_jobs = CacheManager.get(cache_key)
    if cached_jobs:
        logger.info(f"Using cached jobs (key: {cache_key})")
        return cached_jobs[:max_results]

    seen: Set[str] = set()
    scored_jobs: List[dict] = []
    source_stats = []
    start_time = time.time()

    MAX_WORKERS = 12
    GLOBAL_MAX_SECONDS = 45  # safety cutoff

    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        futures = {}

        for name, fn in SOURCES:
            def safe_fetch(func, query, _name=name):
                t0 = time.time()
                jobs = _safe_call(func, query)
                elapsed = time.time() - t0
                return {"jobs": jobs, "elapsed": elapsed}

            futures[executor.submit(safe_fetch, fn, query_string)] = name

        for future in as_completed(futures):
            source_name = futures[future]

            try:
                result = future.result()
            except Exception as e:
                logger.error(f"Source {source_name} crashed: {e}")
                result = {"jobs": [], "elapsed": 0}

            jobs = result.get("jobs", []) or []
            elapsed_src = float(result.get("elapsed", 0))
            source_stats.append((source_name, elapsed_src, len(jobs)))
            logger.debug(f"Source {source_name} returned {len(jobs)} items in {elapsed_src:.2f}s")

            # Process jobs from this source
            for job in jobs:
                # Normalize URL early
                job["apply_url"] = _normalize_apply_url(job)

                # HARD FILTER: remove blog/editorial junk
                if not _is_real_job_post(job):
                    continue

                unique_id = job.get("job_code") or ((job.get("apply_url") or "") + "_" + (job.get("title") or ""))
                if unique_id in seen:
                    continue
                seen.add(unique_id)

                scored_job = _score_job(job, search_terms, job_profile, skills_db)
                if int(scored_job.get("match_score", 0) or 0) >= int(min_match):
                    scored_jobs.append(scored_job)

            # Snapshot for UI
            ranked = _rank_jobs(scored_jobs[:], match_weight, freshness_weight)
            ranked = _filter_by_date(ranked, date_filter)
            ranked = _filter_by_location(ranked, locations)
            snapshot = ranked[:max_results]

            if stream_callback:
                try:
                    stream_callback(snapshot, source_name)
                except Exception:
                    logger.debug("stream_callback raised", exc_info=True)

            # Safety cutoff
            if time.time() - start_time > GLOBAL_MAX_SECONDS:
                logger.warning("Global fetch exceeded 45s; returning best-effort results.")
                break

    # Finalize
    ranked_jobs = _rank_jobs(scored_jobs, match_weight, freshness_weight)
    ranked_jobs = _filter_by_date(ranked_jobs, date_filter)
    ranked_jobs = _filter_by_location(ranked_jobs, locations)
    final_jobs = ranked_jobs[:max_results]

    CacheManager.set(cache_key, final_jobs, ttl_minutes=20)

    try:
        slow_sorted = sorted(source_stats, key=lambda x: x[1], reverse=True)[:12]
        logger.info("Top slow sources (name,sec,count): %s", slow_sorted)
    except Exception:
        pass

    logger.info(f"Final results: {len(final_jobs)} jobs from {len(SOURCES)} sources")
    return final_jobs
