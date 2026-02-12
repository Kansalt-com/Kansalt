"""
Kansalt Education Tab - Study Abroad & University Guidance
Top European Universities with AI-powered consultation
"""
import streamlit as st
from typing import List, Dict
import sys
import os

project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# =====================================================
# MOCK UNIVERSITY DATA
# =====================================================
UNIVERSITIES = [
    {
        "rank": 1,
        "name": "TU Munich (Technische Universität München)",
        "country": "🇩🇪 Germany",
        "city": "Munich",
        "programs": ["Computer Science", "Engineering", "Business"],
        "tuition": "€50-90K/year",
        "intake": "October & April",
        "acceptance_rate": "15%",
        "rating": 4.8,
    },
    {
        "rank": 2,
        "name": "ETH Zurich (Swiss Federal Institute of Technology)",
        "country": "🇨🇭 Switzerland",
        "city": "Zurich",
        "programs": ["Engineering", "Computer Science", "Physics"],
        "tuition": "€100-150K/year",
        "intake": "September",
        "acceptance_rate": "8%",
        "rating": 4.9,
    },
    {
        "rank": 3,
        "name": "University of Amsterdam",
        "country": "🇳🇱 Netherlands",
        "city": "Amsterdam",
        "programs": ["MBA", "Computer Science", "Data Science"],
        "tuition": "€15-25K/year",
        "intake": "September & February",
        "acceptance_rate": "25%",
        "rating": 4.7,
    },
    {
        "rank": 4,
        "name": "KTH Royal Institute of Technology",
        "country": "🇸🇪 Sweden",
        "city": "Stockholm",
        "programs": ["Engineering", "Technology", "Architecture"],
        "tuition": "€13-17K/year",
        "intake": "September",
        "acceptance_rate": "12%",
        "rating": 4.6,
    },
    {
        "rank": 5,
        "name": "Sorbonne University (Paris)",
        "country": "🇫🇷 France",
        "city": "Paris",
        "programs": ["Law", "Business", "Sciences"],
        "tuition": "€3-8K/year",
        "intake": "September",
        "acceptance_rate": "30%",
        "rating": 4.5,
    },
    {
        "rank": 6,
        "name": "University of Milan",
        "country": "🇮🇹 Italy",
        "city": "Milan",
        "programs": ["Finance", "Management", "Medicine"],
        "tuition": "€1-5K/year",
        "intake": "September",
        "acceptance_rate": "35%",
        "rating": 4.4,
    },
]

FIELDS_OF_STUDY = [
    "All Fields",
    "Computer Science",
    "Engineering",
    "Business & MBA",
    "Law",
    "Medicine",
    "Data Science",
    "Architecture",
]

COUNTRIES = ["All", "Germany", "Netherlands", "France", "Sweden", "Italy", "Switzerland"]

DEGREE_TYPES = ["All", "Bachelor", "Master", "PhD"]

# =====================================================
# SESSION STATE
# =====================================================
if "edu_page" not in st.session_state:
    st.session_state.edu_page = 1

def render():
    """Main render function for Education tab."""
    
    # Header
    st.markdown("<h1 style='color: #ffffff; margin-bottom: 4px; text-shadow: 0 0 10px rgba(0, 255, 255, 0.3);'>🎓 Study Abroad</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color: #a1a1aa; font-size: 0.9rem; margin: 0; text-transform: uppercase; letter-spacing: 0.05em;'>Top universities · Expert guidance · Applications</p>", unsafe_allow_html=True)
    
    st.markdown("<div style='height: 16px;'></div>", unsafe_allow_html=True)
    
    # =====================================================
    # SIDEBAR FILTERS
    # =====================================================
    with st.sidebar:
        st.markdown("#### Filters")
        
        country_filter = st.multiselect(
            "Country",
            COUNTRIES,
            default=["All"],
            key="edu_country",
        )
        
        sort_by = st.selectbox(
            "Sort by",
            ["Ranking", "Affordability", "Rating"],
            key="edu_sort",
        )
    
    # =====================================================
    # FILTER LOGIC
    # =====================================================
    filtered_unis = UNIVERSITIES.copy()
    
    if "All" not in country_filter:
        filtered_unis = [u for u in filtered_unis if any(c in u["country"] for c in country_filter)]
    
    if sort_by == "Affordability":
        def get_tuition_value(uni):
            tuition_str = uni["tuition"].split("-")[0].replace("€", "").replace("K", "").strip()
            try:
                return float(tuition_str)
            except:
                return 1000
        filtered_unis.sort(key=get_tuition_value)
    elif sort_by == "Rating":
        filtered_unis.sort(key=lambda x: x["rating"], reverse=True)
    
    # =====================================================
    # RESULTS DISPLAY
    # =====================================================
    st.markdown(f"#### {len(filtered_unis)} Universities")
    st.markdown("")
    
    for uni in filtered_unis:
        # Clean card layout with cyberpunk theme
        st.markdown(f"""
        <div style='border: 1px solid rgba(0, 255, 255, 0.2); border-radius: 16px; padding: 24px; margin-bottom: 16px; background: rgba(229, 231, 235, 0.03); box-shadow: 0 0 20px rgba(124, 58, 237, 0.1);'>
            <div style='display: flex; justify-content: space-between; align-items: start; margin-bottom: 1rem;'>
                <div>
                    <h4 style='color: #ffffff; margin: 0; font-size: 1.1rem;'>{uni["name"]}</h4>
                    <p style='color: #a1a1aa; margin: 0.25rem 0 0 0; font-size: 0.9rem;'>{uni["country"]} • {uni["city"]}</p>
                </div>
                <div style='text-align: right;'>
                    <div style='font-size: 1.5rem; font-weight: 700; color: #f97316;'>#{uni["rank"]}</div>
                    <div style='font-size: 0.75rem; color: #00ffff; text-transform: uppercase;'>Ranking</div>
                </div>
            </div>
            
            <div style='display: grid; grid-template-columns: repeat(3, 1fr); gap: 1rem; margin: 1rem 0; padding: 1rem 0; border-top: 1px solid rgba(0, 255, 255, 0.1); border-bottom: 1px solid rgba(0, 255, 255, 0.1);'>
                <div>
                    <p style='color: #00ffff; font-size: 0.75rem; margin: 0; text-transform: uppercase; font-weight: 500;'>Tuition</p>
                    <p style='color: #ffffff; font-size: 0.95rem; margin: 0.5rem 0 0 0; font-weight: 500;'>{uni["tuition"]}</p>
                </div>
                <div>
                    <p style='color: #00ffff; font-size: 0.75rem; margin: 0; text-transform: uppercase; font-weight: 500;'>Rating</p>
                    <p style='color: #ffffff; font-size: 0.95rem; margin: 0.5rem 0 0 0; font-weight: 500;'>⭐ {uni["rating"]}</p>
                </div>
                <div>
                    <p style='color: #00ffff; font-size: 0.75rem; margin: 0; text-transform: uppercase; font-weight: 500;'>Acceptance</p>
                    <p style='color: #ffffff; font-size: 0.95rem; margin: 0.5rem 0 0 0; font-weight: 500;'>{uni["acceptance_rate"]}</p>
                </div>
            </div>
            
            <div style='margin: 1rem 0;'>
                <p style='color: #00ffff; font-size: 0.75rem; margin: 0 0 0.5rem 0; text-transform: uppercase; font-weight: 500;'>Programs</p>
                <div style='display: flex; gap: 0.5rem; flex-wrap: wrap;'>
        """, unsafe_allow_html=True)
        
        for prog in uni["programs"]:
            st.markdown(f"<span style='display: inline-block; padding: 6px 12px; background: rgba(249, 115, 22, 0.15); color: #f97316; border: 1px solid rgba(249, 115, 22, 0.3); border-radius: 10px; font-size: 0.85rem; font-weight: 500; text-transform: uppercase;'>{prog}</span>", unsafe_allow_html=True)
        
        st.markdown("""
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns([3, 1])
        with col2:
            if st.button("Get Free Consultation", use_container_width=True, key=f"uni_consult_{uni['name']}"):
                st.session_state.selected_uni = uni["name"]
                st.rerun()
        st.markdown("")
    
    # =====================================================
    # CONSULTATION FORM
    # =====================================================
    if "selected_uni" in st.session_state and st.session_state.selected_uni:
        st.markdown("---")
        st.markdown(f"#### 🎓 Free Consultation")
        st.markdown(f"Get personalized guidance for **{st.session_state.selected_uni}**")
        st.markdown("")
        
        col1, col2 = st.columns(2)
        with col1:
            name = st.text_input("Your name", key="consult_name")
        with col2:
            email = st.text_input("Email", key="consult_email")
        
        interest = st.text_area("Your interests & goals", key="consult_interest", height=80, placeholder="Tell us about yourself...")
        
        if st.button("Send Request", use_container_width=True, type="primary"):
            st.success("✅ Thank you! We'll contact you within 24 hours.")
            st.session_state.selected_uni = None
            st.rerun()
        
        st.markdown("")

if __name__ == "__main__":
    render()
