"""
Education page with searchable university list, practical filters, and WhatsApp application CTA.
"""

import os
import urllib.parse
from typing import Dict, List

import streamlit as st


WHATSAPP_NUMBER = os.getenv("WHATSAPP_NUMBER", "")

UNIVERSITIES: List[Dict[str, object]] = [
    {
        "id": 1,
        "name": "University of Toronto",
        "country": "Canada",
        "budget_tier": "High",
        "scholarship": True,
        "fee_structure": "Tuition: CAD 45,000/year | Living: CAD 16,000/year",
        "course_details": "Strong programs in Computer Science, Data Science, and Engineering with co-op opportunities.",
        "link": "https://www.utoronto.ca/",
    },
    {
        "id": 2,
        "name": "University of Melbourne",
        "country": "Australia",
        "budget_tier": "High",
        "scholarship": True,
        "fee_structure": "Tuition: AUD 44,000/year | Living: AUD 21,000/year",
        "course_details": "Popular for Business Analytics, IT, and Health sciences with strong global rankings.",
        "link": "https://www.unimelb.edu.au/",
    },
    {
        "id": 3,
        "name": "Technical University of Munich",
        "country": "Germany",
        "budget_tier": "Low",
        "scholarship": True,
        "fee_structure": "Tuition: Minimal/semester contribution | Living: EUR 12,000/year",
        "course_details": "Well known for engineering and applied sciences; strong research and industry collaboration.",
        "link": "https://www.tum.de/en/",
    },
    {
        "id": 4,
        "name": "National University of Singapore",
        "country": "Singapore",
        "budget_tier": "Medium",
        "scholarship": True,
        "fee_structure": "Tuition: SGD 30,000/year | Living: SGD 15,000/year",
        "course_details": "Leading Asian university with strong Computer Engineering, AI, and Finance programs.",
        "link": "https://www.nus.edu.sg/",
    },
    {
        "id": 5,
        "name": "University of Birmingham",
        "country": "UK",
        "budget_tier": "Medium",
        "scholarship": True,
        "fee_structure": "Tuition: GBP 25,000/year | Living: GBP 11,000/year",
        "course_details": "Offers strong postgraduate pathways in Business, Law, and life sciences.",
        "link": "https://www.birmingham.ac.uk/",
    },
    {
        "id": 6,
        "name": "Arizona State University",
        "country": "USA",
        "budget_tier": "Medium",
        "scholarship": True,
        "fee_structure": "Tuition: USD 34,000/year | Living: USD 14,000/year",
        "course_details": "Career-focused degrees in technology, management, and design with industry projects.",
        "link": "https://www.asu.edu/",
    },
]

COUNTRIES = ["All", "USA", "UK", "Canada", "Australia", "Germany", "Singapore"]
BUDGET_OPTIONS = ["All", "Low", "Medium", "High"]
SCHOLARSHIP_OPTIONS = ["All", "Yes", "No"]


def _wa_link(message: str) -> str:
    digits = "".join(ch for ch in WHATSAPP_NUMBER if ch.isdigit())
    if not digits:
        return ""
    return f"https://wa.me/{digits}?text={urllib.parse.quote(message)}"


def _apply_filters(universities: List[Dict[str, object]], search: str, country: str, budget: str, scholarship: str) -> List[Dict[str, object]]:
    filtered = universities[:]

    s = search.strip().lower()
    if s:
        filtered = [
            u for u in filtered
            if s in str(u.get("name", "")).lower() or s in str(u.get("course_details", "")).lower()
        ]

    if country != "All":
        filtered = [u for u in filtered if u.get("country") == country]

    if budget != "All":
        filtered = [u for u in filtered if u.get("budget_tier") == budget]

    if scholarship == "Yes":
        filtered = [u for u in filtered if bool(u.get("scholarship"))]
    elif scholarship == "No":
        filtered = [u for u in filtered if not bool(u.get("scholarship"))]

    return filtered


def render() -> None:
    st.markdown('<section class="premium-hero">', unsafe_allow_html=True)
    st.markdown('<div class="hero-kicker">Education</div>', unsafe_allow_html=True)
    st.markdown('<h1 class="hero-title">Study Abroad Search</h1>', unsafe_allow_html=True)
    st.markdown('<p class="hero-sub">Search by budget, destination country, and scholarship availability.</p>', unsafe_allow_html=True)
    st.markdown('</section>', unsafe_allow_html=True)

    st.markdown('<div class="section-shell">', unsafe_allow_html=True)
    st.markdown('<div class="search-panel">', unsafe_allow_html=True)

    f1, f2, f3, f4 = st.columns([1.7, 1.1, 1.1, 1.1])

    with f1:
        search = st.text_input("Search colleges/universities", placeholder="Search by university or course", label_visibility="collapsed")

    with f2:
        country = st.selectbox("Country", options=COUNTRIES, label_visibility="collapsed")

    with f3:
        budget = st.selectbox("Budget", options=BUDGET_OPTIONS, label_visibility="collapsed")

    with f4:
        scholarship = st.selectbox("Scholarship", options=SCHOLARSHIP_OPTIONS, label_visibility="collapsed")

    st.markdown('</div>', unsafe_allow_html=True)

    results = _apply_filters(UNIVERSITIES, search, country, budget, scholarship)

    st.markdown(f'<div class="section-subtitle"><strong>{len(results)}</strong> result(s) found</div>', unsafe_allow_html=True)

    if not results:
        st.info("No universities found for the selected filters.")
        st.markdown('</div>', unsafe_allow_html=True)
        return

    for uni in results:
        st.markdown('<article class="premium-card education-card">', unsafe_allow_html=True)
        st.markdown(f'<h3 class="result-title">{uni["name"]}</h3>', unsafe_allow_html=True)
        st.markdown(f'<div class="result-meta"><span>{uni["country"]}</span><span>Budget: {uni["budget_tier"]}</span><span>Scholarship: {"Yes" if uni["scholarship"] else "No"}</span></div>', unsafe_allow_html=True)
        st.markdown(f'<div class="fee-strip">{uni["fee_structure"]}</div>', unsafe_allow_html=True)
        st.markdown(f'<p class="result-description">{uni["course_details"]}</p>', unsafe_allow_html=True)

        c1, c2 = st.columns([1, 1])
        with c1:
            st.link_button("University Website", str(uni["link"]), use_container_width=True)

        with c2:
            msg = (
                f"Hello Kunsalt, I want to apply for {uni['name']} in {uni['country']}. "
                f"Please guide me with admission steps and document checklist."
            )
            wa_url = _wa_link(msg)
            if wa_url:
                st.link_button("Submit Application", wa_url, use_container_width=True)
            else:
                st.button("Submit Application", disabled=True, use_container_width=True, key=f"apply_disabled_{uni['id']}")

        st.markdown('</article>', unsafe_allow_html=True)

    if not WHATSAPP_NUMBER:
        st.caption("Set WHATSAPP_NUMBER environment variable to enable Submit Application on WhatsApp.")

    st.markdown('</div>', unsafe_allow_html=True)
