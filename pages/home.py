"""
Home Dashboard - Quick overview of modules
Clean, no marketing copy, focus on navigation
"""
import streamlit as st


def render():
    """Dashboard Home page - module overview only"""
    
    st.markdown("# Welcome to Kunsalt")
    st.markdown("Find universities, discover jobs, or connect with businesses.")
    st.markdown("")
    
    # Three module cards - dashboard style
    col1, col2, col3 = st.columns(3, gap="medium")
    
    # Education Module
    with col1:
        st.markdown("""
        <div class="card" style="text-align: center; padding: 2rem 1rem;">
            <div style="font-size: 2.5rem; margin-bottom: 1rem;">🎓</div>
            <h3 style="color: var(--accent);">Study Abroad</h3>
            <p>Browse universities, check rankings, and apply for admission.</p>
            <div style="margin-top: 1rem;">
        """, unsafe_allow_html=True)
        if st.button("Browse Universities", use_container_width=True, key="btn_edu"):
            st.session_state.selected_tab = "Education"
            st.rerun()
        st.markdown("</div></div>", unsafe_allow_html=True)
    
    # Jobs Module
    with col2:
        st.markdown("""
        <div class="card" style="text-align: center; padding: 2rem 1rem;">
            <div style="font-size: 2.5rem; margin-bottom: 1rem;">💼</div>
            <h3 style="color: var(--accent);">Find Jobs</h3>
            <p>Search jobs, match skills, and apply to opportunities.</p>
            <div style="margin-top: 1rem;">
        """, unsafe_allow_html=True)
        if st.button("Browse Jobs", use_container_width=True, key="btn_jobs"):
            st.session_state.selected_tab = "Jobs"
            st.rerun()
        st.markdown("</div></div>", unsafe_allow_html=True)
    
    # Business Module
    with col3:
        st.markdown("""
        <div class="card" style="text-align: center; padding: 2rem 1rem;">
            <div style="font-size: 2.5rem; margin-bottom: 1rem;">🏢</div>
            <h3 style="color: var(--accent);">B2B Services</h3>
            <p>Hire talent, get consulting, build your technical team.</p>
            <div style="margin-top: 1rem;">
        """, unsafe_allow_html=True)
        if st.button("View Solutions", use_container_width=True, key="btn_business"):
            st.session_state.selected_tab = "Business"
            st.rerun()
        st.markdown("</div></div>", unsafe_allow_html=True)
    
    # Quick Stats Row
    st.markdown("---")
    st.markdown("### Quick Stats")
    
    stat_col1, stat_col2, stat_col3, stat_col4 = st.columns(4)
    
    stats = [
        ("1,000+", "Universities"),
        ("5,000+", "Active Jobs"),
        ("500+", "Companies"),
        ("50+", "Countries"),
    ]
    
    for col, (number, label) in zip([stat_col1, stat_col2, stat_col3, stat_col4], stats):
        with col:
            st.markdown(f"""
            <div class="card" style="text-align: center; padding: 1.5rem;">
                <div style="font-size: 1.75rem; font-weight: bold; color: var(--accent); margin-bottom: 0.5rem;">{number}</div>
                <div style="font-size: 0.9rem; color: var(--text-secondary);">{label}</div>
            </div>
            """, unsafe_allow_html=True)
