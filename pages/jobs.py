from __future__ import annotations

import html
import json
import math
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import streamlit as st

from pages.ui_kit import empty_state, render_hero
from services.job_fetcher import fetch_all_jobs


DATA_SKILLS_PATH = Path("data") / "skills.json"
STATE_KEYS = {
    "profile": "jobs_profile",
    "manual": "jobs_manual_terms",
    "skills": "jobs_selected_skills",
    "locations": "jobs_locations",
    "date": "jobs_date_filter",
    "min_match": "jobs_min_match",
    "sort": "jobs_sort",
    "results": "jobs_results",
    "page": "jobs_page",
    "signature": "jobs_filter_signature",
}


def _init_state() -> None:
    defaults = {
        STATE_KEYS["profile"]: "",
        STATE_KEYS["manual"]: "",
        STATE_KEYS["skills"]: [],
        STATE_KEYS["locations"]: ["all"],
        STATE_KEYS["date"]: "all",
        STATE_KEYS["min_match"]: 0,
        STATE_KEYS["sort"]: "Best match",
        STATE_KEYS["results"]: [],
        STATE_KEYS["page"]: 1,
        STATE_KEYS["signature"]: "",
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def _load_skills_db_safely() -> dict:
    if not DATA_SKILLS_PATH.exists():
        return {"categories": {}}

    try:
        payload = json.loads(DATA_SKILLS_PATH.read_text(encoding="utf-8"))
    except Exception:
        return {"categories": {}}

    if isinstance(payload, dict) and "categories" in payload and isinstance(payload["categories"], dict):
        return payload

    if isinstance(payload, dict) and isinstance(payload.get("skills"), list):
        return {"categories": {"General": {str(item): {} for item in payload["skills"] if str(item).strip()}}}

    if isinstance(payload, list):
        return {"categories": {"General": {str(item): {} for item in payload if str(item).strip()}}}

    return {"categories": {}}


def _skills_from_db(skills_db: dict) -> List[str]:
    labels: List[str] = []
    categories = skills_db.get("categories", {}) if isinstance(skills_db, dict) else {}

    if isinstance(categories, dict):
        for cat in categories.values():
            if isinstance(cat, dict):
                for label in cat.keys():
                    clean = str(label).strip()
                    if clean:
                        labels.append(clean)

    if labels:
        return sorted(set(labels))

    return sorted(
        {
            "Python",
            "JavaScript",
            "React",
            "Node.js",
            "SQL",
            "Data Analysis",
            "DevOps",
            "AWS",
            "Azure",
            "Docker",
            "Kubernetes",
            "Figma",
            "UI/UX",
            "SEO",
            "Content Writing",
            "Digital Marketing",
        }
    )


def _normalize_apply_url(job: Dict[str, Any]) -> str:
    return str(
        job.get("apply_url")
        or job.get("job_url")
        or job.get("url")
        or job.get("link")
        or ""
    ).strip()


def _format_posted_ago(posted_at_iso: Optional[str]) -> str:
    if not posted_at_iso:
        return "Unknown"
    try:
        dt = datetime.fromisoformat(str(posted_at_iso).replace("Z", "+00:00"))
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        now = datetime.now(timezone.utc)
        seconds = max(0, int((now - dt).total_seconds()))
        if seconds < 3600:
            return f"{max(1, seconds // 60)} mins ago"
        if seconds < 86400:
            return f"{seconds // 3600} hrs ago"
        return f"{seconds // 86400} days ago"
    except Exception:
        return "Unknown"


def _looks_like_blog(job: Dict[str, Any]) -> bool:
    title = str(job.get("title", "")).lower()
    company = str(job.get("company", "")).lower()
    url = _normalize_apply_url(job).lower()

    if "editorial staff" in company:
        return True

    blocked_title_tokens = ["how to", "guide", "tips", "tutorial", "complete guide", "what is"]
    if any(token in title for token in blocked_title_tokens):
        return True

    blocked_url_tokens = ["/blog", "/article", "/guide", "/tips", "/news", "/insights", "/category", "/tag"]
    if any(token in url for token in blocked_url_tokens):
        return True

    return False


def _query_signature() -> Tuple[Any, ...]:
    return (
        str(st.session_state.get(STATE_KEYS["profile"], "")).strip().lower(),
        str(st.session_state.get(STATE_KEYS["manual"], "")).strip().lower(),
        tuple(sorted(str(item).lower() for item in st.session_state.get(STATE_KEYS["skills"], []))),
        tuple(sorted(str(item).lower() for item in st.session_state.get(STATE_KEYS["locations"], []))),
        str(st.session_state.get(STATE_KEYS["date"], "all")),
        int(st.session_state.get(STATE_KEYS["min_match"], 0)),
        str(st.session_state.get(STATE_KEYS["sort"], "Best match")),
    )


def _sort_jobs(jobs: List[Dict[str, Any]], sort_by: str) -> List[Dict[str, Any]]:
    if sort_by == "Newest":
        def newest_key(item: Dict[str, Any]) -> float:
            value = item.get("posted_at_iso")
            try:
                dt = datetime.fromisoformat(str(value).replace("Z", "+00:00"))
                if dt.tzinfo is None:
                    dt = dt.replace(tzinfo=timezone.utc)
                return dt.timestamp()
            except Exception:
                return 0.0

        return sorted(jobs, key=newest_key, reverse=True)

    if sort_by == "Match score":
        return sorted(jobs, key=lambda x: int(x.get("match_score", 0) or 0), reverse=True)

    return sorted(jobs, key=lambda x: int(x.get("rank_score", x.get("match_score", 0)) or 0), reverse=True)


def _apply_ui_filters(jobs: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    profile = str(st.session_state.get(STATE_KEYS["profile"], "")).strip().lower()
    manual = str(st.session_state.get(STATE_KEYS["manual"], "")).strip().lower()
    selected_skills = [str(skill).lower() for skill in st.session_state.get(STATE_KEYS["skills"], [])]
    locations = [str(loc).lower() for loc in st.session_state.get(STATE_KEYS["locations"], ["all"])]
    min_match = int(st.session_state.get(STATE_KEYS["min_match"], 0))

    manual_terms = [term.strip() for term in manual.split(",") if term.strip()]

    filtered: List[Dict[str, Any]] = []
    for job in jobs:
        if _looks_like_blog(job):
            continue

        score = int(job.get("match_score", 0) or 0)
        if score < min_match:
            continue

        location_text = str(job.get("location", "")).lower()
        is_remote = bool(job.get("is_remote", False)) or "remote" in location_text

        if "all" not in locations:
            remote_selected = "remote" in locations
            loc_selected = [loc for loc in locations if loc not in {"all", "remote"}]

            location_ok = False
            if remote_selected and is_remote:
                location_ok = True
            if loc_selected and any(loc in location_text for loc in loc_selected):
                location_ok = True
            if not location_ok:
                continue

        searchable = " ".join(
            [
                str(job.get("title", "")),
                str(job.get("company", "")),
                str(job.get("description_text", "")),
                " ".join(str(tag) for tag in job.get("tags", []) if str(tag).strip()),
            ]
        ).lower()

        if profile:
            tokens = [tok for tok in profile.split() if len(tok) >= 3]
            if tokens and not any(tok in searchable for tok in tokens):
                continue

        if selected_skills and not any(skill in searchable for skill in selected_skills):
            continue

        if manual_terms and not any(term in searchable for term in manual_terms):
            continue

        filtered.append(job)

    return filtered


def _paginate(items: List[Dict[str, Any]], page: int, per_page: int) -> Tuple[List[Dict[str, Any]], int]:
    total_pages = max(1, math.ceil(len(items) / max(per_page, 1)))
    page = max(1, min(page, total_pages))
    start = (page - 1) * per_page
    end = start + per_page
    return items[start:end], total_pages


def _render_job_card(job: Dict[str, Any], idx: int) -> None:
    title = html.escape(str(job.get("title") or "Untitled role"))
    company = html.escape(str(job.get("company") or "Unknown company"))
    location = html.escape(str(job.get("location") or "Location not specified"))
    posted = html.escape(job.get("posted_at_human") or _format_posted_ago(job.get("posted_at_iso")))
    match_score = int(job.get("match_score", 0) or 0)

    description = str(job.get("description_text") or "").strip()
    if len(description) > 260:
        description = description[:260].rstrip() + "..."
    description = html.escape(description)

    tags = [str(tag).strip() for tag in (job.get("tags") or job.get("matched_skills") or []) if str(tag).strip()]
    tags = tags[:10]
    badges_html = "".join(f'<span class="k-badge">{html.escape(tag)}</span>' for tag in tags)

    apply_url = _normalize_apply_url(job)
    safe_apply_url = html.escape(apply_url, quote=True)

    action_html = (
        f'<a class="k-btn" style="margin-top:0.8rem;" href="{safe_apply_url}" target="_blank" rel="noopener">Apply</a>'
        if apply_url
        else '<span class="k-subtle" style="display:block;margin-top:0.8rem;">Application link not available</span>'
    )

    st.markdown(
        f"""
        <article class="k-job-card reveal" id="job_{idx}">
            <h3 class="k-job-title">{title}</h3>
            <div class="k-job-company">{company}</div>
            <div class="k-job-meta">
                <span>Location: {location}</span>
                <span>Posted: {posted}</span>
                <span>Match: {match_score}%</span>
            </div>
            <div class="k-job-desc">{description}</div>
            <div class="k-badge-row">{badges_html}</div>
            {action_html}
        </article>
        """,
        unsafe_allow_html=True,
    )


def _run_fetch(skills_db: dict) -> None:
    profile = str(st.session_state.get(STATE_KEYS["profile"], "")).strip()
    selected_skills = list(st.session_state.get(STATE_KEYS["skills"], []))
    manual_terms = [
        token.strip()
        for token in str(st.session_state.get(STATE_KEYS["manual"], "")).split(",")
        if token.strip()
    ]

    if not profile and not selected_skills and not manual_terms:
        st.warning("Enter a role, choose skills, or add manual keywords before searching.")
        return

    with st.spinner("Scanning global job sources..."):
        jobs = fetch_all_jobs(
            selected_skills=selected_skills,
            skills_db=skills_db,
            job_profile=profile,
            locations=list(st.session_state.get(STATE_KEYS["locations"], ["all"])),
            manual_terms=manual_terms,
            date_filter=str(st.session_state.get(STATE_KEYS["date"], "all")),
            min_match=int(st.session_state.get(STATE_KEYS["min_match"], 0)),
            max_results=500,
        )

    normalized: List[Dict[str, Any]] = []
    for item in jobs:
        item["apply_url"] = _normalize_apply_url(item)
        normalized.append(item)

    st.session_state[STATE_KEYS["results"]] = normalized
    st.session_state[STATE_KEYS["page"]] = 1


def _reset_filters() -> None:
    st.session_state[STATE_KEYS["profile"]] = ""
    st.session_state[STATE_KEYS["manual"]] = ""
    st.session_state[STATE_KEYS["skills"]] = []
    st.session_state[STATE_KEYS["locations"]] = ["all"]
    st.session_state[STATE_KEYS["date"]] = "all"
    st.session_state[STATE_KEYS["min_match"]] = 0
    st.session_state[STATE_KEYS["sort"]] = "Best match"
    st.session_state[STATE_KEYS["results"]] = []
    st.session_state[STATE_KEYS["page"]] = 1
    st.session_state[STATE_KEYS["signature"]] = ""


def render() -> None:
    _init_state()
    skills_db = _load_skills_db_safely()
    skill_options = _skills_from_db(skills_db)

    render_hero(
        kicker="Jobs Dashboard",
        title="Find role-matched opportunities with a clean card-based hiring workspace.",
        subtitle=(
            "Filter by skills, location, freshness, and relevance score. "
            "Every result card includes company, posted time, skill badges, and an apply action."
        ),
    )

    dashboard_left, dashboard_right = st.columns([1, 2.25], gap="large")

    with dashboard_left:
        st.markdown('<aside class="k-panel reveal">', unsafe_allow_html=True)
        st.markdown('<div class="k-filter-head">Filter Panel</div>', unsafe_allow_html=True)

        st.text_input(
            "Role",
            placeholder="Example: Data Analyst, Frontend Engineer",
            key=STATE_KEYS["profile"],
        )

        static_locations = ["all", "remote", "usa", "india", "uk", "uae"]
        dynamic_locations = sorted(
            {
                str(job.get("location", "")).strip().lower()
                for job in st.session_state.get(STATE_KEYS["results"], [])
                if str(job.get("location", "")).strip()
            }
        )
        location_options = list(dict.fromkeys(static_locations + dynamic_locations))

        cleaned_locations = [
            str(item).strip().lower()
            for item in st.session_state.get(STATE_KEYS["locations"], ["all"])
            if str(item).strip().lower() in location_options
        ]
        st.session_state[STATE_KEYS["locations"]] = cleaned_locations or ["all"]

        st.multiselect(
            "Location",
            options=location_options,
            key=STATE_KEYS["locations"],
            help="Use 'all' for no location restriction.",
        )

        st.selectbox(
            "Date Range",
            options=["all", "24h", "1w", "2w", "1m"],
            key=STATE_KEYS["date"],
        )

        st.multiselect(
            "Skills",
            options=skill_options,
            key=STATE_KEYS["skills"],
            placeholder="Pick required skills",
        )

        st.text_input(
            "Manual Keywords",
            placeholder="comma-separated terms",
            key=STATE_KEYS["manual"],
        )

        st.slider("Minimum Match %", min_value=0, max_value=100, step=5, key=STATE_KEYS["min_match"])

        st.selectbox(
            "Sort",
            options=["Best match", "Newest", "Match score"],
            key=STATE_KEYS["sort"],
        )

        search_clicked = st.button("Search Jobs", use_container_width=True, key="jobs_search_btn")
        reset_clicked = st.button("Reset Filters", use_container_width=True, key="jobs_reset_btn")

        st.markdown(
            '<div class="k-top-note">Use broad search terms first, then tighten with skills and minimum match score.</div>',
            unsafe_allow_html=True,
        )
        st.markdown('</aside>', unsafe_allow_html=True)

    signature = str(_query_signature())
    if signature != str(st.session_state.get(STATE_KEYS["signature"], "")):
        st.session_state[STATE_KEYS["page"]] = 1
        st.session_state[STATE_KEYS["signature"]] = signature

    if reset_clicked:
        _reset_filters()
        st.rerun()

    if search_clicked:
        _run_fetch(skills_db)

    with dashboard_right:
        jobs_final = list(st.session_state.get(STATE_KEYS["results"], []))
        jobs_final = _apply_ui_filters(jobs_final)
        jobs_final = _sort_jobs(jobs_final, str(st.session_state.get(STATE_KEYS["sort"], "Best match")))

        st.markdown(
            f'<div class="k-result-count reveal"><strong>{len(jobs_final)}</strong> jobs matched your filters.</div>',
            unsafe_allow_html=True,
        )

        if not jobs_final:
            empty_state(
                "No jobs found",
                "Try broader terms, reduce minimum match score, or remove strict location/skill filters.",
            )
            return

        per_page = 8
        current_page = int(st.session_state.get(STATE_KEYS["page"], 1))
        page_items, total_pages = _paginate(jobs_final, current_page, per_page)
        st.session_state[STATE_KEYS["page"]] = max(1, min(current_page, total_pages))

        for index, job in enumerate(page_items, start=(st.session_state[STATE_KEYS["page"]] - 1) * per_page + 1):
            _render_job_card(job, index)

        nav_prev, nav_meta, nav_next, nav_jump = st.columns([1, 1.2, 1, 1.4])
        with nav_prev:
            if st.button(
                "Previous",
                key="jobs_prev_page",
                use_container_width=True,
                disabled=st.session_state[STATE_KEYS["page"]] <= 1,
            ):
                st.session_state[STATE_KEYS["page"]] -= 1
                st.rerun()

        with nav_meta:
            st.markdown(
                f'<div class="k-subtle" style="text-align:center;padding-top:0.55rem;">Page {st.session_state[STATE_KEYS["page"]]} of {total_pages}</div>',
                unsafe_allow_html=True,
            )

        with nav_next:
            if st.button(
                "Next",
                key="jobs_next_page",
                use_container_width=True,
                disabled=st.session_state[STATE_KEYS["page"]] >= total_pages,
            ):
                st.session_state[STATE_KEYS["page"]] += 1
                st.rerun()

        with nav_jump:
            jump_page = st.number_input(
                "Go to page",
                min_value=1,
                max_value=total_pages,
                value=int(st.session_state[STATE_KEYS["page"]]),
                step=1,
                key="jobs_jump_page",
            )
            if int(jump_page) != int(st.session_state[STATE_KEYS["page"]]):
                st.session_state[STATE_KEYS["page"]] = int(jump_page)
                st.rerun()
