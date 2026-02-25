from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Dict

import streamlit as st
import streamlit.components.v1 as components

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

st.set_page_config(
    page_title="Kansalt | Global Consulting + Technology",
    page_icon="K",
    layout="wide",
    initial_sidebar_state="collapsed",
)

from pages.business import render as render_business
from pages.education import render as render_education
from pages.home import render as render_home
from pages.jobs import render as render_jobs
from pages.ui_kit import route_url


TAB_RENDERERS = {
    "Home": render_home,
    "Education": render_education,
    "Jobs": render_jobs,
    "Business": render_business,
}

TAB_TITLES: Dict[str, str] = {
    "Home": "Kansalt | Premium Consulting Platform",
    "Education": "Kansalt Education | Global University Discovery",
    "Jobs": "Kansalt Jobs | Smart Job Aggregator Dashboard",
    "Business": "Kansalt Business | App Store and Technology Advisory",
}

TAB_DESCRIPTIONS: Dict[str, str] = {
    "Home": "Kansalt is a global consulting and technology platform connecting education, jobs, and business growth workflows.",
    "Education": "Search universities by rank, budget, and scholarship to plan your study abroad strategy.",
    "Jobs": "Find role-matched opportunities through a clean card-based dashboard with skills, location, and date filters.",
    "Business": "Explore business solutions and an app-store style catalog with admin-managed application onboarding.",
}


def _load_global_css() -> None:
    css_path = ROOT / "public" / "styles.css"
    if css_path.exists():
        st.markdown(f"<style>{css_path.read_text(encoding='utf-8')}</style>", unsafe_allow_html=True)


def _query_value(name: str, default: str = "") -> str:
    value = st.query_params.get(name, default)
    if isinstance(value, list):
        return str(value[0]) if value else default
    return str(value)


def _normalize_tab(raw: str) -> str:
    candidate = (raw or "").strip().title()
    if candidate not in TAB_RENDERERS:
        return "Home"
    return candidate


def _render_navbar(active_tab: str) -> None:
    menu = [
        ("Home", route_url("Home")),
        ("Education", route_url("Education")),
        ("Jobs", route_url("Jobs")),
        ("Business", route_url("Business")),
        ("About", route_url("Home", "about")),
        ("Contact", route_url("Home", "contact")),
    ]

    links = []
    for label, href in menu:
        active = " class=\"is-active\"" if (label == active_tab and label in TAB_RENDERERS) else ""
        links.append(f'<a{active} href="{href}">{label}</a>')

    st.markdown(
        f"""
        <nav id="k-navbar">
            <div class="k-nav-inner">
                <a class="k-nav-brand" href="{route_url('Home')}">K<span>ansalt</span></a>
                <div class="k-nav-menu">{''.join(links)}</div>
                <a class="k-nav-cta" href="{route_url('Business')}">Get Started</a>
            </div>
        </nav>
        <div class="k-nav-spacer"></div>
        """,
        unsafe_allow_html=True,
    )


def _inject_runtime_scripts(selected_tab: str, section_target: str) -> None:
    page_title = TAB_TITLES.get(selected_tab, TAB_TITLES["Home"])
    page_description = TAB_DESCRIPTIONS.get(selected_tab, TAB_DESCRIPTIONS["Home"])

    script = f"""
    <script>
    (() => {{
      const rootWin = window.parent;
      const doc = rootWin.document;

      function upsertMeta(selector, attrs) {{
        let node = doc.head.querySelector(selector);
        if (!node) {{
          node = doc.createElement('meta');
          doc.head.appendChild(node);
        }}
        Object.keys(attrs).forEach((key) => node.setAttribute(key, attrs[key]));
      }}

      doc.title = {json.dumps(page_title)};
      upsertMeta('meta[name="description"]', {{ name: 'description', content: {json.dumps(page_description)} }});
      upsertMeta('meta[property="og:title"]', {{ property: 'og:title', content: {json.dumps(page_title)} }});
      upsertMeta('meta[property="og:description"]', {{ property: 'og:description', content: {json.dumps(page_description)} }});
      upsertMeta('meta[name="twitter:card"]', {{ name: 'twitter:card', content: 'summary_large_image' }});

      const nav = doc.getElementById('k-navbar');
      function refreshNav() {{
        if (!nav) return;
        if (rootWin.scrollY > 8) nav.classList.add('is-scrolled');
        else nav.classList.remove('is-scrolled');
      }}

      if (!rootWin.__kansaltScrollBound) {{
        rootWin.addEventListener('scroll', refreshNav, {{ passive: true }});
        rootWin.__kansaltScrollBound = true;
      }}
      refreshNav();

      if (!rootWin.__kansaltRevealObserver) {{
        rootWin.__kansaltRevealObserver = new rootWin.IntersectionObserver((entries) => {{
          entries.forEach((entry) => {{
            if (entry.isIntersecting) {{
              entry.target.classList.add('in-view');
            }}
          }});
        }}, {{ threshold: 0.14, rootMargin: '0px 0px -8% 0px' }});
      }}

      const observer = rootWin.__kansaltRevealObserver;
      const prefersReduced = rootWin.matchMedia('(prefers-reduced-motion: reduce)').matches;
      doc.querySelectorAll('.reveal').forEach((el) => {{
        if (prefersReduced) el.classList.add('in-view');
        observer.observe(el);
      }});

      const targetId = {json.dumps(section_target)};
      if (targetId) {{
        rootWin.setTimeout(() => {{
          const node = doc.getElementById(targetId);
          if (node) {{
            node.scrollIntoView({{ behavior: 'smooth', block: 'start' }});
          }}
        }}, 120);
      }}
    }})();
    </script>
    """

    components.html(script, height=0, width=0)


_load_global_css()

selected_tab = _normalize_tab(_query_value("tab", "Home"))
section = _query_value("section", "").strip().lower()
if section and selected_tab != "Home":
    section = ""

st.session_state.selected_tab = selected_tab

_render_navbar(selected_tab)

TAB_RENDERERS[selected_tab]()

_inject_runtime_scripts(selected_tab, section)

st.markdown(
    """
    <div class="k-subtle" style="text-align:center;margin-top:2.2rem;">
      Kansalt Platform | Education | Jobs | Business Technology
    </div>
    """,
    unsafe_allow_html=True,
)
