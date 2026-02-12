"""
Kansalt Jobs Tool - Search and apply for remote jobs
Unified table view with 25 jobs per page, no API-based separation
"""
import json
import streamlit as st
from datetime import datetime
from typing import Optional, List
import sys
import os
from pathlib import Path

# Add project root to path for imports
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from services import (
    SkillMatcher, ResumeParser, ResumeOptimizer, DocumentBuilder,
    fetch_all_jobs, fetch_jobs_streaming, normalize_jobs, compute_pagination
)
from utils import get_logger

logger = get_logger(__name__)


def render():
    """Main render function for Jobs tool."""
    
    # =========================================================================
    # PAGE CONFIG
    # =========================================================================
    st.set_page_config(
        layout="wide",
        page_title="Kansalt - Remote Jobs",
        page_icon="💼",
        initial_sidebar_state="expanded",
    )

    # =========================================================================
    # DARK CYBERPUNK THEME CSS & STYLING
    # =========================================================================
    st.markdown("""
    <style>
        /* Color Palette - Dark Cyberpunk + Neon */
        :root {
            --primary-accent: #f97316;
            --secondary-accent: #7c3aed;
            --light-bg: #1a0b2e;
            --card-bg: rgba(229, 231, 235, 0.03);
            --text-primary: #ffffff;
            --text-secondary: #a1a1aa;
            --text-muted: #6b7280;
            --border: rgba(0, 255, 255, 0.2);
            --success: #00ffff;
            --warning: #f97316;
        }

        /* Global */
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body, html {
            background: #0f051a !important;
            color: var(--text-primary) !important;
            font-family: 'JetBrains Mono', 'Fira Code', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif !important;
        }

        .main {
            background: #0f051a !important;
        }

        h1, h2, h3, h4, h5, h6 {
            color: var(--text-primary) !important;
            font-weight: 600;
        }

        p, span, label {
            color: var(--text-secondary) !important;
        }

        /* Job Cards - Cyberpunk Neon */
        .job-card {
            background: var(--card-bg);
            border: 1px solid var(--border);
            border-radius: 16px;
            padding: 20px;
            transition: all 0.2s ease;
            margin-bottom: 1rem;
            box-shadow: 0 0 20px rgba(124, 58, 237, 0.1);
        }

        .job-card:hover {
            border-color: rgba(249, 115, 22, 0.5);
            box-shadow: 0 0 30px rgba(249, 115, 22, 0.3);
            transform: translateY(-4px);
        }

        /* Badges - Cyberpunk Neon */
        .badge {
            display: inline-block;
            padding: 6px 12px;
            border-radius: 10px;
            font-size: 0.75rem;
            font-weight: 500;
            text-transform: uppercase;
            border: 1px solid;
        }

        .badge-high {
            background: rgba(249, 115, 22, 0.15);
            color: #f97316;
            border-color: rgba(249, 115, 22, 0.3);
        }

        .badge-med {
            background: rgba(0, 255, 255, 0.15);
            color: #00ffff;
            border-color: rgba(0, 255, 255, 0.3);
        }

        .badge-low {
            background: rgba(124, 58, 237, 0.15);
            color: #7c3aed;
            border-color: rgba(124, 58, 237, 0.3);
        }

        .badge-remote {
            background: rgba(0, 255, 255, 0.15);
            color: #00ffff;
            border-color: rgba(0, 255, 255, 0.3);
        }

        /* Filter Section */
        .filter-title {
            font-size: 0.75rem;
            font-weight: 600;
            color: var(--text-muted);
            text-transform: uppercase;
            letter-spacing: 0.05em;
            margin-bottom: 0.75rem;
        }

        /* Empty State */
        .empty-state {
            text-align: center;
            padding: 3rem;
            color: var(--text-muted);
        }

        .empty-state-icon {
            font-size: 2.5rem;
            margin-bottom: 1rem;
        }

        /* Footer */
        .footer {
            background: #F6FAFB;
            border-top: 1px solid var(--border);
            padding: 2rem;
            text-align: center;
            color: var(--text-muted);
            font-size: 0.875rem;
            margin-top: 4rem;
        }

        .footer a {
            color: var(--primary-blue);
            text-decoration: none;
        }

        .footer a:hover {
            text-decoration: underline;
        }

        hr {
            border: none;
            border-top: 1px solid var(--border-light);
        }
    </style>
    """, unsafe_allow_html=True)

    # =========================================================================
    # SESSION STATE INITIALIZATION
    # =========================================================================
    if "last_search_results" not in st.session_state:
        st.session_state.last_search_results = []
    if "last_search_meta" not in st.session_state:
        st.session_state.last_search_meta = {}
    if "results_page" not in st.session_state:
        st.session_state.results_page = 1
    if "results_per_page" not in st.session_state:
        st.session_state.results_per_page = 25

    # =========================================================================
    # NAVBAR
    # =========================================================================
    col_brand, col_spacer, col_nav = st.columns([2, 3, 2])

    with col_brand:
        st.markdown('<div style="font-size: 1.5rem; font-weight: 700; background: linear-gradient(135deg, #3B82F6 0%, #22C55E 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;">💼 Kansalt - Jobs</div>', unsafe_allow_html=True)

    with col_nav:
        col_back, col_home = st.columns([1, 1])
        with col_back:
            if st.button("← Back", use_container_width=True, key="jobs_btn_back"):
                st.session_state.selected_tool = None
                st.rerun()
        with col_home:
            st.markdown("<div style='font-size: 0.9rem; color: var(--text-secondary); text-transform: uppercase; letter-spacing: 0.05em;'>Jobs Dashboard</div>", unsafe_allow_html=True)

    st.markdown("---")

    # =========================================================================
    # LOAD SKILLS DATABASE
    # =========================================================================
    @st.cache_resource
    def load_skills_db() -> dict:
        """Load skills database."""
        try:
            skills_path = Path(__file__).parent.parent / "data" / "skills.json"
            with open(skills_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"Error loading skills.json: {e}")
            return {"categories": {}}

    skills_db = load_skills_db()
    it_skills = SkillMatcher.get_it_skills(skills_db)
    non_it_skills = SkillMatcher.get_non_it_skills(skills_db)

    # =========================================================================
    # MAIN LAYOUT: Sidebar + Content
    # =========================================================================
    col_sidebar, col_content = st.columns([1, 3.5], gap="large")

    # ===== SIDEBAR: FILTERS =====
    with col_sidebar:
        st.markdown('<span class="filter-title">⚙️ Search Filters</span>', unsafe_allow_html=True)

        job_profile = st.text_input(
            "Job Title/Role",
            placeholder="e.g., Python Developer",
            help="Search by job title or role",
            key="sidebar_profile"
        )

        skill_category = st.radio("Skill Type:", ["All", "IT Only", "Non-IT Only"], key="sidebar_skill_cat")
        available_skills = (
            it_skills + non_it_skills if skill_category == "All"
            else it_skills if skill_category == "IT Only"
            else non_it_skills
        )

        selected_skills = st.multiselect(
            "Select Skills:",
            available_skills,
            key="sidebar_skills",
            help="Pick skills to match",
        )

        manual_skills_text = st.text_input(
            "Custom Skills",
            placeholder="e.g., Kubernetes, Medical Billing",
            key="sidebar_manual_skills",
            help="Add skills not listed",
        )
        manual_skills = [s.strip() for s in manual_skills_text.split(",") if s.strip()]

        st.markdown("---")
        st.markdown('<div class="filter-title">📍 Filters</div>', unsafe_allow_html=True)

        location_options = [
            "Remote", "United States", "United Kingdom", "Canada",
            "India", "Australia", "Germany", "Netherlands", "Europe"
        ]
        locations = st.multiselect(
            "Locations:",
            location_options,
            default=["Remote"],
            key="sidebar_locations",
        )

        date_filter = st.selectbox(
            "Posted:",
            ["all", "24h", "1w", "2w", "1m"],
            format_func=lambda x: {
                "all": "Any time",
                "24h": "Last 24h",
                "1w": "Last 7 days",
                "2w": "Last 2 weeks",
                "1m": "Last month"
            }[x],
            key="sidebar_date",
        )

        min_match = st.slider(
            "Min Match %",
            0, 100, 10, 5,
            key="sidebar_min_match",
        )

        st.markdown("---")

        # Search Button
        search_clicked = st.button(
            "🔎 Search Jobs",
            use_container_width=True,
            type="primary",
            key="btn_search"
        )

        clear_clicked = st.button(
            "🗑️ Clear",
            use_container_width=True,
            key="btn_clear"
        )

    # ===== CONTENT AREA =====
    with col_content:
        # Handle search
        if search_clicked:
            if not job_profile.strip() and not selected_skills and not manual_skills:
                st.error("⚠️ Enter a job title, select skills, or add custom skills to search.")
                st.stop()

            # Placeholder for incremental results
            results_placeholder = st.empty()

            try:
                # Expand search terms first
                from services.job_fetcher import _expand_search_terms
                search_terms = _expand_search_terms(selected_skills, skills_db, job_profile.strip(), manual_skills)

                # Check cache first (instant results if available)
                from utils.cache import CacheManager
                cache_key = f"jobs_{hash(tuple(sorted(search_terms)))}"
                cached_jobs = CacheManager.get(cache_key)

                if cached_jobs:
                    # Use cached results immediately and render
                    normalized_jobs = normalize_jobs(cached_jobs)
                    st.session_state.last_search_results = normalized_jobs
                    st.session_state.results_page = 1
                    st.session_state.last_search_meta = {
                        "job_profile": job_profile,
                        "selected_skills": selected_skills,
                        "manual_skills": manual_skills,
                        "locations": locations,
                        "date_filter": date_filter,
                        "min_match": min_match,
                    }
                    st.rerun()

                # Define streaming callback to update UI as sources complete
                def _stream_cb(jobs_so_far, source_name=None):
                    try:
                        normalized = normalize_jobs(jobs_so_far)
                        snapshot = normalized[:25]
                        with results_placeholder.container():
                            for job in snapshot:
                                st.markdown(f"### {job.get('title','Untitled')}")
                                st.caption(f"**{job.get('company','Unknown')}** — {job.get('location','Remote')}")
                                match_pct = job.get('match_percent', 0)
                                if match_pct >= 70:
                                    st.markdown(f'<div class="badge badge-high">{match_pct}%</div>', unsafe_allow_html=True)
                                elif match_pct >= 40:
                                    st.markdown(f'<div class="badge badge-med">{match_pct}%</div>', unsafe_allow_html=True)
                                else:
                                    st.markdown(f'<div class="badge badge-low">{match_pct}%</div>', unsafe_allow_html=True)
                                st.markdown('---')
                    except Exception:
                        logger.debug('stream callback render error', exc_info=True)

                # Kick off fetch with streaming callback; this will render intermediate results quickly
                jobs = fetch_all_jobs(
                    selected_skills=selected_skills,
                    skills_db=skills_db,
                    job_profile=job_profile.strip(),
                    locations=locations if locations else ["Remote"],
                    manual_terms=manual_skills,
                    date_filter=date_filter,
                    min_match=min_match,
                    max_results=500,
                    match_weight=60,
                    freshness_weight=40,
                    stream_callback=_stream_cb,
                )

                normalized_jobs = normalize_jobs(jobs)

                st.session_state.last_search_results = normalized_jobs
                st.session_state.results_page = 1
                st.session_state.last_search_meta = {
                    "job_profile": job_profile,
                    "selected_skills": selected_skills,
                    "manual_skills": manual_skills,
                    "locations": locations,
                    "date_filter": date_filter,
                    "min_match": min_match,
                }
                st.rerun()

            except Exception as e:
                st.error(f"❌ Search error: {str(e)}")
                logger.error(f"Search error: {e}", exc_info=True)

        if clear_clicked:
            st.session_state.last_search_results = []
            st.session_state.last_search_meta = {}
            st.session_state.results_page = 1
            st.rerun()

        # ===== RESULTS DISPLAY =====
        results = st.session_state.last_search_results

        if not results:
            st.markdown("""
            <div class="empty-state">
                <div class="empty-state-icon">🔍</div>
                <h3>No Jobs Yet</h3>
                <p>Use the filters on the left to search for your dream job.</p>
            </div>
            """, unsafe_allow_html=True)
        else:
            # Pagination
            page_size = 25
            pagination = compute_pagination(len(results), st.session_state.results_page, page_size)

            # Results header
            col_info, col_page = st.columns([3, 1])
            with col_info:
                st.markdown(f"**{pagination['display_text']}**")
            with col_page:
                if pagination["total_pages"] > 1:
                    new_page = st.number_input(
                        "Page",
                        min_value=1,
                        max_value=pagination["total_pages"],
                        value=pagination["current_page"],
                        label_visibility="collapsed"
                    )
                    if new_page != st.session_state.results_page:
                        st.session_state.results_page = new_page
                        st.rerun()

            st.markdown("---")

            # Get paginated results
            paginated_results = results[pagination["start_idx"]:pagination["end_idx"]]

            # Render job cards
            for idx, job in enumerate(paginated_results):
                with st.container(border=True):
                    col1, col2, col3 = st.columns([3, 1, 0.8])

                    with col1:
                        st.markdown(f"### {job.get('title', 'Untitled')}")
                        col_company, col_location = st.columns([2, 1])
                        with col_company:
                            st.caption(f"**{job.get('company', 'Unknown')}**")
                        with col_location:
                            st.markdown(f'<span class="badge badge-remote">🌍 {job.get("location", "Remote")}</span>', unsafe_allow_html=True)

                        st.caption(f"Posted {job.get('posted_ago', '—')}")

                    with col2:
                        # Match badge
                        match_pct = job.get("match_percent", 0)
                        if match_pct >= 70:
                            st.markdown(f'<div class="badge badge-high">{match_pct}%</div>', unsafe_allow_html=True)
                        elif match_pct >= 40:
                            st.markdown(f'<div class="badge badge-med">{match_pct}%</div>', unsafe_allow_html=True)
                        else:
                            st.markdown(f'<div class="badge badge-low">{match_pct}%</div>', unsafe_allow_html=True)

                    with col3:
                        apply_url = job.get("apply_url", "")
                        if apply_url and apply_url.startswith("http"):
                            st.link_button("Apply", apply_url, use_container_width=True)
                        else:
                            st.button("Apply", disabled=True, use_container_width=True, key=f"apply_disabled_{idx}")

    # =========================================================================
    # FOOTER
    # =========================================================================
    st.markdown("---")
    st.markdown("""
    <div class="footer">
        <p><strong>Kansalt</strong> v1.0 | Find your perfect remote job</p>
        <p>Made with ❤️ | <a href="https://github.com" target="_blank">GitHub</a> | Contact: hello@kansalt.io</p>
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    render()
