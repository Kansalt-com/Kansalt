"""
Business page - launch stage positioning (no inflated metrics/dummy growth data)
"""

import os
import urllib.parse

import streamlit as st


WHATSAPP_NUMBER = os.getenv("WHATSAPP_NUMBER", "")

SERVICE_AREAS = [
    {
        "id": "talent",
        "title": "Talent Sourcing",
        "description": "Role-specific candidate pipelines for startups and growing teams.",
        "highlights": ["Tech and non-tech roles", "Screened candidate profiles", "Fast shortlist delivery"],
    },
    {
        "id": "hiring",
        "title": "Hiring Support",
        "description": "Interview coordination and offer-stage support to reduce hiring friction.",
        "highlights": ["Interview scheduling", "Candidate communication", "Offer follow-up"],
    },
    {
        "id": "branding",
        "title": "Employer Branding",
        "description": "Foundational employer branding support for early-stage market visibility.",
        "highlights": ["Job post optimization", "Career page guidance", "Candidate-facing messaging"],
    },
    {
        "id": "custom",
        "title": "Custom Engagement",
        "description": "Flexible collaboration model built around your current hiring stage.",
        "highlights": ["Discovery call", "Scope-based engagement", "Milestone reporting"],
    },
]


def _wa_link(message: str) -> str:
    digits = "".join(ch for ch in WHATSAPP_NUMBER if ch.isdigit())
    if not digits:
        return ""
    return f"https://wa.me/{digits}?text={urllib.parse.quote(message)}"


def render() -> None:
    st.markdown('<section class="premium-hero">', unsafe_allow_html=True)
    st.markdown('<div class="hero-kicker">Business</div>', unsafe_allow_html=True)
    st.markdown('<h1 class="hero-title">Business Hiring Solutions</h1>', unsafe_allow_html=True)
    st.markdown(
        '<p class="hero-sub">We are a new market entrant focused on practical hiring support, transparent communication, and execution speed.</p>',
        unsafe_allow_html=True,
    )
    st.markdown('</section>', unsafe_allow_html=True)

    st.markdown('<div class="section-shell">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">What We Offer Right Now</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-subtitle">Built for teams that want lean, outcome-focused recruitment support.</div>', unsafe_allow_html=True)

    for item in SERVICE_AREAS:
        st.markdown('<article class="premium-card business-card">', unsafe_allow_html=True)
        st.markdown(f'<h3 class="result-title">{item["title"]}</h3>', unsafe_allow_html=True)
        st.markdown(f'<p class="result-description">{item["description"]}</p>', unsafe_allow_html=True)

        bullets_html = "".join([f"<li>{h}</li>" for h in item["highlights"]])
        st.markdown(f'<ul class="feature-list">{bullets_html}</ul>', unsafe_allow_html=True)

        cols = st.columns([1.2, 1])
        with cols[0]:
            st.markdown('<div class="new-market-note">Launch-stage service. Scope and pricing shared after requirement discussion.</div>', unsafe_allow_html=True)
        with cols[1]:
            msg = f"Hello Kunsalt, I want to discuss {item['title']} for my company."
            wa = _wa_link(msg)
            if wa:
                st.link_button("Talk on WhatsApp", wa, use_container_width=True)
            else:
                st.button("Talk on WhatsApp", disabled=True, use_container_width=True, key=f"wa_disabled_{item['id']}")

        st.markdown('</article>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="section-shell">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Contact</div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<div class="premium-card compact-card"><div class="result-title">Email</div><div class="result-description">sales@kunsalt.com</div></div>', unsafe_allow_html=True)
    with col2:
        if WHATSAPP_NUMBER:
            wa_contact = _wa_link("Hello Kunsalt, I would like to discuss business hiring requirements.")
            st.markdown('<div class="premium-card compact-card">', unsafe_allow_html=True)
            st.markdown('<div class="result-title">WhatsApp</div>', unsafe_allow_html=True)
            st.link_button("Start Conversation", wa_contact, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="premium-card compact-card"><div class="result-title">WhatsApp</div><div class="result-description">Set WHATSAPP_NUMBER env var to enable direct messaging CTA.</div></div>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)
