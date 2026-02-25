from __future__ import annotations

import html
import urllib.parse
from typing import Iterable, Optional

import streamlit as st


def route_url(tab: str, section: Optional[str] = None) -> str:
    params = [("tab", tab)]
    if section:
        params.append(("section", section))
    return "?" + urllib.parse.urlencode(params)


def _render_buttons(buttons: Iterable[dict]) -> str:
    chunks = []
    for button in buttons:
        label = html.escape(str(button.get("label", "Open")))
        href = html.escape(str(button.get("href", "#")), quote=True)
        style = str(button.get("style", "primary"))
        class_name = "k-btn" if style == "primary" else "k-btn k-btn-ghost"
        target = " target=\"_blank\" rel=\"noopener\"" if bool(button.get("external", False)) else ""
        chunks.append(f'<a class="{class_name}" href="{href}"{target}>{label}</a>')
    return "".join(chunks)


def render_hero(
    *,
    kicker: str,
    title: str,
    subtitle: str,
    buttons: Optional[Iterable[dict]] = None,
    section_id: Optional[str] = None,
) -> None:
    sid = f' id="{html.escape(section_id, quote=True)}"' if section_id else ""
    buttons_html = _render_buttons(buttons or [])
    cta_html = f'<div class="k-hero-cta">{buttons_html}</div>' if buttons_html else ""

    st.markdown(
        f"""
        <section{sid} class="k-hero reveal">
            <div class="k-eyebrow">{html.escape(kicker)}</div>
            <h1>{html.escape(title)}</h1>
            <p>{html.escape(subtitle)}</p>
            {cta_html}
        </section>
        """,
        unsafe_allow_html=True,
    )


def section_open(*, title: str, subtitle: str, kicker: str = "", section_id: Optional[str] = None, alt: bool = False) -> None:
    sid = f' id="{html.escape(section_id, quote=True)}"' if section_id else ""
    alt_class = " alt" if alt else ""
    kicker_html = f'<div class="k-eyebrow">{html.escape(kicker)}</div>' if kicker else ""
    st.markdown(
        f"""
        <section{sid} class="k-section{alt_class} reveal">
            {kicker_html}
            <h2>{html.escape(title)}</h2>
            <p class="k-section-sub">{html.escape(subtitle)}</p>
        """,
        unsafe_allow_html=True,
    )


def section_close() -> None:
    st.markdown("</section>", unsafe_allow_html=True)


def metric_strip(items: list[tuple[str, str]]) -> None:
    chips = "".join(
        f'<article class="k-metric"><div class="k-metric-value">{html.escape(value)}</div><div class="k-metric-label">{html.escape(label)}</div></article>'
        for value, label in items
    )
    st.markdown(f'<div class="k-metric-grid reveal">{chips}</div>', unsafe_allow_html=True)


def empty_state(title: str, message: str) -> None:
    st.markdown(
        f"""
        <div class="k-empty reveal">
            <h3>{html.escape(title)}</h3>
            <p>{html.escape(message)}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
