"""
Kansalt.com - Multi-Tool Professional Platform
Landing page with 3 main tools: Jobs, Education, Businesses
"""
import streamlit as st
import sys
import os

# Add project root to path for imports
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# =========================================================================
# DISPATCH TO TOOLS
# =========================================================================
if "selected_tool" not in st.session_state:
    st.session_state.selected_tool = None

if st.session_state.selected_tool:
    sel = st.session_state.selected_tool
    if sel == "jobs":
        from pages import jobs
        jobs.render()
        st.stop()
    elif sel == "education":
        from pages import education
        education.render()
        st.stop()
    elif sel == "businesses":
        from pages import businesses
        businesses.render()
        st.stop()

# =========================================================================
# PAGE CONFIG
# =========================================================================
st.set_page_config(
    layout="wide",
    page_title="Kansalt - Professional Tools",
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

    .main {
        background: #0B1220 !important;
    }

    /* Headings */
    h1, h2, h3, h4, h5, h6 {
        color: #E5E7EB !important;
    }

    /* Text */
    p, span, label {
        color: #E5E7EB !important;
    }

    /* Tool Cards */
    .tool-card {
        background: linear-gradient(135deg, #111A2E 0%, #1A2744 100%);
        border: 1px solid #1F2A44;
        border-radius: 16px;
        padding: 3rem;
        margin-bottom: 2rem;
        transition: all 0.3s ease;
        cursor: pointer;
        text-align: center;
    }

    .tool-card:hover {
        border-color: #3B82F6;
        box-shadow: 0 0 30px rgba(59, 130, 246, 0.2);
        transform: translateY(-5px);
    }

    .tool-icon {
        font-size: 4rem;
        margin-bottom: 1rem;
        display: block;
    }

    .tool-title {
        font-size: 1.75rem;
        font-weight: 700;
        color: #E5E7EB;
        margin-bottom: 1rem;
    }

    .tool-description {
        color: #94A3B8;
        font-size: 1rem;
        line-height: 1.6;
        margin-bottom: 2rem;
    }

    .tool-button {
        background: linear-gradient(135deg, #3B82F6 0%, #22C55E 100%);
        color: white;
        border: none;
        padding: 0.75rem 2rem;
        border-radius: 8px;
        font-weight: 600;
        cursor: pointer;
        transition: all 0.3s ease;
        font-size: 1rem;
    }

    .tool-button:hover {
        opacity: 0.9;
        transform: scale(1.05);
    }

    /* Hero Section */
    .hero {
        text-align: center;
        padding: 4rem 2rem;
        background: linear-gradient(135deg, rgba(59, 130, 246, 0.1) 0%, rgba(34, 197, 94, 0.1) 100%);
        border-radius: 16px;
        margin-bottom: 4rem;
        border: 1px solid #1F2A44;
    }

    .hero h1 {
        font-size: 3rem;
        background: linear-gradient(135deg, #3B82F6 0%, #22C55E 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 1rem;
        font-weight: 800;
    }

    .hero p {
        font-size: 1.25rem;
        color: #94A3B8;
        margin-bottom: 2rem;
        max-width: 600px;
        margin-left: auto;
        margin-right: auto;
    }

    /* Features Grid */
    .features {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
        gap: 2rem;
        margin-bottom: 4rem;
    }

    .feature-item {
        background: #111A2E;
        border: 1px solid #1F2A44;
        border-radius: 12px;
        padding: 1.5rem;
    }

    .feature-icon {
        font-size: 2rem;
        margin-bottom: 1rem;
    }

    .feature-title {
        font-weight: 600;
        margin-bottom: 0.5rem;
        color: #3B82F6;
    }

    .feature-text {
        font-size: 0.9rem;
        color: #94A3B8;
    }

    /* Footer */
    .footer {
        background: #111A2E;
        border-top: 1px solid #1F2A44;
        padding: 3rem;
        text-align: center;
        color: #94A3B8;
        font-size: 0.875rem;
        margin-top: 4rem;
        border-radius: 12px;
    }

    .footer a {
        color: #3B82F6;
        text-decoration: none;
    }

    .footer a:hover {
        text-decoration: underline;
    }

    /* Buttons */
    .stButton > button {
        border-radius: 8px !important;
    }

    .stButton > button:hover {
        border-color: #3B82F6 !important;
    }

    /* Input Fields */
    .stTextInput > div > div > input,
    .stSelectbox > div > div > select,
    .stNumberInput > div > div > input {
        background: #1F2A44 !important;
        color: #E5E7EB !important;
        border: 1px solid #1F2A44 !important;
        border-radius: 8px !important;
    }

    .stTextInput > div > div > input:focus,
    .stSelectbox > div > div > select:focus,
    .stNumberInput > div > div > input:focus {
        background: #2D3E52 !important;
        color: #E5E7EB !important;
        border-color: #3B82F6 !important;
    }

    /* Dividers */
    hr {
        border: none;
        border-top: 1px solid #1F2A44;
        margin: 2rem 0;
    }
</style>
""", unsafe_allow_html=True)

# =========================================================================
# NAVBAR
# =========================================================================
col_brand, col_spacer, col_auth = st.columns([2, 3, 2])

with col_brand:
    st.markdown('<div style="font-size: 1.8rem; font-weight: 800; background: linear-gradient(135deg, #3B82F6 0%, #22C55E 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;">🚀 Kansalt.com</div>', unsafe_allow_html=True)

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
            st.info("You're browsing as a guest")

st.markdown("---")

# =========================================================================
# HERO SECTION
# =========================================================================
st.markdown("""
<div class="hero">
    <h1>Welcome to Kansalt</h1>
    <p>Your all-in-one professional platform for finding jobs, learning, and growing your business</p>
</div>
""", unsafe_allow_html=True)

# =========================================================================
# TOOLS SECTION
# =========================================================================
st.markdown("### 🛠️ Our Tools")
st.markdown("")

col1, col2, col3 = st.columns(3, gap="large")

# Tool 1: Jobs
with col1:
    st.markdown("""
    <div class="tool-card">
        <span class="tool-icon">💼</span>
        <div class="tool-title">Jobs</div>
        <div class="tool-description">
            Search and apply for remote jobs from 35+ sources. Get personalized job matches based on your skills and experience. Optimize your resume for each job with AI-powered tailoring.
        </div>
    </div>
    """, unsafe_allow_html=True)

    if st.button("Open Jobs Tool →", use_container_width=True, key="btn_jobs"):
        st.session_state.selected_tool = "jobs"
        st.rerun()

# Tool 2: Education
with col2:
    st.markdown("""
    <div class="tool-card">
        <span class="tool-icon">🎓</span>
        <div class="tool-title">Education</div>
        <div class="tool-description">
            Discover online courses, certifications, and learning paths to upskill. Find programs that match your career goals and budget. Track your learning progress and earn certificates.
        </div>
    </div>
    """, unsafe_allow_html=True)

    if st.button("Open Education Tool →", use_container_width=True, key="btn_education"):
        st.session_state.selected_tool = "education"
        st.rerun()

# Tool 3: Businesses
with col3:
    st.markdown("""
    <div class="tool-card">
        <span class="tool-icon">🏢</span>
        <div class="tool-title">Businesses</div>
        <div class="tool-description">
            Explore business opportunities, startups, and investment options. Find partnerships and growth strategies. Connect with entrepreneurs and investors in your field.
        </div>
    </div>
    """, unsafe_allow_html=True)

    if st.button("Open Businesses Tool →", use_container_width=True, key="btn_businesses"):
        st.session_state.selected_tool = "businesses"
        st.rerun()

# =========================================================================
# FEATURES SECTION
# =========================================================================
st.markdown("---")
st.markdown("### ✨ Why Choose Kansalt?")

st.markdown("""
<div class="features">
    <div class="feature-item">
        <div class="feature-icon">⚡</div>
        <div class="feature-title">Fast & Efficient</div>
        <div class="feature-text">Get real-time results from 35+ job sources instantly</div>
    </div>
    <div class="feature-item">
        <div class="feature-icon">🎯</div>
        <div class="feature-title">Smart Matching</div>
        <div class="feature-text">AI-powered job matching based on your skills</div>
    </div>
    <div class="feature-item">
        <div class="feature-icon">📄</div>
        <div class="feature-title">Resume Optimizer</div>
        <div class="feature-text">Intelligently tailor resumes for each job</div>
    </div>
    <div class="feature-item">
        <div class="feature-icon">🌍</div>
        <div class="feature-title">Global Opportunities</div>
        <div class="feature-text">Find remote jobs from companies worldwide</div>
    </div>
    <div class="feature-item">
        <div class="feature-icon">📊</div>
        <div class="feature-title">Data-Driven</div>
        <div class="feature-text">Analytics and insights for better decisions</div>
    </div>
    <div class="feature-item">
        <div class="feature-icon">🔒</div>
        <div class="feature-title">Secure & Private</div>
        <div class="feature-text">Your data is protected with enterprise-grade security</div>
    </div>
</div>
""", unsafe_allow_html=True)

# =========================================================================
# FOOTER
# =========================================================================
st.markdown("---")
st.markdown("""
<div class="footer">
    <p><strong>Kansalt.com</strong> v2.0 | Your Professional Platform</p>
    <p>🚀 Empowering careers through technology | 
       <a href="https://github.com" target="_blank">GitHub</a> | 
       <a href="mailto:hello@kansalt.com">Contact Us</a></p>
    <p style="margin-top: 1rem; font-size: 0.75rem; color: #64748B;">
        © 2026 Kansalt. All rights reserved. | 
        <a href="#" target="_blank">Privacy Policy</a> | 
        <a href="#" target="_blank">Terms of Service</a>
    </p>
</div>
""", unsafe_allow_html=True)
