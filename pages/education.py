"""
Kansalt Education Tool - Discover courses and learning paths
"""
import streamlit as st


def render():
    st.set_page_config(
        layout="wide",
        page_title="Kansalt - Education",
        page_icon="🎓",
        initial_sidebar_state="collapsed",
    )

    # Dark theme
    st.markdown("""
    <style>
        body, html {
            background: #0B1220 !important;
            color: #E5E7EB !important;
        }
        .main { background: #0B1220 !important; }
        h1, h2, h3, h4, h5, h6 { color: #E5E7EB !important; }
        p, span, label { color: #E5E7EB !important; }
        hr { border: none; border-top: 1px solid #1F2A44; }
        .footer {
            background: #111A2E;
            border-top: 1px solid #1F2A44;
            padding: 2rem;
            text-align: center;
            color: #94A3B8;
            font-size: 0.875rem;
            margin-top: 4rem;
        }
        .footer a { color: #3B82F6; text-decoration: none; }
        .footer a:hover { text-decoration: underline; }
    </style>
    """, unsafe_allow_html=True)

    # Navbar
    col_brand, col_spacer, col_nav = st.columns([2, 3, 2])
    with col_brand:
        st.markdown('<div style="font-size: 1.5rem; font-weight: 700; background: linear-gradient(135deg, #3B82F6 0%, #22C55E 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;">🚀 Kansalt - Education</div>', unsafe_allow_html=True)
    with col_nav:
        col_back, col_home = st.columns([1, 1])
        with col_back:
            if st.button("← Back", use_container_width=True, key="edu_btn_back"):
                st.session_state.selected_tool = None
                st.rerun()
        with col_home:
            st.markdown("🎓 Education Tool")

    st.markdown("---")

    # Main content
    st.markdown("## 🎓 Education Tool")
    st.markdown("**Coming Soon!** We're building the ultimate learning discovery platform.")

    with st.container(border=True):
        st.markdown("### Features We're Building:")
        st.markdown("""
        - 📚 **Course Discovery** - Find courses from top platforms (Coursera, Udemy, edX, etc.)
        - 🎯 **Learning Paths** - Personalized career development roadmaps
        - 💰 **Budget Filtering** - Find affordable courses within your budget
        - 📊 **Progress Tracking** - Track your learning journey and certificates
        - 🏆 **Skill Certification** - Earn recognized certificates that boost your resume
        - 🎓 **Degree Programs** - Explore online degree options
        - 🤝 **Mentorship** - Connect with industry experts and mentors
        - 📈 **Career Matching** - Courses aligned with job opportunities
        """)

    with st.container(border=True):
        st.markdown("### Popular Learning Platforms:")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown("**Coursera** - Courses from top universities")
        with col2:
            st.markdown("**Udemy** - Affordable skill-specific courses")
        with col3:
            st.markdown("**edX** - University-backed courses")

    st.markdown("---")
    st.markdown("### 🚀 Get Notified When Ready!")

    email = st.text_input("Enter your email to be notified:", placeholder="you@example.com")
    if st.button("Notify Me", use_container_width=True, type="primary"):
        if email:
            st.success("✓ We'll notify you when Education Tool is ready!")
        else:
            st.error("Please enter a valid email")

    st.markdown("---")
    st.markdown("""
    <div class="footer">
        <p><strong>Kansalt Education Tool</strong> | Coming Soon</p>
        <p>Made with ❤️ | <a href="https://github.com" target="_blank">GitHub</a> | Contact: hello@kansalt.io</p>
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    render()
