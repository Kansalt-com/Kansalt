import streamlit as st
import sys
import os
from pathlib import Path   # already needed

# FIX: project_root must be defined before CSS load
project_root = Path(__file__).resolve().parents[1]

# Add project root to path
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

# LOAD GLOBAL STYLES
css_file = project_root / "public" / "styles.css"
if css_file.exists():
    st.markdown(
        f"""
        <style>
        {css_file.read_text(encoding="utf-8")}

        /* ensure app content is above animated background */
        .stApp,
        [data-testid="stAppViewContainer"],
        [data-testid="stMain"] {{
            position: relative;
            z-index: 2;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )


# =====================================================
# ADD PROJECT ROOT TO PATH
# =====================================================
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# =====================================================
# NEW: LOAD GLOBAL CSS (public/styles.css)
# =====================================================
def load_global_css():
    css_path = Path(project_root) / "public" / "styles.css"
    if css_path.exists():
        st.markdown(
            f"<style>{css_path.read_text(encoding='utf-8')}</style>",
            unsafe_allow_html=True
        )
    else:
        st.error(f"styles.css not found at {css_path}")

load_global_css()

# =====================================================
# IMPORT TAB RENDER FUNCTIONS
# =====================================================
from pages.home import render as render_home
from pages.education import render as render_education
from pages.jobs import render as render_jobs
from pages.business import render as render_business

# =====================================================
# PAGE CONFIG
# =====================================================
st.set_page_config(
    layout="wide",
    page_title="Kansalt - Jobs Dashboard",
    page_icon="💼",
    initial_sidebar_state="expanded",
)

# =====================================================
# YOUR EXISTING INLINE STYLE (UNCHANGED)
# =====================================================
st.markdown("""
<style>
    :root {
        --primary-bg: #F4FAFA;
        --secondary-bg: #E6F4F3;
        --card-bg: #FFFFFF;
        --accent: #0F766E;
        --accent-secondary: #14B8A6;
        --accent-light: #99F6E4;
        --text-primary: #0F172A;
        --text-secondary: #475569;
        --text-muted: #6B7280;
        --border: #D1FAF5;
        --card-radius: 8px;
        --duration: 200ms;
        --ease: cubic-bezier(0.4, 0, 0.2, 1);
    }

    html, body, main {
        background: var(--primary-bg) !important;
        color: var(--text-primary) !important;
        font-family: 'Segoe UI', Arial, sans-serif !important;
        line-height: 1.5;
        font-size: 0.97rem;
        min-height: 100vh;
    }
</style>
""", unsafe_allow_html=True)

# =====================================================
# SESSION STATE
# =====================================================
if "selected_tab" not in st.session_state:
    st.session_state.selected_tab = "Home"

if "last_search_results" not in st.session_state:
    st.session_state.last_search_results = []

# =====================================================
# GLOBAL NAVBAR
# =====================================================
st.markdown('<div class="navbar-container">', unsafe_allow_html=True)

navbar_col1, navbar_col2, navbar_col3 = st.columns([1, 2, 1])

with navbar_col1:
    st.markdown('<div class="navbar-brand">💼 Kansalt</div>', unsafe_allow_html=True)

with navbar_col2:
    col_home, col_ed, col_jobs, col_bus = st.columns([1, 1, 1, 1])

    with col_home:
        if st.button("🏠 Home", use_container_width=True):
            st.session_state.selected_tab = "Home"
            st.rerun()

    with col_ed:
        if st.button("🎓 Education", use_container_width=True):
            st.session_state.selected_tab = "Education"
            st.rerun()

    with col_jobs:
        if st.button("💼 Jobs", use_container_width=True):
            st.session_state.selected_tab = "Jobs"
            st.rerun()

    with col_bus:
        if st.button("🏢 Business", use_container_width=True):
            st.session_state.selected_tab = "Business"
            st.rerun()

with navbar_col3:
    st.markdown(
        '<div style="text-align: right; font-size: 0.85rem; color: var(--text-muted);">👤 Login</div>',
        unsafe_allow_html=True
    )

st.markdown('</div>', unsafe_allow_html=True)

# =====================================================
# TAB DISPATCH
# =====================================================
if st.session_state.selected_tab == "Home":
    render_home()
elif st.session_state.selected_tab == "Education":
    render_education()
elif st.session_state.selected_tab == "Business":
    render_business()
else:
    render_jobs()

