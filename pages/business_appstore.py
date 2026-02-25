from __future__ import annotations

import html
from datetime import datetime
from typing import Any, Dict, List

import streamlit as st

from pages.ui_kit import empty_state, render_hero
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


def _render_tags(tags: List[str]) -> str:
    if not tags:
        return ""
    return "".join(f'<span class="k-badge">{html.escape(tag)}</span>' for tag in tags)


def _render_install_button(service: AppStoreService, app: Dict[str, Any], key_prefix: str) -> None:
    payload = service.get_zip_bytes(int(app["id"]))
    if payload:
        st.download_button(
            "Install",
            data=payload,
            file_name=service.get_download_filename(app),
            mime="application/zip",
            key=f"{key_prefix}_install_{app['id']}",
            use_container_width=True,
            on_click=service.increment_downloads,
            args=(int(app["id"]),),
        )
    else:
        st.button(
            "Install",
            disabled=True,
            key=f"{key_prefix}_install_disabled_{app['id']}",
            use_container_width=True,
        )


def _render_detail_view(service: AppStoreService, app: Dict[str, Any]) -> None:
    c1, c2 = st.columns([1, 1])
    with c1:
        if st.button("Back to App Store", key="appstore_back_btn", use_container_width=True):
            st.session_state[STATE_SELECTED_SLUG] = None
            st.rerun()
    with c2:
        _render_install_button(service, app, "detail")

    st.markdown(
        f"""
        <article class="k-app-card reveal">
            <h2 class="k-app-title">{html.escape(str(app.get('name', 'Untitled App')))}</h2>
            <div class="k-uni-meta">
                <span>Category: {html.escape(str(app.get('category', 'Other')))}</span>
                <span>Version: {html.escape(str(app.get('version', '-')))}</span>
                <span>Updated: {html.escape(_format_iso(str(app.get('updated_at', ''))))}</span>
                <span>Downloads: {int(app.get('downloads', 0) or 0)}</span>
            </div>
            <p class="k-course">{html.escape(str(app.get('full_desc') or app.get('short_desc') or 'No detailed description available.'))}</p>
            <div class="k-badge-row">{_render_tags(list(app.get('tags', [])))}</div>
        </article>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("### Setup and Run")
    st.code(str(app.get("setup_instructions") or "No setup instructions provided."), language="text")

    st.markdown("### Changelog")
    st.code(str(app.get("changelog") or "No changelog provided."), language="text")


def render(service: AppStoreService) -> None:
    _init_state()

    render_hero(
        kicker="Business App Store",
        title="Install and launch business-ready applications from a clean app-store experience.",
        subtitle=(
            "Browse by category and tags, review descriptions, and download deployable packages. "
            "Admin users can continuously onboard new apps from ZIP uploads or local project folders."
        ),
    )

    selected_slug = st.session_state.get(STATE_SELECTED_SLUG)
    if selected_slug:
        app = service.get_app_by_slug(str(selected_slug), include_inactive=False)
        if not app:
            st.info("This app is currently unavailable.")
            st.session_state[STATE_SELECTED_SLUG] = None
        else:
            _render_detail_view(service, app)
            return

    categories = ["All"] + service.get_categories(active_only=True)
    tags_available = service.get_all_tags(active_only=True)

    st.markdown('<section class="k-section reveal">', unsafe_allow_html=True)
    st.markdown('<div class="k-filter-head">App Catalog Filters</div>', unsafe_allow_html=True)

    f1, f2, f3 = st.columns([1.8, 1.0, 1.4])
    with f1:
        st.text_input(
            "Search",
            placeholder="Search app name or keyword",
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

    st.markdown('</section>', unsafe_allow_html=True)

    signature = (
        str(st.session_state.get(STATE_SEARCH, "")).strip().lower(),
        str(st.session_state.get(STATE_CATEGORY, "All")),
        tuple(sorted(str(tag) for tag in st.session_state.get(STATE_TAGS, []))),
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
        f'<div class="k-result-count reveal"><strong>{total}</strong> apps available.</div>',
        unsafe_allow_html=True,
    )

    if not apps:
        empty_state("No apps found", "Try clearing filters or searching with a broader keyword.")
        return

    st.markdown('<div class="k-app-grid">', unsafe_allow_html=True)
    for app in apps:
        name = html.escape(str(app.get("name", "Untitled App")))
        category = html.escape(str(app.get("category", "Other")))
        version = html.escape(str(app.get("version", "-")))
        updated = html.escape(_format_iso(str(app.get("updated_at", ""))))
        downloads = int(app.get("downloads", 0) or 0)

        short_desc = str(app.get("short_desc") or "No description available.").strip()
        if len(short_desc) > 180:
            short_desc = short_desc[:180].rstrip() + "..."

        st.markdown(
            f"""
            <article class="k-app-card reveal" id="app_{app['id']}">
                <h3 class="k-app-title">{name}</h3>
                <div class="k-uni-meta">
                    <span>{category}</span>
                    <span>v{version}</span>
                    <span>Updated: {updated}</span>
                </div>
                <p class="k-course">{html.escape(short_desc)}</p>
                <div class="k-subtle">Downloads: {downloads}</div>
                <div class="k-badge-row">{_render_tags(list(app.get('tags', [])))}</div>
            </article>
            """,
            unsafe_allow_html=True,
        )

        a1, a2 = st.columns(2)
        with a1:
            if st.button("Launch", key=f"launch_{app['id']}", use_container_width=True):
                st.session_state[STATE_SELECTED_SLUG] = app.get("slug")
                st.rerun()
        with a2:
            _render_install_button(service, app, f"card_{app['id']}")

    st.markdown('</div>', unsafe_allow_html=True)

    n1, n2, n3, n4 = st.columns([1, 1, 1.2, 1.4])
    with n1:
        if st.button(
            "Previous",
            key="app_prev",
            use_container_width=True,
            disabled=int(st.session_state[STATE_PAGE]) <= 1,
        ):
            st.session_state[STATE_PAGE] = max(1, int(st.session_state[STATE_PAGE]) - 1)
            st.rerun()
    with n2:
        if st.button(
            "Next",
            key="app_next",
            use_container_width=True,
            disabled=int(st.session_state[STATE_PAGE]) >= total_pages,
        ):
            st.session_state[STATE_PAGE] = min(total_pages, int(st.session_state[STATE_PAGE]) + 1)
            st.rerun()
    with n3:
        st.markdown(
            f'<div class="k-subtle" style="text-align:center;padding-top:0.55rem;">Page {int(st.session_state[STATE_PAGE])} of {total_pages}</div>',
            unsafe_allow_html=True,
        )
    with n4:
        jump = st.number_input(
            "Go to page",
            min_value=1,
            max_value=total_pages,
            value=int(st.session_state[STATE_PAGE]),
            step=1,
            key="app_jump",
        )
        if int(jump) != int(st.session_state[STATE_PAGE]):
            st.session_state[STATE_PAGE] = int(jump)
            st.rerun()
