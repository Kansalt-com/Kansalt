from __future__ import annotations

import urllib.parse

import streamlit as st

from pages.business_admin import is_admin_authenticated, render_admin_access, render_admin_panel
from pages.business_appstore import render as render_app_store
from pages.ui_kit import render_hero
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
    "Business is already stable and we want to scale.",
    "Business growth has stagnated and profit is flat.",
    "Business is inconsistent with volatile monthly outcomes.",
    "Business is new and needs market entry support.",
    "Business has growth demand but operations are manual.",
]

STATUS_SOLUTIONS = {
    BUSINESS_STATUSES[0]: [
        "Expansion roadmap with region prioritization and branch-level performance KPIs.",
        "CRM and marketing automation stack for predictable lead generation.",
        "Inventory and demand forecasting workflows for multi-unit scaling.",
    ],
    BUSINESS_STATUSES[1]: [
        "Revenue leakage diagnosis with funnel analytics and conversion checkpoints.",
        "Retention campaign engine based on customer segment behavior.",
        "Pricing and mix optimization dashboards for margin-focused decisions.",
    ],
    BUSINESS_STATUSES[2]: [
        "Cashflow and margin control dashboard with early warning alerts.",
        "Demand stabilization strategy using seasonal and behavioral signals.",
        "Process automation to reduce waste and improve operating rhythm.",
    ],
    BUSINESS_STATUSES[3]: [
        "Launch stack for site, lead capture, CRM, and campaign execution.",
        "Market visibility strategy for local discovery and first customer acquisition.",
        "90-day operating system with weekly KPI tracking and accountability loops.",
    ],
    BUSINESS_STATUSES[4]: [
        "Workflow digitization for invoicing, inventory, and internal task tracking.",
        "Unified management dashboard for real-time business visibility.",
        "SOP-led automation to cut repeat errors and operational delays.",
    ],
}


@st.cache_resource
def _get_appstore_service() -> AppStoreService:
    return AppStoreService()


def _wa_link(message: str) -> str:
    digits = "".join(ch for ch in WHATSAPP_NUMBER if ch.isdigit())
    if not digits:
        return ""
    return f"https://wa.me/{digits}?text={urllib.parse.quote(message)}"


def _render_overview() -> None:
    render_hero(
        kicker="Business Advisory",
        title="Select your business scenario and receive a focused technology transformation plan.",
        subtitle=(
            "This module mirrors consulting workflows: diagnose current state, map interventions, "
            "and move into app-enabled execution through the business app store."
        ),
    )

    st.markdown('<section class="k-section reveal">', unsafe_allow_html=True)
    st.markdown('<div class="k-filter-head">Step 1: Business Category</div>', unsafe_allow_html=True)

    category_query = st.text_input(
        "Category Search",
        placeholder="Type category prefix, for example tea or retail",
        key="business_category_query",
        label_visibility="collapsed",
    ).strip()

    category_options = BUSINESS_CATEGORIES
    if category_query:
        category_options = [item for item in BUSINESS_CATEGORIES if item.lower().startswith(category_query.lower())]

    if not category_options:
        st.info("No category starts with that text. Try another prefix.")
        st.markdown('</section>', unsafe_allow_html=True)
        return

    selected_category = st.selectbox(
        "Business Category",
        options=category_options,
        key="business_selected_category",
    )

    st.markdown('<div class="k-filter-head" style="margin-top:0.8rem;">Step 2: Current Business Status</div>', unsafe_allow_html=True)
    selected_status = st.radio(
        "Current Status",
        options=BUSINESS_STATUSES,
        key="business_status_radio",
        label_visibility="collapsed",
    )

    st.markdown('<div class="k-filter-head" style="margin-top:0.9rem;">Recommended Solutions</div>', unsafe_allow_html=True)
    for solution in STATUS_SOLUTIONS[selected_status]:
        st.markdown(
            f"""
            <article class="k-card reveal">
                <p class="k-course" style="margin:0;">{solution}</p>
            </article>
            """,
            unsafe_allow_html=True,
        )

    message = (
        f"Hello Kansalt, my business category is {selected_category}. "
        f"Current status: {selected_status} Please share a practical technology plan."
    )
    wa_url = _wa_link(message)

    c1, c2 = st.columns([1.2, 1])
    with c1:
        st.markdown(
            '<div class="k-admin-note">Kansalt combines strategy and implementation. The output is an executable operating plan, not generic slideware.</div>',
            unsafe_allow_html=True,
        )
    with c2:
        if wa_url:
            st.link_button("Get Solution Plan", wa_url, use_container_width=True)
        else:
            st.button("Get Solution Plan", disabled=True, use_container_width=True)

    st.markdown('</section>', unsafe_allow_html=True)


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
