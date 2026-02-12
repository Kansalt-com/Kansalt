"""
Education Dashboard - University browser
Two-column layout: filters (left sidebar) + results (right)
"""
import streamlit as st

# Sample universities data
UNIVERSITIES = [
    {
        "id": 1,
        "name": "Stanford University",
        "country": "USA",
        "city": "Stanford, CA",
        "rank": 1,
        "rating": 4.9,
        "tuition": "$60K/year",
        "acceptance_rate": "3.2%",
        "programs": ["Computer Science", "Engineering", "Business", "Medicine"],
    },
    {
        "id": 2,
        "name": "MIT",
        "country": "USA",
        "city": "Cambridge, MA",
        "rank": 2,
        "rating": 4.9,
        "tuition": "$62K/year",
        "acceptance_rate": "3.3%",
        "programs": ["Engineering", "Computer Science", "Physics", "Mathematics"],
    },
    {
        "id": 3,
        "name": "University of Oxford",
        "country": "UK",
        "city": "Oxford",
        "rank": 3,
        "rating": 4.8,
        "tuition": "$45K/year",
        "acceptance_rate": "15%",
        "programs": ["Liberal Arts", "Engineering", "Business", "Law"],
    },
    {
        "id": 4,
        "name": "Harvard University",
        "country": "USA",
        "city": "Cambridge, MA",
        "rank": 4,
        "rating": 4.9,
        "tuition": "$63K/year",
        "acceptance_rate": "3.4%",
        "programs": ["Medicine", "Law", "Business", "Arts & Sciences"],
    },
    {
        "id": 5,
        "name": "Cambridge University",
        "country": "UK",
        "city": "Cambridge",
        "rank": 5,
        "rating": 4.8,
        "tuition": "$46K/year",
        "acceptance_rate": "17%",
        "programs": ["Mathematics", "Sciences", "Engineering", "Humanities"],
    },
]

COUNTRIES = ["All", "USA", "UK", "Canada", "Australia", "Germany", "Singapore"]
DEGREES = ["All", "Bachelor", "Master", "PhD"]

def render():
    """Education Dashboard - Universities browser"""
    
    st.markdown("# 🎓 Study Abroad")
    st.markdown("Find top universities and apply for admission.")
    
    # Initialize session state
    if "edu_country" not in st.session_state:
        st.session_state.edu_country = "All"
    if "edu_degree" not in st.session_state:
        st.session_state.edu_degree = "All"
    if "edu_sort" not in st.session_state:
        st.session_state.edu_sort = "Ranking"
    if "edu_search" not in st.session_state:
        st.session_state.edu_search = ""

    # Two-column layout: Sidebar + Results
    col_sidebar, col_results = st.columns([1, 3.5], gap="large")

    # =========================================================================
    # LEFT SIDEBAR - FILTERS
    # =========================================================================
    with col_sidebar:
        st.markdown('<div class="sidebar-filters">', unsafe_allow_html=True)
        st.markdown("### 🔍 Filters")
        
        # Search
        st.markdown('<div class="filter-section">', unsafe_allow_html=True)
        st.markdown('<div class="filter-label">University Name</div>', unsafe_allow_html=True)
        search = st.text_input("Search", placeholder="e.g., Stanford", label_visibility="collapsed")
        st.session_state.edu_search = search
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Country filter
        st.markdown('<div class="filter-section">', unsafe_allow_html=True)
        st.markdown('<div class="filter-label">Country</div>', unsafe_allow_html=True)
        country = st.selectbox("Select country", COUNTRIES, label_visibility="collapsed", index=0)
        st.session_state.edu_country = country
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Degree filter
        st.markdown('<div class="filter-section">', unsafe_allow_html=True)
        st.markdown('<div class="filter-label">Degree Level</div>', unsafe_allow_html=True)
        degree = st.selectbox("Select degree", DEGREES, label_visibility="collapsed", index=0)
        st.session_state.edu_degree = degree
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Sort filter
        st.markdown('<div class="filter-section">', unsafe_allow_html=True)
        st.markdown('<div class="filter-label">Sort By</div>', unsafe_allow_html=True)
        sort_by = st.selectbox("Sort", ["Ranking", "Rating", "Affordability"], label_visibility="collapsed", index=0)
        st.session_state.edu_sort = sort_by
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)

    # =========================================================================
    # RIGHT SIDE - RESULTS
    # =========================================================================
    with col_results:
        # Filter universities
        filtered_unis = UNIVERSITIES.copy()
        
        if search:
            filtered_unis = [u for u in filtered_unis if search.lower() in u["name"].lower()]
        
        if country != "All":
            filtered_unis = [u for u in filtered_unis if u["country"] == country]
        
        # Sorting
        if sort_by == "Rating":
            filtered_unis.sort(key=lambda x: x["rating"], reverse=True)
        elif sort_by == "Affordability":
            filtered_unis.sort(key=lambda x: float(x["tuition"].split("$")[1].split("/")[0].replace("K", "000")))
        else:  # Ranking
            filtered_unis.sort(key=lambda x: x["rank"])
        
        # Results header
        st.markdown(f'<div style="font-size: 0.95rem; color: var(--text-secondary); margin-bottom: 1.5rem;"><strong>{len(filtered_unis)} universities found</strong></div>', unsafe_allow_html=True)
        
        # Display results
        if filtered_unis:
            for uni in filtered_unis:
                st.markdown('<div class="result-item">', unsafe_allow_html=True)
                
                # Header with rank
                col1, col2 = st.columns([5, 1])
                with col1:
                    st.markdown(f'<h3 class="result-title">#{uni["rank"]} {uni["name"]}</h3>', unsafe_allow_html=True)
                    st.markdown(f'<p style="margin: 0.25rem 0; color: var(--text-secondary);">{uni["city"]}, {uni["country"]}</p>', unsafe_allow_html=True)
                
                with col2:
                    st.markdown(f'<div style="text-align: right;"><div style="font-size: 1.1rem; font-weight: 600; color: var(--accent);">⭐ {uni["rating"]}</div></div>', unsafe_allow_html=True)
                
                # Key stats
                st.markdown(f'<div class="result-meta">', unsafe_allow_html=True)
                st.markdown(f'<span>💰 {uni["tuition"]}</span>', unsafe_allow_html=True)
                st.markdown(f'<span>📊 Acceptance: {uni["acceptance_rate"]}</span>', unsafe_allow_html=True)
                st.markdown(f'</div>', unsafe_allow_html=True)
                
                # Programs
                st.markdown('<div class="result-tags">', unsafe_allow_html=True)
                for program in uni["programs"]:
                    st.markdown(f'<span class="badge">{program}</span>', unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)
                
                # Action button
                if st.button("📝 Get Free Consultation", use_container_width=True, key=f"consult_{uni['id']}"):
                    st.success(f"Consultation request sent for {uni['name']}")
                
                st.markdown('</div>', unsafe_allow_html=True)
                st.markdown('<hr style="margin: 1rem 0;">', unsafe_allow_html=True)
        else:
            st.info("No universities found. Try adjusting your filters.")
