"""
Business App Store user interface.
"""

from __future__ import annotations

import html
from datetime import datetime
from typing import Any, Dict

import streamlit as st

from services.appstore_service import AppStoreService


PER_PAGE = 12

STATE_PAGE = "business_store_page"
STATE_SEARCH = "business_store_search"
STATE_CATEGORY = "business_store_category"
STATE_TAGS = "business_store_tags"
STATE_SIGNATURE = "business_store_signature"
STATE_SELECTED_SLUG = "business_store_selected_slug"


def _init_state() -> None:
    defaults = {
        STATE_PAGE: 1,
        STATE_SEARCH: "",
        STATE_CATEGORY: "All",
        STATE_TAGS: [],
        STATE_SIGNATURE: None,
        STATE_SELECTED_SLUG: None,
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def _format_iso(iso_text: str) -> str:
    if not iso_text:
        return "-"
    try:
        dt = datetime.fromisoformat(str(iso_text).replace("Z", "+00:00"))
        return dt.strftime("%Y-%m-%d")
    except Exception:
        return str(iso_text)


def _render_tags(tags: list[str]) -> None:
    if not tags:
        return
    chips = "".join(f'<span class="badge">{html.escape(tag)}</span>' for tag in tags)
    st.markdown(f'<div class="result-tags">{chips}</div>', unsafe_allow_html=True)


def _render_download_button(service: AppStoreService, app: Dict[str, Any], key_prefix: str) -> None:
    payload = service.get_zip_bytes(int(app["id"]))
    if payload:
        st.download_button(
            "Download ZIP",
            data=payload,
            file_name=service.get_download_filename(app),
            mime="application/zip",
            key=f"{key_prefix}_dl_{app['id']}",
            use_container_width=True,
            on_click=service.increment_downloads,
            args=(int(app["id"]),),
        )
    else:
        st.button(
            "Download ZIP",
            disabled=True,
            key=f"{key_prefix}_dl_disabled_{app['id']}",
            use_container_width=True,
        )


def _render_detail_view(service: AppStoreService, app: Dict[str, Any]) -> None:
    top_left, top_right = st.columns([1, 1])
    with top_left:
        if st.button("Back to App Store", key="appstore_back_to_list", use_container_width=True):
            st.session_state[STATE_SELECTED_SLUG] = None
            st.rerun()
    with top_right:
        _render_download_button(service, app, "appstore_detail")

    st.markdown(
        f"""
        <article class="premium-card">
            <h2 class="result-title">{html.escape(str(app.get("name", "")))}</h2>
            <div class="result-meta">
                <span>Category: {html.escape(str(app.get("category", "Other")))}</span>
                <span>Version: {html.escape(str(app.get("version", "-")))}</span>
                <span>Last updated: {html.escape(_format_iso(str(app.get("updated_at", ""))))}</span>
                <span>Downloads: {int(app.get("downloads", 0))}</span>
            </div>
        </article>
        """,
        unsafe_allow_html=True,
    )

    _render_tags(app.get("tags", []))

    full_desc = str(app.get("full_desc") or app.get("short_desc") or "No detailed description available.")
    setup_instructions = str(app.get("setup_instructions") or "No setup instructions provided yet.")
    changelog = str(app.get("changelog") or "No changelog available yet.")

    st.markdown("### Description")
    st.write(full_desc)

    st.markdown("### Setup / Run Instructions")
    st.code(setup_instructions, language="text")

    st.markdown("### Changelog")
    st.code(changelog, language="text")


def render(service: AppStoreService) -> None:
    _init_state()

    st.markdown(
        """
        <section class="premium-hero">
            <div class="hero-kicker">Business</div>
            <h1 class="hero-title">App Store</h1>
            <p class="hero-sub">Browse business apps, check details, and download ZIP packages instantly.</p>
        </section>
        """,
        unsafe_allow_html=True,
    )

    selected_slug = st.session_state.get(STATE_SELECTED_SLUG)
    if selected_slug:
        app = service.get_app_by_slug(str(selected_slug), include_inactive=False)
        if not app:
            st.info("This app is no longer available in the store.")
            st.session_state[STATE_SELECTED_SLUG] = None
        else:
            _render_detail_view(service, app)
            return

    categories = ["All"] + service.get_categories(active_only=True)
    tags_available = service.get_all_tags(active_only=True)

    st.markdown('<div class="section-shell">', unsafe_allow_html=True)
    f1, f2, f3 = st.columns([1.8, 1.0, 1.4])
    with f1:
        st.text_input(
            "Search",
            placeholder="Search by app name or keywords",
            key=STATE_SEARCH,
            label_visibility="collapsed",
        )
    with f2:
        st.selectbox(
            "Category",
            options=categories,
            key=STATE_CATEGORY,
            label_visibility="collapsed",
        )
    with f3:
        st.multiselect(
            "Tags",
            options=tags_available,
            key=STATE_TAGS,
            placeholder="Filter by tags",
            label_visibility="collapsed",
        )
    st.markdown('</div>', unsafe_allow_html=True)

    signature = (
        str(st.session_state.get(STATE_SEARCH, "")).strip().lower(),
        str(st.session_state.get(STATE_CATEGORY, "All")),
        tuple(sorted([str(tag) for tag in st.session_state.get(STATE_TAGS, [])])),
    )
    if st.session_state.get(STATE_SIGNATURE) != signature:
        st.session_state[STATE_PAGE] = 1
        st.session_state[STATE_SIGNATURE] = signature

    page_data = service.list_apps(
        search=str(st.session_state.get(STATE_SEARCH, "")),
        category=str(st.session_state.get(STATE_CATEGORY, "All")),
        tags=list(st.session_state.get(STATE_TAGS, [])),
        page=int(st.session_state.get(STATE_PAGE, 1)),
        per_page=PER_PAGE,
        active_only=True,
    )

    st.session_state[STATE_PAGE] = int(page_data["page"])
    apps = list(page_data["items"])
    total = int(page_data["total"])
    total_pages = int(page_data["total_pages"])

    st.markdown(
        f'<div class="section-subtitle"><strong>{total}</strong> app(s) found</div>',
        unsafe_allow_html=True,
    )

    if not apps:
        st.info("No apps match your current filters.")
        return

    cols = st.columns(3, gap="large")
    for idx, app in enumerate(apps):
        with cols[idx % 3]:
            name = html.escape(str(app.get("name", "Untitled App")))
            category = html.escape(str(app.get("category", "Other")))
            version = html.escape(str(app.get("version", "-")))
            updated = html.escape(_format_iso(str(app.get("updated_at", ""))))
            downloads = int(app.get("downloads", 0))
            short_desc = str(app.get("short_desc") or "").strip() or "No short description available."
            if len(short_desc) > 180:
                short_desc = short_desc[:180].rstrip() + "..."

            st.markdown(
                f"""
                <article class="premium-card compact-card">
                    <h3 class="result-title">{name}</h3>
                    <div class="result-meta">
                        <span>{category}</span>
                        <span>Version: {version}</span>
                        <span>Updated: {updated}</span>
                    </div>
                    <p class="result-description">{html.escape(short_desc)}</p>
                    <div class="section-subtitle" style="margin:0 0 6px 0;">Downloads: {downloads}</div>
                </article>
                """,
                unsafe_allow_html=True,
            )
            _render_tags(app.get("tags", []))

            c1, c2 = st.columns(2)
            with c1:
                if st.button("View Details", key=f"appstore_view_{app['id']}", use_container_width=True):
                    st.session_state[STATE_SELECTED_SLUG] = app.get("slug")
                    st.rerun()
            with c2:
                _render_download_button(service, app, f"appstore_card_{app['id']}")

    nav1, nav2, nav3, nav4 = st.columns([1, 1, 1.4, 1.2])
    with nav1:
        if st.button(
            "Previous",
            use_container_width=True,
            disabled=int(st.session_state[STATE_PAGE]) <= 1,
            key="appstore_prev_page",
        ):
            st.session_state[STATE_PAGE] = max(1, int(st.session_state[STATE_PAGE]) - 1)
            st.rerun()
    with nav2:
        if st.button(
            "Next",
            use_container_width=True,
            disabled=int(st.session_state[STATE_PAGE]) >= total_pages,
            key="appstore_next_page",
        ):
            st.session_state[STATE_PAGE] = min(total_pages, int(st.session_state[STATE_PAGE]) + 1)
            st.rerun()
    with nav3:
        st.markdown(
            f'<div class="section-subtitle" style="text-align:center;margin-top:8px;">Page {int(st.session_state[STATE_PAGE])} of {total_pages}</div>',
            unsafe_allow_html=True,
        )
    with nav4:
        new_page = st.number_input(
            "Go to page",
            min_value=1,
            max_value=total_pages,
            value=int(st.session_state[STATE_PAGE]),
            step=1,
            key="appstore_page_input",
        )
        if int(new_page) != int(st.session_state[STATE_PAGE]):
            st.session_state[STATE_PAGE] = int(new_page)
            st.rerun()
