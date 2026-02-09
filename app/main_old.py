"""
Kansalt.com - Modern SaaS Remote Job Aggregator
Premium dark-theme dashboard with modern UX
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
    SkillMatcher, ResumeParser, DocumentBuilder, fetch_all_jobs,
    fetch_jobs_streaming, normalize_jobs, compute_pagination
)
from utils import get_logger

logger = get_logger(__name__)

# =========================================================================
# PAGE CONFIG
# =========================================================================
st.set_page_config(
    layout="wide",
    page_title="Kansalt - Remote Jobs",
    page_icon="🚀",
    initial_sidebar_state="collapsed",
)

# =========================================================================
# DARK THEME CSS & STYLING
# =========================================================================
st.markdown("""
<style>
    /* Color Scheme */
    :root {
        --bg: #0B1220;
        --card: #111A2E;
        --primary: #3B82F6;
        --accent: #22C55E;
        --text: #E5E7EB;
        --text-muted: #94A3B8;
        --border: #1F2A44;
    }

    /* Global Styles */
    * {
        margin: 0;
        padding: 0;
        box-sizing: border-box;
    }

    body, html {
        background: #0B1220 !important;
        color: #E5E7EB !important;
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif !important;
    }

    /* Main Container */
    .main {
        background: #0B1220 !important;
    }

    /* Sidebar */
    .sidebar {
        background: #111A2E !important;
        border-right: 1px solid #1F2A44;
    }

    /* Text Colors */
    h1, h2, h3, h4, h5, h6 {
        color: #E5E7EB !important;
    }

    p, span, label {
        color: #E5E7EB !important;
    }

    .stMarkdown p {
        color: #E5E7EB !important;
    }

    /* Input Fields */
    .stTextInput > div > div > input,
    .stSelectbox > div > div > select,
    .stNumberInput > div > div > input,
    .stMultiSelect > div > div > div > input {
        background: #1F2A44 !important;
        color: #E5E7EB !important;
        border: 1px solid #1F2A44 !important;
        border-radius: 8px !important;
    }

    .stTextInput > div > div > input:focus,
    .stSelectbox > div > div > select:focus,
    .stNumberInput > div > div > input:focus,
    .stMultiSelect > div > div > div > input:focus {
        border-color: #3B82F6 !important;
        box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1) !important;
    }

    /* Buttons */
    .stButton > button {
        background: #3B82F6 !important;
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        font-weight: 600 !important;
        padding: 10px 20px !important;
        transition: all 0.2s ease !important;
    }

    .stButton > button:hover {
        background: #2563EB !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 4px 12px rgba(59, 130, 246, 0.4) !important;
    }

    .stButton > button:active {
        transform: translateY(0) !important;
    }

    /* Secondary Button */
    .btn-secondary {
        background: #1F2A44 !important;
        color: #E5E7EB !important;
        border: 1px solid #2D3E52 !important;
    }

    .btn-secondary:hover {
        background: #2D3E52 !important;
        color: #E5E7EB !important;
    }

    /* Ghost Button */
    .btn-ghost {
        background: transparent !important;
        color: #3B82F6 !important;
        border: 1px solid #3B82F6 !important;
    }

    .btn-ghost:hover {
        background: rgba(59, 130, 246, 0.1) !important;
    }

    /* Cards */
    .job-card {
        background: #111A2E !important;
        border: 1px solid #1F2A44;
        border-radius: 12px;
        padding: 1.5rem;
        transition: all 0.2s ease;
        margin-bottom: 1rem;
    }

    .job-card:hover {
        border-color: #3B82F6;
        box-shadow: 0 4px 12px rgba(59, 130, 246, 0.15) !important;
        transform: translateY(-2px);
    }

    /* Navbar */
    .navbar {
        background: #111A2E;
        border-bottom: 1px solid #1F2A44;
        padding: 1rem 2rem;
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 2rem;
    }

    .navbar-brand {
        font-size: 1.5rem;
        font-weight: 700;
        background: linear-gradient(135deg, #3B82F6 0%, #22C55E 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }

    .navbar-actions {
        display: flex;
        gap: 0.75rem;
    }

    /* Badge Styles */
    .badge {
        display: inline-block;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.75rem;
        font-weight: 600;
    }

    .badge-high {
        background: rgba(34, 197, 94, 0.2) !important;
        color: #22C55E !important;
        border: 1px solid #22C55E !important;
    }

    .badge-med {
        background: rgba(249, 115, 22, 0.2) !important;
        color: #FB923C !important;
        border: 1px solid #FB923C !important;
    }

    .badge-low {
        background: rgba(148, 163, 184, 0.2) !important;
        color: #94A3B8 !important;
        border: 1px solid #94A3B8 !important;
    }

    .badge-remote {
        background: rgba(59, 130, 246, 0.2) !important;
        color: #3B82F6 !important;
        border: 1px solid #3B82F6 !important;
    }

    /* Skill Chips */
    .skill-chip {
        display: inline-block;
        background: #1F2A44;
        color: #3B82F6;
        padding: 4px 10px;
        border-radius: 6px;
        font-size: 0.75rem;
        margin-right: 0.5rem;
        margin-bottom: 0.5rem;
        border: 1px solid #2D3E52;
    }

    /* Loading Skeleton */
    .skeleton {
        background: linear-gradient(90deg, #1F2A44 25%, #2D3E52 50%, #1F2A44 75%);
        background-size: 200% 100%;
        animation: loading 1.5s infinite;
        border-radius: 8px;
    }

    @keyframes loading {
        0% { background-position: 200% 0; }
        100% { background-position: -200% 0; }
    }

    /* Empty State */
    .empty-state {
        text-align: center;
        padding: 3rem;
        color: #94A3B8;
    }

    .empty-state-icon {
        font-size: 3rem;
        margin-bottom: 1rem;
    }

    /* Footer */
    .footer {
        background: #111A2E;
        border-top: 1px solid #1F2A44;
        padding: 2rem;
        text-align: center;
        color: #94A3B8;
        font-size: 0.875rem;
        margin-top: 4rem;
    }

    .footer a {
        color: #3B82F6;
        text-decoration: none;
    }

    .footer a:hover {
        text-decoration: underline;
    }

    /* Divider */
    hr {
        border: none;
        border-top: 1px solid #1F2A44;
    }

    /* Sidebar Styles */
    .filter-section {
        background: #111A2E;
        border: 1px solid #1F2A44;
        border-radius: 12px;
        padding: 1.5rem;
        margin-bottom: 1.5rem;
    }

    .filter-title {
        font-size: 0.875rem;
        font-weight: 700;
        color: #94A3B8;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-bottom: 1rem;
    }

    /* Progress Bar */
    .stProgress > div > div > div {
        background: linear-gradient(90deg, #3B82F6, #22C55E) !important;
    }

    /* Links */
    a {
        color: #3B82F6 !important;
        text-decoration: none;
    }

    a:hover {
        color: #2563EB !important;
    }

    /* Metrics */
    .metric-card {
        background: #111A2E;
        border: 1px solid #1F2A44;
        border-radius: 12px;
        padding: 1.5rem;
        text-align: center;
    }

    .metric-value {
        font-size: 2rem;
        font-weight: 700;
        color: #22C55E;
        margin-bottom: 0.5rem;
    }

    .metric-label {
        font-size: 0.875rem;
        color: #94A3B8;
    }

    /* Responsive */
    @media (max-width: 768px) {
        .navbar {
            flex-direction: column;
            gap: 1rem;
        }

        .job-card {
            padding: 1rem;
        }
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
if "resume_text" not in st.session_state:
    st.session_state.resume_text = ""
if "candidate_name" not in st.session_state:
    st.session_state.candidate_name = ""
if "candidate_email" not in st.session_state:
    st.session_state.candidate_email = ""
if "generated_docs" not in st.session_state:
    st.session_state.generated_docs = {}
if "auth_state" not in st.session_state:
    st.session_state.auth_state = "guest"

# =========================================================================
# NAVBAR
# =========================================================================
col_brand, col_spacer, col_auth = st.columns([2, 3, 2])

with col_brand:
    st.markdown('<div style="font-size: 1.5rem; font-weight: 700; background: linear-gradient(135deg, #3B82F6 0%, #22C55E 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;">🚀 Kansalt</div>', unsafe_allow_html=True)

with col_auth:
    col_l, col_r, col_g = st.columns([1, 1, 1.2])
    with col_l:
        if st.button("Login", use_container_width=True, key="btn_login"):
            st.info("Login feature coming soon!")
    with col_r:
        if st.button("Register", use_container_width=True, key="btn_register"):
            st.info("Registration coming soon!")
    with col_g:
        if st.button("👤 Continue as Guest", use_container_width=True, key="btn_guest"):
            st.session_state.auth_state = "guest"

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
    st.markdown('<div class="filter-title">⚙️ Search Filters</div>', unsafe_allow_html=True)

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

        # Containers for streaming display
        status_placeholder = st.empty()
        results_placeholder = st.container()
        
        status_placeholder.markdown("🔄 **Searching for jobs...** Results appear as they arrive!", unsafe_allow_html=True)
        
        all_streaming_jobs = []
        sources_found = 0
        
        try:
            # Stream results as they arrive
            for source_name, jobs_so_far in fetch_jobs_streaming(
                selected_skills=selected_skills,
                skills_db=skills_db,
                job_profile=job_profile.strip(),
                locations=locations if locations else ["Remote"],
                manual_terms=manual_skills,
                date_filter=date_filter,
                min_match=min_match,
                match_weight=60,
                freshness_weight=40,
            ):
                sources_found += 1
                all_streaming_jobs = jobs_so_far[:25]  # Show top 25
                
                # Update display with current results
                with results_placeholder:
                    st.markdown(f"**✓ {source_name}** — {len(jobs_so_far)} jobs found so far", help=f"Jobs from {source_name}")
                    
                    # Show top results so far
                    if jobs_so_far:
                        cols = st.columns(2, gap="medium")
                        for idx, job in enumerate(jobs_so_far[:10]):
                            col = cols[idx % 2]
                            with col:
                                with st.container(border=True):
                                    # Job title
                                    st.markdown(f"**{job.get('title', 'N/A')}**")
                                    
                                    # Company + match score
                                    match = job.get("match_score", 0)
                                    if match >= 70:
                                        badge_color = "#22C55E"
                                        badge_text = f"✓ {match}% Match"
                                    elif match >= 40:
                                        badge_color = "#F97316"
                                        badge_text = f"◐ {match}% Match"
                                    else:
                                        badge_color = "#64748B"
                                        badge_text = f"○ {match}% Match"
                                    
                                    col1, col2 = st.columns([3, 1])
                                    with col1:
                                        st.caption(f"**{job.get('company', 'Unknown')}**")
                                    with col2:
                                        st.markdown(f'<span style="color: {badge_color}; font-weight: 600;">{badge_text}</span>', unsafe_allow_html=True)
                                    
                                    # Location & posted time
                                    st.caption(f"📍 {job.get('location', 'Remote')} • {job.get('posted_at_human', 'Recently')}")
                                    
                                    # Apply button - use unique key with index to avoid duplicates
                                    unique_key = f"{job.get('job_code', '')}_streaming_{idx}_{sources_found}"
                                    if st.button("Apply →", key=unique_key, use_container_width=True):
                                        st.session_state.current_job = job
                        
                        st.divider()
            
            # Final results processing
            status_placeholder.empty()
            results_placeholder.empty()
            
            # Get final ranked results
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
            )
            
            normalized_jobs = normalize_jobs(jobs)

            with st.container():
                st.success(f"✓ **Found {len(normalized_jobs)} matching jobs** from {sources_found}+ sources!")

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
            status_placeholder.empty()
            results_placeholder.empty()
            st.error(f"❌ Search error: {e}")
            logger.error(f"Search error: {e}", exc_info=True)

    if clear_clicked:
        st.session_state.last_search_results = []
        st.session_state.last_search_meta = {}
        st.session_state.generated_docs = {}
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

        # Render job cards in a responsive layout
        for idx, job in enumerate(paginated_results):
            job_code = job.get("job_code", "unknown")
            title = job.get("title", "Untitled")
            company = job.get("company", "Unknown")
            location = job.get("location", "Remote")
            match_pct = job.get("match_percent", 0)
            posted_ago = job.get("posted_ago", "—")
            apply_url = job.get("apply_url", "")

            # Job Card
            with st.container(border=True):
                col1, col2, col3 = st.columns([3, 1, 0.8])

                with col1:
                    st.markdown(f"### {title}")
                    col_company, col_location = st.columns([2, 1])
                    with col_company:
                        st.caption(f"**{company}**")
                    with col_location:
                        st.markdown(f'<span class="badge badge-remote">🌍 {location}</span>', unsafe_allow_html=True)

                    st.caption(f"Posted {posted_ago}")

                with col2:
                    # Match badge
                    if match_pct >= 70:
                        st.markdown(f'<div class="badge badge-high">{match_pct}%</div>', unsafe_allow_html=True)
                    elif match_pct >= 40:
                        st.markdown(f'<div class="badge badge-med">{match_pct}%</div>', unsafe_allow_html=True)
                    else:
                        st.markdown(f'<div class="badge badge-low">{match_pct}%</div>', unsafe_allow_html=True)

                with col3:
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
