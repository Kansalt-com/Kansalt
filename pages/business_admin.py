"""
Business App Store admin authentication and management UI.
"""

from __future__ import annotations

from typing import Any, Dict, List

import streamlit as st

from services.appstore_service import AppStoreService, DEFAULT_CATEGORIES


SESSION_ADMIN_AUTH = "business_admin_authenticated"
SESSION_ADMIN_USER = "business_admin_username"


def is_admin_authenticated() -> bool:
    return bool(st.session_state.get(SESSION_ADMIN_AUTH, False))


def _set_admin_session(username: str) -> None:
    st.session_state[SESSION_ADMIN_AUTH] = True
    st.session_state[SESSION_ADMIN_USER] = username


def _clear_admin_session() -> None:
    st.session_state[SESSION_ADMIN_AUTH] = False
    st.session_state[SESSION_ADMIN_USER] = None


def render_admin_access(service: AppStoreService) -> None:
    """
    Render admin initialize/login/logout controls outside admin panel.
    This lets admin users authenticate even when Admin tab is hidden.
    """
    has_admin = service.has_admin_users()
    with st.expander("Admin Access", expanded=not has_admin):
        st.markdown('<div class="section-shell">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">Admin Access</div>', unsafe_allow_html=True)

        if is_admin_authenticated():
            user = str(st.session_state.get(SESSION_ADMIN_USER, "admin"))
            c1, c2 = st.columns([3, 1])
            with c1:
                st.markdown(
                    f'<div class="section-subtitle">Signed in as <strong>{user}</strong>.</div>',
                    unsafe_allow_html=True,
                )
            with c2:
                if st.button("Logout", use_container_width=True, key="business_admin_logout_access"):
                    _clear_admin_session()
                    st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)
            return

        if not has_admin:
            st.markdown(
                '<div class="section-subtitle">No admin account exists yet. Initialize the first admin.</div>',
                unsafe_allow_html=True,
            )
            with st.form("business_admin_init_form", clear_on_submit=True):
                username = st.text_input("Admin username", placeholder="Choose admin username")
                password = st.text_input("Admin password", type="password", placeholder="At least 8 characters")
                confirm = st.text_input("Confirm password", type="password")
                submitted = st.form_submit_button("Initialize Admin", use_container_width=True)

            if submitted:
                if password != confirm:
                    st.error("Passwords do not match.")
                else:
                    ok, msg = service.create_initial_admin(username=username, password=password)
                    if ok:
                        _set_admin_session(username.strip())
                        st.success(msg)
                        st.rerun()
                    else:
                        st.error(msg)
        else:
            st.markdown(
                '<div class="section-subtitle">Sign in to access App Store administration.</div>',
                unsafe_allow_html=True,
            )
            with st.form("business_admin_login_form", clear_on_submit=True):
                username = st.text_input("Admin username", placeholder="Enter username")
                password = st.text_input("Admin password", type="password", placeholder="Enter password")
                submitted = st.form_submit_button("Login", use_container_width=True)

            if submitted:
                if service.verify_admin(username=username, password=password):
                    _set_admin_session(username.strip())
                    st.success("Admin login successful.")
                    st.rerun()
                else:
                    st.error("Invalid admin credentials.")

        st.markdown('</div>', unsafe_allow_html=True)


def _parse_csv(raw: str) -> List[str]:
    return [part.strip() for part in raw.split(",") if part.strip()]


def _render_add_app_panel(service: AppStoreService) -> None:
    st.markdown("### Add New App")

    with st.form("business_admin_add_app_form", clear_on_submit=False):
        c1, c2, c3 = st.columns([1.5, 1.0, 0.8])
        with c1:
            name = st.text_input("App Name", placeholder="Example: SIMS Hospital Suite")
        with c2:
            category = st.selectbox("Category", options=DEFAULT_CATEGORIES, index=0)
        with c3:
            version = st.text_input("Version", value="1.0.0")

        short_desc = st.text_area("Short Description", height=80)
        full_desc = st.text_area("Full Description", height=130)

        c4, c5 = st.columns([1.4, 1.2])
        with c4:
            tags_csv = st.text_input("Tags (comma-separated)", placeholder="analytics, dashboard, ai")
        with c5:
            os_support = st.multiselect(
                "OS Support",
                options=["Windows", "Linux", "macOS", "Web"],
                default=["Windows", "Linux", "Web"],
            )

        setup_instructions = st.text_area("Setup / Run Instructions", height=110)
        changelog = st.text_area("Changelog", height=90)
        is_active = st.checkbox("Visible in App Store", value=True)

        source_mode = st.radio(
            "Package Source",
            options=["Upload ZIP", "Add Local Folder Path"],
            horizontal=True,
        )
        uploaded_zip = None
        folder_path = ""
        if source_mode == "Upload ZIP":
            uploaded_zip = st.file_uploader("Upload ZIP", type=["zip"], accept_multiple_files=False)
        else:
            folder_path = st.text_input(
                "Local Project Folder Path",
                placeholder=r"Example: D:\projects\my_app",
            )

        submitted = st.form_submit_button("Add / Update App", use_container_width=True)

    if not submitted:
        return

    metadata = {
        "name": name,
        "category": category,
        "short_desc": short_desc,
        "full_desc": full_desc,
        "version": version,
        "tags": _parse_csv(tags_csv),
        "os_support": os_support,
        "setup_instructions": setup_instructions,
        "changelog": changelog,
        "is_active": is_active,
    }

    if source_mode == "Upload ZIP":
        if uploaded_zip is None:
            st.error("Please upload a ZIP file.")
            return
        ok, msg, _ = service.add_or_update_app_from_uploaded_zip(
            metadata=metadata,
            zip_bytes=uploaded_zip.getvalue(),
        )
    else:
        if not folder_path.strip():
            st.error("Please provide a local folder path.")
            return
        ok, msg, _ = service.add_or_update_app_from_folder(
            metadata=metadata,
            folder_path=folder_path,
        )

    if ok:
        st.success(msg)
        st.rerun()
    else:
        st.error(msg)


def _render_manage_apps_panel(service: AppStoreService) -> None:
    st.markdown("### Manage Apps")
    apps = service.list_admin_apps()
    if not apps:
        st.info("No apps available yet.")
        return

    app_by_id = {int(app["id"]): app for app in apps}
    app_ids = list(app_by_id.keys())

    selected_id = st.selectbox(
        "Select app",
        options=app_ids,
        format_func=lambda app_id: (
            f"{app_by_id[app_id]['name']} "
            f"(v{app_by_id[app_id]['version']}) - "
            f"{'Active' if app_by_id[app_id]['is_active'] else 'Disabled'}"
        ),
        key="business_admin_selected_app",
    )
    app = app_by_id[int(selected_id)]
    app_id = int(app["id"])

    st.markdown(
        f'<div class="section-subtitle">Downloads: <strong>{int(app.get("downloads", 0))}</strong></div>',
        unsafe_allow_html=True,
    )

    name = st.text_input("Name", value=str(app.get("name", "")), key=f"admin_name_{app_id}")
    category = st.selectbox(
        "Category",
        options=DEFAULT_CATEGORIES,
        index=max(0, DEFAULT_CATEGORIES.index(app.get("category", "Other")) if app.get("category", "Other") in DEFAULT_CATEGORIES else 0),
        key=f"admin_category_{app_id}",
    )
    version = st.text_input("Version", value=str(app.get("version", "1.0.0")), key=f"admin_version_{app_id}")
    short_desc = st.text_area(
        "Short Description",
        value=str(app.get("short_desc", "")),
        height=80,
        key=f"admin_short_desc_{app_id}",
    )
    full_desc = st.text_area(
        "Full Description",
        value=str(app.get("full_desc", "")),
        height=120,
        key=f"admin_full_desc_{app_id}",
    )
    tags_csv = st.text_input(
        "Tags (comma-separated)",
        value=", ".join(app.get("tags", [])),
        key=f"admin_tags_{app_id}",
    )
    os_support = st.multiselect(
        "OS Support",
        options=["Windows", "Linux", "macOS", "Web"],
        default=app.get("os_support", []),
        key=f"admin_os_{app_id}",
    )
    setup_instructions = st.text_area(
        "Setup / Run Instructions",
        value=str(app.get("setup_instructions", "")),
        height=110,
        key=f"admin_setup_{app_id}",
    )
    changelog = st.text_area(
        "Changelog",
        value=str(app.get("changelog", "")),
        height=90,
        key=f"admin_changelog_{app_id}",
    )
    active_flag = st.checkbox(
        "Visible in App Store",
        value=bool(app.get("is_active", True)),
        key=f"admin_visible_{app_id}",
    )

    if st.button("Save Metadata", use_container_width=True, key=f"admin_save_{app_id}"):
        payload: Dict[str, Any] = {
            "name": name,
            "category": category,
            "version": version,
            "short_desc": short_desc,
            "full_desc": full_desc,
            "tags": _parse_csv(tags_csv),
            "os_support": os_support,
            "setup_instructions": setup_instructions,
            "changelog": changelog,
            "is_active": active_flag,
        }
        ok, msg = service.update_app_metadata(app_id, payload)
        if ok:
            st.success(msg)
            st.rerun()
        else:
            st.error(msg)

    c1, c2, c3 = st.columns([1, 1, 2])
    with c1:
        toggle_label = "Disable App" if bool(app.get("is_active")) else "Enable App"
        if st.button(toggle_label, use_container_width=True, key=f"admin_toggle_{app_id}"):
            ok, msg = service.set_app_active(app_id, not bool(app.get("is_active")))
            if ok:
                st.success(msg)
                st.rerun()
            else:
                st.error(msg)
    with c2:
        confirm = st.checkbox("Confirm Delete", key=f"admin_confirm_delete_{app_id}")
    with c3:
        if st.button(
            "Delete App",
            use_container_width=True,
            disabled=not confirm,
            key=f"admin_delete_{app_id}",
        ):
            ok, msg = service.delete_app(app_id)
            if ok:
                st.success(msg)
                st.rerun()
            else:
                st.error(msg)


def _render_stats_panel(service: AppStoreService) -> None:
    st.markdown("### Download Stats")
    rows = service.list_download_stats()
    if not rows:
        st.info("No download stats available.")
        return

    table_rows = [
        {
            "App": row.get("name"),
            "Category": row.get("category"),
            "Version": row.get("version"),
            "Downloads": int(row.get("downloads", 0) or 0),
            "Status": "Active" if int(row.get("is_active", 0) or 0) == 1 else "Disabled",
            "Updated": row.get("updated_at"),
        }
        for row in rows
    ]
    st.dataframe(table_rows, hide_index=True, use_container_width=True)


def render_admin_panel(service: AppStoreService) -> None:
    if not is_admin_authenticated():
        st.info("Admin authentication required.")
        return

    username = str(st.session_state.get(SESSION_ADMIN_USER, "admin"))

    c1, c2 = st.columns([3, 1])
    with c1:
        st.markdown(
            f"""
            <section class="premium-hero">
                <div class="hero-kicker">Business Admin</div>
                <h1 class="hero-title">App Store Control Panel</h1>
                <p class="hero-sub">Signed in as <strong>{username}</strong>. Manage packages, metadata, visibility, and analytics.</p>
            </section>
            """,
            unsafe_allow_html=True,
        )
    with c2:
        if st.button("Logout Admin", use_container_width=True, key="business_admin_logout_panel"):
            _clear_admin_session()
            st.rerun()

    tab_add, tab_manage, tab_stats = st.tabs(["Add New App", "Manage Apps", "Download Stats"])
    with tab_add:
        _render_add_app_panel(service)
    with tab_manage:
        _render_manage_apps_panel(service)
    with tab_stats:
        _render_stats_panel(service)
