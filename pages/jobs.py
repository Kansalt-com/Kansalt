"""
Kansalt.com — Jobs Portal (Naukri-style UI, REAL filters)
- Real search (profile + skills + manual keywords)
- Location multi-select (All/Remote + dynamic locations)
- Date posted filter (all/24h/1w/2w/1m)
- Min match % filter
- Sort: Best match / Newest / Match%
- View: List / Compact
- Pagination: 10 per page (fills as more jobs stream in)
- Job cards: Title, Posted, Description, Skills, Apply
- NO visible fetching status box for user (silent background updates)

IMPORTANT:
- This page expects your orchestrator here:
  from services.job_fetcher import fetch_all_jobs
- Skills dropdown will populate from skills_db.json or services/utils loader.
"""

from __future__ import annotations

import math
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional, Tuple

import streamlit as st

from services.job_fetcher import fetch_all_jobs  # type: ignore


# ----------------------------
# Skills DB loader (robust)
# ----------------------------
def _load_skills_db_safely() -> dict:
    """
    Load skills from data/skills.json
    Supports structure:
    {
        "categories": {
            "DevOps": {
                "Docker": {...},
                "Kubernetes": {...}
            }
        }
    }
    OR simple list:
    {
        "skills": ["Docker", "Kubernetes"]
    }
    """
    import json
    from pathlib import Path

    path = Path("data/skills.json")

    if not path.exists():
        return {"categories": {}}

    try:
        data = json.loads(path.read_text(encoding="utf-8"))

        # If file already structured correctly
        if "categories" in data:
            return data

        # If simple structure like {"skills": [...]}
        if "skills" in data and isinstance(data["skills"], list):
            return {
                "categories": {
                    "General": {skill: {} for skill in data["skills"]}
                }
            }

        # If just a list of skills
        if isinstance(data, list):
            return {
                "categories": {
                    "General": {skill: {} for skill in data}
                }
            }

    except Exception:
        pass

    return {"categories": {}}


def _skills_from_db(skills_db: dict) -> List[str]:
    """
    Expected structure:
    skills_db["categories"][category_name][skill_label] = {...}
    """
    labels: List[str] = []
    cats = (skills_db or {}).get("categories", {}) or {}
    if isinstance(cats, dict):
        for _, cat in cats.items():
            if isinstance(cat, dict):
                for label in cat.keys():
                    if isinstance(label, str) and label.strip():
                        labels.append(label.strip())

    labels = sorted(list(set(labels)))

    # Fallback (if db missing/empty) so UI still works
    if not labels:
        labels = sorted(
            {
                "Video Editing",
                "Adobe Premiere Pro",
                "After Effects",
                "DaVinci Resolve",
                "Motion Graphics",
                "Photoshop",
                "Graphic Design",
                "Content Writing",
                "SEO",
                "Digital Marketing",
                "Python",
                "JavaScript",
                "React",
                "Node.js",
                "AWS",
                "Azure",
                "Docker",
                "Kubernetes",
                "Terraform",
                "SQL",
            }
        )

    return labels


# ----------------------------
# State
# ----------------------------
def _init_state() -> None:
    defaults = {
        "jobs_profile": "",
        "jobs_manual": "",
        "jobs_selected_skills": [],
        "jobs_locations": ["all"],
        "jobs_date_filter": "all",
        "jobs_min_match": 0,
        "jobs_sort": "Best match",
        "jobs_view": "List",
        "jobs_page": 1,
        "jobs_results": [],
        "jobs_live_snapshot": [],
        "jobs_last_query_sig": None,
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v


# ----------------------------
# Helpers
# ----------------------------
def _normalize_apply_url(job: Dict[str, Any]) -> str:
    return (
        job.get("apply_url")
        or job.get("job_url")
        or job.get("url")
        or job.get("link")
        or ""
    )


def _format_posted_ago(posted_at_iso: Optional[str]) -> str:
    if not posted_at_iso:
        return "—"
    try:
        dt = datetime.fromisoformat(str(posted_at_iso).replace("Z", "+00:00"))
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        now = datetime.now(timezone.utc)
        secs = max(0, (now - dt).total_seconds())

        minutes = int(secs // 60)
        hours = int(secs // 3600)
        days = int(secs // 86400)

        if minutes < 60:
            return f"{minutes}m ago"
        if hours < 24:
            return f"{hours}h ago"
        return f"{days}d ago"
    except Exception:
        return "—"


def _query_signature(
    profile: str,
    manual: str,
    skills: List[str],
    locations: List[str],
    date_filter: str,
    min_match: int,
    sort_by: str,
    view: str,
) -> Tuple:
    return (
        profile.strip().lower(),
        manual.strip().lower(),
        tuple(sorted([s.strip().lower() for s in skills])),
        tuple(sorted([l.strip().lower() for l in locations])),
        date_filter,
        int(min_match),
        sort_by,
        view,
    )


def _reset_page_on_filter_change(new_sig: Tuple) -> None:
    if st.session_state.jobs_last_query_sig != new_sig:
        st.session_state.jobs_page = 1
        st.session_state.jobs_last_query_sig = new_sig


def _sort_jobs(jobs: List[Dict[str, Any]], sort_by: str) -> List[Dict[str, Any]]:
    if sort_by == "Newest":

        def key(j: Dict[str, Any]) -> float:
            s = j.get("posted_at_iso")
            try:
                dt = datetime.fromisoformat(str(s).replace("Z", "+00:00"))
                if dt.tzinfo is None:
                    dt = dt.replace(tzinfo=timezone.utc)
                return dt.timestamp()
            except Exception:
                return 0.0

        return sorted(jobs, key=key, reverse=True)

    if sort_by == "Match %":
        return sorted(jobs, key=lambda j: int(j.get("match_score", 0) or 0), reverse=True)

    # Best match (rank_score)
    return sorted(
        jobs,
        key=lambda j: int(j.get("rank_score", j.get("match_score", 0)) or 0),
        reverse=True,
    )


def _paginate(items: List[Any], page: int, per_page: int) -> Tuple[List[Any], int]:
    total_pages = max(1, math.ceil(len(items) / max(1, per_page)))
    page = max(1, min(page, total_pages))
    start = (page - 1) * per_page
    end = start + per_page
    return items[start:end], total_pages


def _looks_like_blog(job: Dict[str, Any]) -> bool:
    # Extra safety (backend should already filter)
    title = (job.get("title") or "").lower()
    company = (job.get("company") or "").lower()
    url = _normalize_apply_url(job).lower()

    if "editorial staff" in company:
        return True
    if any(x in title for x in ["how to", "guide", "tips", "tutorial", "what is", "complete guide", "career transition"]):
        return True
    if any(x in url for x in ["/blog", "/article", "/how-to", "/guide", "/tips", "/news", "/insights", "/tag", "/category"]):
        return True
    return False


def _apply_ui_filters(jobs: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    REAL filters applied after fetch (so user filters always work).
    """
    profile = (st.session_state.jobs_profile or "").strip().lower()
    manual = (st.session_state.jobs_manual or "").strip().lower()
    selected_skills = st.session_state.jobs_selected_skills or []
    locations = st.session_state.jobs_locations or ["all"]
    min_match = int(st.session_state.jobs_min_match or 0)

    manual_terms = [t.strip() for t in manual.split(",") if t.strip()]
    loc_lower = [l.lower().strip() for l in locations if l]

    filtered: List[Dict[str, Any]] = []
    for j in jobs or []:
        if _looks_like_blog(j):
            continue

        # min match
        if int(j.get("match_score", 0) or 0) < min_match:
            continue

        # location filter
        if "all" not in loc_lower:
            job_loc = (j.get("location") or "").lower()
            is_remote = bool(j.get("is_remote", False)) or ("remote" in job_loc)

            if "remote" in loc_lower:
                if not is_remote:
                    # allow other chosen locations too
                    other_locs = [x for x in loc_lower if x not in ("remote", "all")]
                    if other_locs and any(x in job_loc for x in other_locs):
                        pass
                    else:
                        continue
            else:
                if not any(x in job_loc for x in loc_lower):
                    continue

        # profile/manual/skills keyword sanity (UI-side)
        # This prevents totally irrelevant stuff if some source is noisy
        text = " ".join(
            [
                str(j.get("title") or ""),
                str(j.get("company") or ""),
                str(j.get("description_text") or ""),
                " ".join(j.get("tags") or []),
            ]
        ).lower()

        # If user typed a profile, require at least some token match
        if profile:
            tokens = [t for t in profile.split() if len(t) >= 3]
            if tokens and not any(t in text for t in tokens):
                continue

        # If user selected skills, require at least 1 skill match in tags/text
        if selected_skills:
            if not any(s.lower() in text for s in selected_skills):
                continue

        # manual terms: if provided, require at least one
        if manual_terms:
            if not any(t in text for t in manual_terms):
                continue

        filtered.append(j)

    return filtered


# ----------------------------
# UI cards
# ----------------------------
def _job_card(job: Dict[str, Any]) -> None:
    title = job.get("title") or "Untitled"
    company = job.get("company") or "—"
    location = job.get("location") or "—"
    posted_ago = job.get("posted_at_human") or _format_posted_ago(job.get("posted_at_iso"))
    apply_url = _normalize_apply_url(job)

    desc = (job.get("description_text") or "").strip()
    if len(desc) > 260:
        desc = desc[:260].rstrip() + "…"

    tags = job.get("tags") or job.get("matched_skills") or []
    tags = [t for t in tags if isinstance(t, str) and t.strip()]
    tags = tags[:10]

    st.markdown('<div class="k-card k-animate" style="margin-top:12px;">', unsafe_allow_html=True)

    top1, top2 = st.columns([3, 1.2])
    with top1:
        st.markdown(f'<div style="font-weight:950;font-size:16px;color:var(--accent);">{title}</div>', unsafe_allow_html=True)
        st.markdown(f'<div style="color:var(--muted);font-weight:800;margin-top:2px;">{company}</div>', unsafe_allow_html=True)
        st.markdown(
            f'<div style="margin-top:8px;color:var(--muted);font-size:13px;">📍 {location}</div>',
            unsafe_allow_html=True,
        )

    with top2:
        st.markdown(
            f'<div style="text-align:right;color:var(--muted);font-size:12px;">Posted: <b>{posted_ago}</b></div>',
            unsafe_allow_html=True,
        )
        ms = int(job.get("match_score", 0) or 0)
        st.markdown(
            f'<div style="text-align:right;margin-top:6px;font-weight:900;">Match {ms}%</div>',
            unsafe_allow_html=True,
        )

    if desc:
        st.markdown(
            f'<div style="margin-top:10px;color:var(--text);font-size:13px;line-height:1.5;">{desc}</div>',
            unsafe_allow_html=True,
        )

    if tags:
        chips_html = "".join(
            [
                (
                    '<span style="padding:5px 10px;border-radius:999px;border:1px solid var(--border);'
                    f'background:rgba(231,226,217,0.5);font-size:12px;color:var(--text);">{t}</span>'
                )
                for t in tags
            ]
        )
        st.markdown(
            f'<div style="margin-top:10px;display:flex;flex-wrap:wrap;gap:8px;">{chips_html}</div>',
            unsafe_allow_html=True,
        )

    if apply_url:
        st.link_button("Apply ↗", apply_url, use_container_width=True)
    else:
        st.button("Apply (missing link)", use_container_width=True, disabled=True)

    st.markdown("</div>", unsafe_allow_html=True)


# ----------------------------
# Main page
# ----------------------------
def render() -> None:
    _init_state()

    skills_db = _load_skills_db_safely()
    skill_options = _skills_from_db(skills_db)

    st.markdown("## 💼 Jobs")

    # Silent placeholders (no user-facing progress boxes)
    live_ph = st.empty()

    # ----------------------------
    # Search Bar
    # ----------------------------
    st.markdown('<div class="k-card k-animate">', unsafe_allow_html=True)
    c1, c2, c3, c4 = st.columns([2.0, 1.7, 1.1, 1.0])

    with c1:
        st.markdown(
            '<div style="font-weight:800;font-size:13px;color:var(--muted);margin-bottom:6px;">Job profile / role</div>',
            unsafe_allow_html=True,
        )
        st.text_input(
            "Job profile / role",
            key="jobs_profile",
            placeholder="DevOps Engineer, Video Editor, Data Analyst…",
            label_visibility="collapsed",
        )

    with c2:
        st.markdown(
            '<div style="font-weight:800;font-size:13px;color:var(--muted);margin-bottom:6px;">Location</div>',
            unsafe_allow_html=True,
        )
        static_opts = ["all", "remote", "india", "usa", "hyderabad", "saudi"]
        dynamic_locs = sorted(
            {str(j.get("location", "")).strip() for j in (st.session_state.jobs_results or []) if j.get("location")}
        )
        st.multiselect(
            "Location",
            options=list(dict.fromkeys(static_opts + dynamic_locs)),
            key="jobs_locations",
            help="Choose 'all' for no location filtering.",
        )

    with c3:
        st.markdown(
            '<div style="font-weight:800;font-size:13px;color:var(--muted);margin-bottom:6px;">Date posted</div>',
            unsafe_allow_html=True,
        )
        st.selectbox("Date posted", ["all", "24h", "1w", "2w", "1m"], key="jobs_date_filter", label_visibility="collapsed")

    with c4:
        st.markdown('<div style="height:22px;"></div>', unsafe_allow_html=True)
        clicked_search = st.button("Search", use_container_width=True)

    st.markdown("</div>", unsafe_allow_html=True)

    # ----------------------------
    # Filters
    # ----------------------------
    with st.expander("⚙️ Filters", expanded=False):
        f1, f2, f3 = st.columns([2.2, 1.2, 1.2])

        with f1:
            st.multiselect(
                "Skills",
                options=skill_options,
                key="jobs_selected_skills",
                placeholder="Select skills…",
                help="Jobs must match at least 1 selected skill.",
            )
            st.text_input(
                "Manual keywords (comma-separated)",
                key="jobs_manual",
                placeholder="premiere pro, after effects, davinci, motion graphics",
            )

        with f2:
            st.slider("Minimum match %", 0, 100, key="jobs_min_match", step=5)

        with f3:
            st.selectbox("Sort", ["Best match", "Newest", "Match %"], key="jobs_sort")
            st.selectbox("View", ["List", "Compact"], key="jobs_view")

        sig = _query_signature(
            st.session_state.jobs_profile,
            st.session_state.jobs_manual,
            st.session_state.jobs_selected_skills,
            st.session_state.jobs_locations,
            st.session_state.jobs_date_filter,
            st.session_state.jobs_min_match,
            st.session_state.jobs_sort,
            st.session_state.jobs_view,
        )
        _reset_page_on_filter_change(sig)

        if st.button("Clear all", use_container_width=False):
            st.session_state.jobs_profile = ""
            st.session_state.jobs_manual = ""
            st.session_state.jobs_selected_skills = []
            st.session_state.jobs_locations = ["all"]
            st.session_state.jobs_date_filter = "all"
            st.session_state.jobs_min_match = 0
            st.session_state.jobs_sort = "Best match"
            st.session_state.jobs_view = "List"
            st.session_state.jobs_page = 1
            st.session_state.jobs_results = []
            st.session_state.jobs_live_snapshot = []
            st.rerun()

    # ----------------------------
    # Fetch (live but silent)
    # ----------------------------
    if clicked_search:
        profile = (st.session_state.jobs_profile or "").strip()
        skills = st.session_state.jobs_selected_skills or []
        manual = (st.session_state.jobs_manual or "").strip()

        if not skills and not profile and not manual:
            st.warning("Enter a role OR select skills OR add manual keywords.")
        else:
            st.session_state.jobs_results = []
            st.session_state.jobs_live_snapshot = []
            st.session_state.jobs_page = 1

            def stream_cb(snapshot: List[dict], source_name: str) -> None:
                # User should NOT see status; we just update the live placeholder quietly
                safe = [j for j in (snapshot or []) if not _looks_like_blog(j)]
                safe = _sort_jobs(safe, st.session_state.jobs_sort)

                # Apply UI filters so what user sees is consistent
                safe = _apply_ui_filters(safe)

                with live_ph.container():
                    st.markdown(
                        f'<div style="margin:10px 0 6px 0;font-weight:900;color:var(--accent);">{len(safe)} jobs</div>',
                        unsafe_allow_html=True,
                    )
                    for j in safe[:10]:
                        _job_card(j)

            jobs = fetch_all_jobs(
                selected_skills=skills,
                skills_db=skills_db,
                job_profile=profile,
                locations=st.session_state.jobs_locations or ["all"],
                manual_terms=[x.strip() for x in manual.split(",") if x.strip()],
                date_filter=st.session_state.jobs_date_filter,
                min_match=int(st.session_state.jobs_min_match),
                max_results=500,
                stream_callback=stream_cb,
            )

            # finalize
            for j in jobs:
                j["apply_url"] = _normalize_apply_url(j)

            jobs = [j for j in jobs if not _looks_like_blog(j)]
            st.session_state.jobs_results = jobs
            live_ph.empty()

    # ----------------------------
    # Final Results (always filtered + paginated)
    # ----------------------------
    jobs_final: List[Dict[str, Any]] = st.session_state.get("jobs_results", []) or []
    jobs_final = [j for j in jobs_final if not _looks_like_blog(j)]
    jobs_final = _apply_ui_filters(jobs_final)
    jobs_final = _sort_jobs(jobs_final, st.session_state.jobs_sort)

    if not jobs_final:
        st.markdown(
            """
            <div class="k-card k-animate" style="text-align:center;padding:32px;margin-top:12px;">
              <div style="font-weight:900;font-size:18px;">No jobs found</div>
              <div style="color:var(--muted);margin-top:6px;">Try a broader role, lower match %, or remove strict skills.</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        return

    per_page = 10
    page = int(st.session_state.jobs_page)
    page_items, total_pages = _paginate(jobs_final, page, per_page)
    st.session_state.jobs_page = max(1, min(page, total_pages))

    st.markdown(
        f'<div style="margin:10px 0 6px 0;font-weight:900;color:var(--accent);">{len(jobs_final)} jobs</div>',
        unsafe_allow_html=True,
    )

    if st.session_state.jobs_view == "Compact":
        cols = st.columns(2)
        for i, j in enumerate(page_items):
            with cols[i % 2]:
                _job_card(j)
    else:
        for j in page_items:
            _job_card(j)

    # Pagination
    st.markdown('<div style="margin-top:16px;"></div>', unsafe_allow_html=True)
    p1, p2, p3, p4 = st.columns([1, 1.2, 1, 2])

    with p1:
        if st.button("← Prev", use_container_width=True, disabled=(st.session_state.jobs_page <= 1)):
            st.session_state.jobs_page -= 1
            st.rerun()

    with p2:
        st.markdown(
            f'<div class="k-card" style="text-align:center;padding:10px;">Page <b>{st.session_state.jobs_page}</b> / {total_pages}</div>',
            unsafe_allow_html=True,
        )

    with p3:
        if st.button("Next →", use_container_width=True, disabled=(st.session_state.jobs_page >= total_pages)):
            st.session_state.jobs_page += 1
            st.rerun()

    with p4:
        jump = st.number_input(
            "Jump to page",
            min_value=1,
            max_value=total_pages,
            value=st.session_state.jobs_page,
            step=1,
        )
        if int(jump) != int(st.session_state.jobs_page):
            st.session_state.jobs_page = int(jump)
            st.rerun()
