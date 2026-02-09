"""
Kansalt Businesses Tool - Explore business opportunities
"""
import streamlit as st


def render():
    st.set_page_config(
        layout="wide",
        page_title="Kansalt - Businesses",
        page_icon="🏢",
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
        st.markdown('<div style="font-size: 1.5rem; font-weight: 700; background: linear-gradient(135deg, #3B82F6 0%, #22C55E 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;">🚀 Kansalt - Businesses</div>', unsafe_allow_html=True)
    with col_nav:
        col_back, col_home = st.columns([1, 1])
        with col_back:
            if st.button("← Back", use_container_width=True, key="bus_btn_back"):
                st.session_state.selected_tool = None
                st.rerun()
        with col_home:
            st.markdown("🏢 Businesses Tool")

    st.markdown("---")

    # Main content
    st.markdown("## 🏢 Businesses Tool")
    st.markdown("**Coming Soon!** Explore business opportunities and entrepreneurship resources.")

    with st.container(border=True):
        st.markdown("### Features We're Building:")
        st.markdown("""
        - 🚀 **Startup Opportunities** - Find promising startups and growth companies
        - 💰 **Investment Options** - Discover investment and funding opportunities
        - 🤝 **Business Partnerships** - Connect with potential business partners
        - 📊 **Market Analysis** - Research industries and business trends
        - 🏆 **Success Stories** - Learn from successful entrepreneurs
        - 💼 **Franchise Opportunities** - Explore franchise options
        - 🎯 **Business Consulting** - Access expert business advice
        - 📈 **Growth Strategies** - Scale your business with proven tactics
        """)

    with st.container(border=True):
        st.markdown("### Business Categories:")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown("**Tech Startups** - Innovative technology companies")
        with col2:
            st.markdown("**E-commerce** - Online retail businesses")
        with col3:
            st.markdown("**Services** - Professional service companies")

    st.markdown("---")
    st.markdown("### 🚀 Get Notified When Ready!")

    email = st.text_input("Enter your email to be notified:", placeholder="you@example.com")
    if st.button("Notify Me", use_container_width=True, type="primary"):
        if email:
            st.success("✓ We'll notify you when Businesses Tool is ready!")
        else:
            st.error("Please enter a valid email")

    st.markdown("---")
    st.markdown("""
    <div class="footer">
        <p><strong>Kansalt Businesses Tool</strong> | Coming Soon</p>
        <p>Made with ❤️ | <a href="https://github.com" target="_blank">GitHub</a> | Contact: hello@kansalt.io</p>
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    render()
