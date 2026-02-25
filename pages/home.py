from __future__ import annotations

import streamlit as st

from pages.ui_kit import metric_strip, render_hero, route_url, section_close, section_open


def render() -> None:
    render_hero(
        kicker="Global Consulting + Technology",
        title="Scale education access, talent pipelines, and business systems from one platform.",
        subtitle=(
            "Kansalt combines advisory depth with productized execution. Discover universities, "
            "find high-fit opportunities, and launch business applications with a premium, simple workflow."
        ),
        buttons=[
            {"label": "Explore Services", "href": route_url("Home", "services"), "style": "primary"},
            {"label": "Get Started", "href": route_url("Business"), "style": "secondary"},
        ],
    )

    section_open(
        kicker="Core Services",
        title="Three delivery pillars built for outcomes",
        subtitle="Each module follows the same principle: clear structure, fast execution, and measurable progress.",
        section_id="services",
    )

    st.markdown(
        f"""
        <div class="k-services-grid">
            <article class="k-service-card reveal reveal-delay-1">
                <div class="k-service-icon">E</div>
                <h3>Education Portal</h3>
                <p>Search top universities with structured filters for budget, scholarship, rank, and course fit.</p>
                <a class="k-link" href="{route_url('Education')}">Open Education Portal</a>
            </article>
            <article class="k-service-card reveal reveal-delay-2">
                <div class="k-service-icon">J</div>
                <h3>Job Aggregator</h3>
                <p>Use a card-based job dashboard with skill matching, location filters, and direct apply pathways.</p>
                <a class="k-link" href="{route_url('Jobs')}">Open Jobs Dashboard</a>
            </article>
            <article class="k-service-card reveal reveal-delay-3">
                <div class="k-service-icon">B</div>
                <h3>Business App Store</h3>
                <p>Browse deployable applications and manage app onboarding from an integrated admin control panel.</p>
                <a class="k-link" href="{route_url('Business')}">Open Business App Store</a>
            </article>
        </div>
        """,
        unsafe_allow_html=True,
    )

    metric_strip(
        [
            ("100+", "Global universities indexed"),
            ("30+", "Job sources aggregated"),
            ("24/7", "Digital platform availability"),
            ("1", "Unified operating workspace"),
        ]
    )
    section_close()

    section_open(
        kicker="About",
        title="Built for founders, students, and growth teams",
        subtitle=(
            "Kansalt follows a consulting-grade UX system: high readability, premium whitespace, and low-friction calls to action."
        ),
        section_id="about",
        alt=True,
    )

    st.markdown(
        """
        <div class="k-two-col">
            <article class="k-card reveal reveal-delay-1">
                <h3 class="k-job-title">What makes this platform different</h3>
                <p class="k-job-desc">
                    The experience is intentionally uncluttered. Every screen prioritizes decision quality,
                    not visual noise. Inputs are concise, cards are scannable, and every CTA maps to a next action.
                </p>
                <ul class="k-contact-list">
                    <li>Consulting-grade information hierarchy</li>
                    <li>Card-first UX for quick decision cycles</li>
                    <li>Consistent system across education, jobs, and business workflows</li>
                </ul>
            </article>
            <article class="k-card reveal reveal-delay-2">
                <h3 class="k-job-title">Execution principles</h3>
                <p class="k-job-desc">
                    The platform is designed mobile-first with responsive modules, optimized render behavior,
                    and subtle motion that supports context instead of distracting from it.
                </p>
                <div class="k-top-note">
                    Minimal motion, strong typography, and section-based layout transitions create a premium consulting feel.
                </div>
            </article>
        </div>
        """,
        unsafe_allow_html=True,
    )
    section_close()

    section_open(
        kicker="Contact",
        title="Start your next program with Kansalt",
        subtitle="Choose your pathway and connect with the team for onboarding.",
        section_id="contact",
    )

    st.markdown(
        f"""
        <div class="k-two-col">
            <article class="k-card reveal reveal-delay-1">
                <h3 class="k-job-title">Direct contact channels</h3>
                <ul class="k-contact-list">
                    <li>Email: support@kansalt.com</li>
                    <li>WhatsApp: +91-8555052189</li>
                    <li>Coverage: Education, Hiring, Business Technology</li>
                </ul>
            </article>
            <article class="k-card reveal reveal-delay-2">
                <h3 class="k-job-title">Quick actions</h3>
                <div class="k-hero-cta" style="margin-top:0.8rem;">
                    <a class="k-btn" href="{route_url('Education')}">Plan Study Route</a>
                    <a class="k-btn k-btn-ghost" href="{route_url('Jobs')}">Find Jobs</a>
                    <a class="k-btn k-btn-ghost" href="{route_url('Business')}">Launch Business Apps</a>
                </div>
            </article>
        </div>
        """,
        unsafe_allow_html=True,
    )
    section_close()
