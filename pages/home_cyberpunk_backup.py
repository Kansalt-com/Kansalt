import streamlit as st


def render():
    """Dashboard Home page — Premium SaaS, data-driven, professional."""
    
    # Quick Stats / Header Section
    st.markdown("""
    <div style='background: linear-gradient(135deg, #1a0b2e 0%, #0f051a 100%); padding: 32px; margin-bottom: 24px; border-radius: 16px; border: 1px solid rgba(0, 255, 255, 0.2); box-shadow: 0 0 20px rgba(124, 58, 237, 0.15);'>
        <div style='max-width: 1200px; margin: 0 auto;'>
            <h1 style='font-size: 2rem; font-weight: 700; color: #ffffff; margin-bottom: 8px; text-shadow: 0 0 10px rgba(0, 255, 255, 0.3);'>Welcome to Kunsalt</h1>
            <p style='font-size: 0.95rem; color: #a1a1aa; margin: 0;'>Your platform for education, careers, and business solutions.</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Dashboard Grid - Three Main Modules
    st.markdown("<h2 style='font-size: 1.4rem; font-weight: 600; color: #ffffff; margin-bottom: 16px; margin-top: 24px; text-transform: uppercase; letter-spacing: 0.05em;'>Modules</h2>", unsafe_allow_html=True)
    
    cols = st.columns(3, gap="medium")
    
    # Education Module Card
    with cols[0]:
        st.markdown("""
        <div style='background: rgba(229, 231, 235, 0.03); border: 1px solid rgba(0, 255, 255, 0.2); border-radius: 12px; padding: 20px; transition: all 200ms cubic-bezier(0.4, 0, 0.2, 1); box-shadow: 0 0 20px rgba(124, 58, 237, 0.1);'>
            <div style='display: flex; align-items: center; margin-bottom: 16px;'>
                <div style='font-size: 1.8rem; margin-right: 12px;'>🎓</div>
                <h3 style='font-size: 1rem; font-weight: 700; color: #ffffff; margin: 0;'>Education</h3>
            </div>
            <p style='color: #a1a1aa; font-size: 0.9rem; line-height: 1.5; margin: 0 0 12px 0;'>Top universities · Guidance · Applications</p>
            <div style='display: flex; gap: 8px;'>
                <div style='flex: 1; background: rgba(249, 115, 22, 0.15); padding: 8px 12px; border-radius: 8px; font-size: 0.8rem; text-align: center; color: #f97316; font-weight: 500; text-transform: uppercase;'>Browse</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Explore Education", key="dash_edu", use_container_width=True):
            st.session_state.selected_tab = "Education"
            st.rerun()
    
    # Jobs Module Card
    with cols[1]:
        st.markdown("""
        <div style='background: rgba(229, 231, 235, 0.03); border: 1px solid rgba(0, 255, 255, 0.2); border-radius: 12px; padding: 20px; transition: all 200ms cubic-bezier(0.4, 0, 0.2, 1); box-shadow: 0 0 20px rgba(124, 58, 237, 0.1);'>
            <div style='display: flex; align-items: center; margin-bottom: 16px;'>
                <div style='font-size: 1.8rem; margin-right: 12px;'>💼</div>
                <h3 style='font-size: 1rem; font-weight: 700; color: #ffffff; margin: 0;'>Jobs</h3>
            </div>
            <p style='color: #a1a1aa; font-size: 0.9rem; line-height: 1.5; margin: 0 0 12px 0;'>Skill matching · Curated roles · Tools</p>
            <div style='display: flex; gap: 8px;'>
                <div style='flex: 1; background: rgba(249, 115, 22, 0.15); padding: 8px 12px; border-radius: 8px; font-size: 0.8rem; text-align: center; color: #f97316; font-weight: 500; text-transform: uppercase;'>Search</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Find Jobs", key="dash_jobs", use_container_width=True):
            st.session_state.selected_tab = "Jobs"
            st.rerun()
    
    # Business Module Card
    with cols[2]:
        st.markdown("""
        <div style='background: rgba(229, 231, 235, 0.03); border: 1px solid rgba(0, 255, 255, 0.2); border-radius: 12px; padding: 20px; transition: all 200ms cubic-bezier(0.4, 0, 0.2, 1); box-shadow: 0 0 20px rgba(124, 58, 237, 0.1);'>
            <div style='display: flex; align-items: center; margin-bottom: 16px;'>
                <div style='font-size: 1.8rem; margin-right: 12px;'>🏢</div>
                <h3 style='font-size: 1rem; font-weight: 700; color: #ffffff; margin: 0;'>Business</h3>
            </div>
            <p style='color: #a1a1aa; font-size: 0.9rem; line-height: 1.5; margin: 0 0 12px 0;'>Tech solutions · Consulting · Staffing</p>
            <div style='display: flex; gap: 8px;'>
                <div style='flex: 1; background: rgba(249, 115, 22, 0.15); padding: 8px 12px; border-radius: 8px; font-size: 0.8rem; text-align: center; color: #f97316; font-weight: 500; text-transform: uppercase;'>Explore</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Business Solutions", key="dash_business", use_container_width=True):
            st.session_state.selected_tab = "Business"
            st.rerun()
    
    # Quick Access Section
    st.markdown("<h2 style='font-size: 1.4rem; font-weight: 600; color: #ffffff; margin-bottom: 16px; margin-top: 32px; text-transform: uppercase; letter-spacing: 0.05em;'>Quick Access</h2>", unsafe_allow_html=True)
    
    st.markdown("""
    <div style='display: grid; grid-template-columns: repeat(2, 1fr); gap: 16px;'>
        <div style='background: rgba(229, 231, 235, 0.03); border: 1px solid rgba(0, 255, 255, 0.2); border-radius: 12px; padding: 16px;'>
            <p style='font-size: 0.85rem; color: #00ffff; margin: 0 0 8px 0; text-transform: uppercase; font-weight: 500;'>Recent Activity</p>
            <p style='color: #a1a1aa; font-size: 0.9rem; margin: 0;'>Start exploring universities, jobs, and services today.</p>
        </div>
        <div style='background: rgba(229, 231, 235, 0.03); border: 1px solid rgba(0, 255, 255, 0.2); border-radius: 12px; padding: 16px;'>
            <p style='font-size: 0.85rem; color: #00ffff; margin: 0 0 8px 0; text-transform: uppercase; font-weight: 500;'>Dashboard Features</p>
            <p style='color: #a1a1aa; font-size: 0.9rem; margin: 0;'>Personalized recommendations · Smart filters · Saved items.</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<div style='height: 24px;'></div>", unsafe_allow_html=True)
    
    # Footer
    st.markdown("""
    <div style='text-align: center; color: #6b7280; font-size: 0.8rem; padding-top: 24px; border-top: 1px solid rgba(0, 255, 255, 0.1); text-transform: uppercase; letter-spacing: 0.05em;'>
        <p style='margin: 8px 0;'>© 2026 Kunsalt | <a href='#' style='color: #f97316; text-decoration: none;'>Docs</a> · <a href='#' style='color: #f97316; text-decoration: none;'>Support</a> · <a href='#' style='color: #f97316; text-decoration: none;'>Status</a></p>
    </div>
    """, unsafe_allow_html=True)


