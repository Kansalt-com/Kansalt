"""
Business page - overview advisory + app store + admin workflows.
"""

import urllib.parse

import streamlit as st

from pages.business_admin import is_admin_authenticated, render_admin_access, render_admin_panel
from pages.business_appstore import render as render_app_store
from services.appstore_service import AppStoreService


WHATSAPP_NUMBER = "+91-8555052189"

BUSINESS_CATEGORIES = [
    "Tea Shop",
    "Tea Manufacturing",
    "Tea Export Business",
    "Textile Manufacturing",
    "Textile Retail",
    "Travel Agency",
    "Transport and Logistics",
    "Restaurant",
    "Cafe",
    "E-commerce Store",
    "Retail Store",
    "Pharmacy",
    "Clinic and Healthcare Center",
    "Construction Company",
    "Real Estate Agency",
    "Education Institute",
    "Coaching Center",
    "IT Services Company",
    "Digital Marketing Agency",
    "Legal Services Firm",
    "Accounting and Finance Firm",
    "Beauty and Wellness Salon",
    "Gym and Fitness Center",
    "Automobile Service Center",
    "Manufacturing Unit",
]

BUSINESS_STATUSES = [
    "1. Business is running good and we want to expand.",
    "2. Business is stagnant and profit is not increasing.",
    "3. Business is unstable: some months profit, some months loss.",
    "4. Business is new and we need market entry + first customers.",
    "5. Operations are growing but systems are manual and inefficient.",
]

STATUS_SOLUTIONS = {
    BUSINESS_STATUSES[0]: [
        "Expansion roadmap with market prioritization and branch-level KPI dashboards.",
        "CRM + marketing automation to scale lead generation and retention.",
        "Inventory and demand forecasting setup for multi-location growth.",
    ],
    BUSINESS_STATUSES[1]: [
        "Revenue leakage audit with sales funnel analytics and conversion tracking.",
        "Customer segmentation + targeted campaign engine for repeat business.",
        "Pricing and product mix insights using BI dashboards.",
    ],
    BUSINESS_STATUSES[2]: [
        "Cashflow and margin tracking system with early warning alerts.",
        "Demand stabilization plan using seasonal trend analytics.",
        "Operational cost optimization with process automation.",
    ],
    BUSINESS_STATUSES[3]: [
        "Launch stack: website, lead capture, CRM, and campaign setup.",
        "Digital presence and local discoverability strategy.",
        "First 90-day execution plan with weekly business metrics.",
    ],
    BUSINESS_STATUSES[4]: [
        "Workflow digitization: invoicing, inventory, and task tracking.",
        "Management dashboard for real-time business visibility.",
        "SOP-driven automation to reduce manual errors and delays.",
    ],
}


def _wa_link(message: str) -> str:
    digits = "".join(ch for ch in WHATSAPP_NUMBER if ch.isdigit())
    if not digits:
        return ""
    return f"https://wa.me/{digits}?text={urllib.parse.quote(message)}"


@st.cache_resource
def _get_appstore_service() -> AppStoreService:
    return AppStoreService()


def _render_overview() -> None:
    st.markdown(
        """
        <section class="premium-hero">
            <div class="hero-kicker">Business</div>
            <h1 class="hero-title">Tech Solutions For Every Business Category</h1>
            <p class="hero-sub">Select your business category and current status. We will map the right technology interventions for growth, stability, and efficiency.</p>
        </section>
        """,
        unsafe_allow_html=True,
    )

    st.markdown('<div class="section-shell">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Step 1: Select Business Category</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-subtitle">Autocomplete is prefix-based. Example: type "tea" to see categories starting with tea.</div>', unsafe_allow_html=True)

    query = st.text_input(
        "Search business category",
        placeholder="Type category prefix (e.g., tea, text, travel)",
        key="business_category_query",
    ).strip()

    filtered_categories = BUSINESS_CATEGORIES
    if query:
        filtered_categories = [c for c in BUSINESS_CATEGORIES if c.lower().startswith(query.lower())]

    if not filtered_categories:
        st.info("No category starts with this text. Try another prefix.")
        st.markdown('</div>', unsafe_allow_html=True)
        return

    selected_category = st.selectbox(
        "Business category",
        options=filtered_categories,
        key="business_selected_category",
        help="Dropdown supports typeahead; list is already filtered by your prefix.",
    )

    st.markdown('<div class="section-title" style="margin-top:10px;">Step 2: Select Current Business Status</div>', unsafe_allow_html=True)
    selected_status = st.radio(
        "Current status",
        options=BUSINESS_STATUSES,
        key="business_status_radio",
    )

    st.markdown('<div class="section-title" style="margin-top:10px;">Recommended Tech-Based Solutions</div>', unsafe_allow_html=True)
    for item in STATUS_SOLUTIONS[selected_status]:
        st.markdown(
            f'<article class="premium-card business-card"><p class="result-description" style="margin:0;">{item}</p></article>',
            unsafe_allow_html=True,
        )

    msg = (
        f"Hello Kansalt, my business category is {selected_category}. "
        f"Current status: {selected_status} Please share a tech solution plan."
    )
    wa = _wa_link(msg)

    c1, c2 = st.columns(2)
    with c1:
        st.markdown('<div class="new-market-note">We are a new market entrant focused on practical implementation, not generic consulting decks.</div>', unsafe_allow_html=True)
    with c2:
        if wa:
            st.link_button("Get Solution Plan on WhatsApp", wa, use_container_width=True)
        else:
            st.button("Get Solution Plan on WhatsApp", disabled=True, use_container_width=True)

    st.markdown('</div>', unsafe_allow_html=True)


def render() -> None:
    service = _get_appstore_service()

    tab_names = ["Overview", "App Store"]
    if is_admin_authenticated():
        tab_names.append("Admin")

    tabs = st.tabs(tab_names)
    with tabs[0]:
        _render_overview()
    with tabs[1]:
        render_app_store(service)

    if is_admin_authenticated() and len(tabs) > 2:
        with tabs[2]:
            render_admin_panel(service)
    else:
        render_admin_access(service)

