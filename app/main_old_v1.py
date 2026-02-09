"""
Kansalt.com - Premium Remote Job Aggregator
Streamlit Frontend
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
    normalize_jobs, compute_pagination
)
from utils import get_logger

logger = get_logger(__name__)

# =========================================================================
# PAGE CONFIG & BRANDING
# =========================================================================
st.set_page_config(
    layout="wide",
    page_title="Kansalt.com - Remote Jobs",
    page_icon="🚀",
    initial_sidebar_state="expanded",
)

# Custom CSS for premium look
st.markdown("""
<style>
    .kansalt-header {
        text-align: center;
        margin-bottom: 2rem;
    }
    .kansalt-title {
        font-size: 2.5rem;
        font-weight: 700;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    .job-row {
        display: flex;
        padding: 1rem;
        border-bottom: 1px solid #f0f0f0;
        align-items: center;
        gap: 1rem;
        transition: background-color 0.2s;
    }
    .job-row:hover {
        background-color: #f9f9f9;
    }
    .match-badge-high {
        background-color: #10b981;
        color: white;
        padding: 0.25rem 0.75rem;
        border-radius: 9999px;
        font-weight: 600;
        font-size: 0.875rem;
    }
    .match-badge-med {
        background-color: #f59e0b;
        color: white;
        padding: 0.25rem 0.75rem;
        border-radius: 9999px;
        font-weight: 600;
        font-size: 0.875rem;
    }
    .match-badge-low {
        background-color: #6b7280;
        color: white;
        padding: 0.25rem 0.75rem;
        border-radius: 9999px;
        font-weight: 600;
        font-size: 0.875rem;
    }
    .pagination-info {
        text-align: center;
        font-size: 0.875rem;
        color: #666;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# =========================================================================
# HEADER
# =========================================================================
st.markdown('<div class="kansalt-header">', unsafe_allow_html=True)
st.markdown('<h1 class="kansalt-title">Kansalt.com</h1>', unsafe_allow_html=True)
st.markdown("**Premium Remote Job Aggregator** | Find your perfect role from 10+ sources")
st.markdown('</div>', unsafe_allow_html=True)

# =========================================================================
# SESSION STATE INITIALIZATION
# =========================================================================
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.user_name = None

if "resume_text" not in st.session_state:
    st.session_state.resume_text = ""
    st.session_state.candidate_name = ""
    st.session_state.candidate_email = ""
    st.session_state.candidate_phone = ""

if "last_search_results" not in st.session_state:
    st.session_state.last_search_results = []

if "last_search_meta" not in st.session_state:
    st.session_state.last_search_meta = {}

if "generated_docs" not in st.session_state:
    st.session_state.generated_docs = {}

if "results_page" not in st.session_state:
    st.session_state.results_page = 1

if "results_per_page" not in st.session_state:
    st.session_state.results_per_page = 25

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
# SIDEBAR: AUTHENTICATION & RESUME UPLOAD
# =========================================================================
with st.sidebar:
    st.header("📋 User & Resume")

    if not st.session_state.logged_in:
        auth_mode = st.radio("Choose action:", ["Guest", "Login", "Register"])

        if auth_mode == "Login":
            with st.form("login_form"):
                email = st.text_input("Email")
                password = st.text_input("Password", type="password")
                if st.form_submit_button("Login"):
                    st.session_state.logged_in = True
                    st.session_state.user_name = email
                    st.success(f"Logged in as {email}")
                    st.rerun()

        elif auth_mode == "Register":
            with st.form("register_form"):
                name = st.text_input("Full Name")
                email = st.text_input("Email")
                password = st.text_input("Password", type="password")
                if st.form_submit_button("Register"):
                    st.session_state.logged_in = True
                    st.session_state.user_name = name
                    st.success(f"Registered and logged in as {name}")
                    st.rerun()

        else:  # Guest
            st.info("👤 Browsing as guest. Upload resume to generate tailored documents.")

    else:
        st.success(f"✓ Logged in: {st.session_state.user_name}")
        if st.button("Logout"):
            st.session_state.logged_in = False
            st.session_state.user_name = None
            st.rerun()

    st.divider()

    # Resume upload
    st.subheader("📄 Resume Upload")
    resume_file = st.file_uploader("Upload PDF or DOCX (optional)", type=["pdf", "docx"])

    if resume_file:
        try:
            file_bytes = resume_file.read()
            if resume_file.type == "application/pdf":
                text = ResumeParser.extract_text_from_pdf(file_bytes)
            else:
                text = ResumeParser.extract_text_from_docx(file_bytes)

            st.session_state.resume_text = text
            st.session_state.candidate_name = ResumeParser.extract_name(text) or "Candidate"
            st.session_state.candidate_email = ResumeParser.extract_email(text) or ""
            st.session_state.candidate_phone = ResumeParser.extract_phone(text) or ""

            st.success(f"✓ Loaded: {st.session_state.candidate_name}")
            logger.info(f"Resume loaded for {st.session_state.candidate_name}")

        except Exception as e:
            st.error(f"Resume parsing error: {e}")
            logger.error(f"Resume parsing error: {e}")

# =========================================================================
# MAIN CONTENT: SEARCH & RESULTS
# =========================================================================
tab_search, tab_results = st.tabs(["🔍 Search Jobs", "📊 Results"])

# ===== SEARCH TAB =====
with tab_search:
    col1, col2 = st.columns([1, 1])

    with col1:
        st.subheader("Search Criteria")

        job_profile = st.text_input(
            "Job Profile/Role (e.g., DevOps Engineer, Medical Coder)",
            placeholder="Enter job title or role",
            help="Optional but recommended. Leave blank and select skills instead.",
        )

        skill_category = st.radio("Skill Type:", ["All", "IT Only", "Non-IT Only"])
        available_skills = (
            it_skills + non_it_skills if skill_category == "All"
            else it_skills if skill_category == "IT Only"
            else non_it_skills
        )

        selected_skills = st.multiselect(
            "Select Skills:",
            available_skills,
            help="Select one or more skills to search for.",
        )

        manual_skills_text = st.text_input(
            "Add custom skills (comma-separated)",
            placeholder="e.g., Kubernetes, Python, Medical Billing",
            help="Add skills not in the list above.",
        )
        manual_skills = [s.strip() for s in manual_skills_text.split(",") if s.strip()]

    with col2:
        st.subheader("Filters")

        location_options = [
            "Remote", "United States", "United Kingdom", "Canada",
            "India", "Australia", "Germany", "Netherlands", "Europe"
        ]
        locations = st.multiselect(
            "Locations:",
            location_options,
            default=["Remote"],
            help="Select one or more locations.",
        )

        date_filter = st.selectbox(
            "Posted within:",
            ["all", "24h", "1w", "2w", "1m"],
            format_func=lambda x: {
                "all": "Any time",
                "24h": "Last 24 hours",
                "1w": "Last week",
                "2w": "Last 2 weeks",
                "1m": "Last month"
            }[x],
            help="Filter jobs by posting date.",
        )

        min_match = st.slider(
            "Minimum match %",
            0, 100, 10, 5,
            help="Only show jobs matching at least this % of search criteria.",
        )

        # Set defaults
        st.session_state.results_per_page = 25
        match_weight = 60
        freshness_weight = 40

    # Search button
    col_search, col_clear = st.columns([1, 1])
    with col_search:
        search_clicked = st.button("🔎 Search Jobs", use_container_width=True, type="primary")
    with col_clear:
        clear_clicked = st.button("🗑️ Clear Results", use_container_width=True)

    # Validation and search
    if search_clicked:
        if not job_profile.strip() and not selected_skills and not manual_skills:
            st.error("⚠️ Provide at least ONE of: Job Profile, Selected Skills, or Custom Skills.")
            st.stop()

        with st.spinner("🔄 Fetching jobs from 10+ sources..."):
            logger.info(f"Search initiated: profile={job_profile}, skills={selected_skills}, manual={manual_skills}")

            try:
                jobs = fetch_all_jobs(
                    selected_skills=selected_skills,
                    skills_db=skills_db,
                    job_profile=job_profile.strip(),
                    locations=locations if locations else ["Remote"],
                    manual_terms=manual_skills,
                    date_filter=date_filter,
                    min_match=min_match,
                    max_results=500,
                    match_weight=match_weight,
                    freshness_weight=freshness_weight,
                )

                # Normalize jobs for consistent UI display
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
                    "match_weight": match_weight,
                    "freshness_weight": freshness_weight,
                }

                st.success(f"✓ Found {len(normalized_jobs)} matching jobs!")
                st.rerun()

            except Exception as e:
                st.error(f"Search error: {e}")
                logger.error(f"Search error: {e}", exc_info=True)

    if clear_clicked:
        st.session_state.last_search_results = []
        st.session_state.last_search_meta = {}
        st.session_state.generated_docs = {}
        st.session_state.results_page = 1
        st.rerun()

# ===== RESULTS TAB =====
with tab_results:
    results = st.session_state.last_search_results
    meta = st.session_state.last_search_meta

    if not results:
        st.info("📭 No results yet. Use the 'Search Jobs' tab to find jobs.")
    else:
        # Compute pagination
        page_size = st.session_state.results_per_page
        pagination = compute_pagination(len(results), st.session_state.results_page, page_size)

        # Top toolbar
        col_info, col_page, col_sort = st.columns([2, 1, 1])

        with col_info:
            st.markdown(f"**{pagination['display_text']}** jobs")

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

        with col_sort:
            st.selectbox("Sort by:", ["Match ↓", "Posted ↓", "Company"], disabled=False, label_visibility="collapsed")

        st.divider()

        # Get paginated results
        paginated_results = results[pagination["start_idx"]:pagination["end_idx"]]

        # Render results as clean rows
        for idx, job in enumerate(paginated_results):
            job_code = job.get("job_code", "unknown")
            title = job.get("title", "Untitled")
            company = job.get("company", "Unknown")
            location = job.get("location", "Remote")
            match_pct = job.get("match_percent", 0)
            posted_ago = job.get("posted_ago", "—")
            apply_url = job.get("apply_url", "")

            # Render job row (Posted | Job Code | Title | Company | Location | Match % | Apply)
            col1, col2, col3, col4, col5, col6, col7 = st.columns([0.8, 1, 2.5, 1.5, 1.5, 0.8, 1.5])

            with col1:
                st.caption(posted_ago)

            with col2:
                st.caption(f"`{job_code[:12]}`")

            with col3:
                st.markdown(f"**{title}**")

            with col4:
                st.caption(company)

            with col5:
                st.caption(location)

            with col6:
                # Match badge
                if match_pct >= 70:
                    st.markdown(f'<span class="match-badge-high">{match_pct}%</span>', unsafe_allow_html=True)
                elif match_pct >= 40:
                    st.markdown(f'<span class="match-badge-med">{match_pct}%</span>', unsafe_allow_html=True)
                else:
                    st.markdown(f'<span class="match-badge-low">{match_pct}%</span>', unsafe_allow_html=True)

            with col7:
                # Action buttons
                if apply_url and apply_url.startswith("http"):
                    st.link_button("Apply →", apply_url, use_container_width=True)
                else:
                    st.button("Apply", disabled=True, use_container_width=True)

            # Document generation buttons (below the row)
            if st.session_state.resume_text:
                col_res, col_letter = st.columns([1, 1])

                with col_res:
                    if st.button("📄 Resume", key=f"resume_{job_code}_{idx}", use_container_width=True):
                        try:
                            resume_bytes = DocumentBuilder.build_tailored_resume(
                                base_resume_text=st.session_state.resume_text,
                                candidate_name=st.session_state.candidate_name,
                                email=st.session_state.candidate_email,
                                phone=st.session_state.candidate_phone,
                                job=job,
                                selected_skills=meta.get("selected_skills", []),
                                manual_skills=meta.get("manual_skills", []),
                            )

                            if job_code not in st.session_state.generated_docs:
                                st.session_state.generated_docs[job_code] = {}

                            st.session_state.generated_docs[job_code]["resume"] = resume_bytes
                            st.success("✓ Resume generated")

                        except Exception as e:
                            st.error(f"Error: {e}")
                            logger.error(f"Resume generation error: {e}")

                with col_letter:
                    if st.button("📧 Cover Letter", key=f"letter_{job_code}_{idx}", use_container_width=True):
                        try:
                            letter_bytes = DocumentBuilder.build_cover_letter(
                                candidate_name=st.session_state.candidate_name,
                                email=st.session_state.candidate_email,
                                phone=st.session_state.candidate_phone,
                                job=job,
                                base_resume_text=st.session_state.resume_text,
                                selected_skills=meta.get("selected_skills", []),
                                manual_skills=meta.get("manual_skills", []),
                            )

                            if job_code not in st.session_state.generated_docs:
                                st.session_state.generated_docs[job_code] = {}

                            st.session_state.generated_docs[job_code]["cover_letter"] = letter_bytes
                            st.success("✓ Cover letter generated")

                        except Exception as e:
                            st.error(f"Error: {e}")
                            logger.error(f"Cover letter error: {e}")

            # Download buttons
            if job_code in st.session_state.generated_docs:
                gen_docs = st.session_state.generated_docs[job_code]
                col_dl1, col_dl2 = st.columns([1, 1])

                if "resume" in gen_docs:
                    with col_dl1:
                        st.download_button(
                            "⬇️ Download Resume",
                            data=gen_docs["resume"],
                            file_name=f"{st.session_state.candidate_name}_{job_code}_Resume.docx",
                            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                            key=f"dl_resume_{job_code}",
                            use_container_width=True,
                        )

                if "cover_letter" in gen_docs:
                    with col_dl2:
                        st.download_button(
                            "⬇️ Download Cover Letter",
                            data=gen_docs["cover_letter"],
                            file_name=f"{st.session_state.candidate_name}_{job_code}_CoverLetter.docx",
                            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                            key=f"dl_letter_{job_code}",
                            use_container_width=True,
                        )

            st.divider()

        # Pagination info at bottom
        if pagination["total_pages"] > 1:
            st.markdown(
                f'<div class="pagination-info">Page {pagination["current_page"]} of {pagination["total_pages"]}</div>',
                unsafe_allow_html=True
            )

# =========================================================================
# FOOTER
# =========================================================================
st.divider()
st.markdown(
    """
    **Kansalt.com** — Premium Remote Job Aggregator  
    Sourced from Remotive, ArbeitNow, The Himalayas, and 8+ RSS feeds  
    💡 Upload your resume to auto-generate tailored resumes and cover letters  
    🔒 Privacy: No data stored without your consent
    """
)
