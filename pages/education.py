from __future__ import annotations

import json
import re
import urllib.parse
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import streamlit as st

from pages.ui_kit import empty_state, render_hero


WHATSAPP_NUMBER = "+91-8555052189"
DATA_PATH = Path(__file__).resolve().parents[1] / "data" / "universities_top100.json"

BUDGET_OPTIONS = ["All", "Low", "Medium", "High"]
SCHOLARSHIP_OPTIONS = ["All", "Yes", "No"]
SORT_OPTIONS = ["QS Rank", "Name A-Z", "Fee: Low to High", "Fee: High to Low"]

FALLBACK_UNIVERSITIES: List[Dict[str, Any]] = [
    {
        "id": 1,
        "name": "University of Toronto",
        "country": "Canada",
        "city": "Toronto",
        "rank": 21,
        "scholarship": True,
        "fee_amount": 45000.0,
        "budget_tier": "High",
        "fee_structure": "Tuition: CAD 45,000/year | Living: CAD 16,000/year",
        "course_details": "Strong programs in Computer Science, Data Science, and Engineering.",
        "link": "https://www.utoronto.ca/",
    },
    {
        "id": 2,
        "name": "Technical University of Munich",
        "country": "Germany",
        "city": "Munich",
        "rank": 37,
        "scholarship": True,
        "fee_amount": 12000.0,
        "budget_tier": "Low",
        "fee_structure": "Semester contribution model | Living: EUR 12,000/year",
        "course_details": "Engineering and applied science tracks with strong industry collaboration.",
        "link": "https://www.tum.de/en/",
    },
    {
        "id": 3,
        "name": "University of Birmingham",
        "country": "UK",
        "city": "Birmingham",
        "rank": 84,
        "scholarship": True,
        "fee_amount": 25000.0,
        "budget_tier": "Medium",
        "fee_structure": "Tuition: GBP 25,000/year | Living: GBP 11,000/year",
        "course_details": "Postgraduate pathways in business, law, and life sciences.",
        "link": "https://www.birmingham.ac.uk/",
    },
]


def _wa_link(message: str) -> str:
    digits = "".join(ch for ch in WHATSAPP_NUMBER if ch.isdigit())
    if not digits:
        return ""
    return f"https://wa.me/{digits}?text={urllib.parse.quote(message)}"


def _parse_fee_amount(text: str) -> Optional[float]:
    if not text:
        return None

    normalized = text.lower().replace(",", "")
    short_match = re.search(r"(\d+(?:\.\d+)?)\s*([km])", normalized)
    if short_match:
        value = float(short_match.group(1))
        suffix = short_match.group(2)
        return value * (1000 if suffix == "k" else 1000000)

    full_match = re.search(r"(\d{3,7}(?:\.\d+)?)", normalized)
    if full_match:
        return float(full_match.group(1))

    return None


def _budget_tier_from_fee(fee_amount: Optional[float]) -> str:
    if fee_amount is None:
        return "Medium"
    if fee_amount < 20000:
        return "Low"
    if fee_amount <= 40000:
        return "Medium"
    return "High"


def _pick_first_non_empty(src: Dict[str, Any], keys: List[str], default: Any = "") -> Any:
    for key in keys:
        value = src.get(key)
        if value is not None and str(value).strip() != "":
            return value
    return default


def _to_bool(value: Any) -> bool:
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        return value.strip().lower() in {"yes", "true", "1", "y"}
    if isinstance(value, (int, float)):
        return bool(value)
    return False


def _normalize_university(raw: Dict[str, Any], idx: int) -> Dict[str, Any]:
    name = str(_pick_first_non_empty(raw, ["name", "university", "university_name"], "Unnamed University"))
    country = str(_pick_first_non_empty(raw, ["country", "nation"], "Unknown"))
    city = str(_pick_first_non_empty(raw, ["city", "location_city"], ""))

    rank_raw = _pick_first_non_empty(raw, ["rank", "qs_rank", "world_rank"], 9999)
    try:
        rank = int(str(rank_raw).replace("=", "").strip())
    except Exception:
        rank = 9999

    link = str(
        _pick_first_non_empty(
            raw,
            ["official_website", "website", "link", "university_link", "url", "qs_profile_url"],
            "",
        )
    )

    ug_fee = str(_pick_first_non_empty(raw, ["intl_ug_fee_range_local", "ug_fee", "tuition", "fee_structure"], ""))
    pg_fee = str(_pick_first_non_empty(raw, ["intl_pg_fee_range_local", "pg_fee"], ""))
    currency = str(_pick_first_non_empty(raw, ["currency"], "")).strip()

    if ug_fee and pg_fee:
        fee_structure = f"UG: {ug_fee} | PG: {pg_fee}"
    elif ug_fee:
        fee_structure = ug_fee
    elif pg_fee:
        fee_structure = pg_fee
    else:
        fee_structure = "Fee details available on university website"

    courses = raw.get("courses_offered") or raw.get("programs") or raw.get("courses") or []
    if isinstance(courses, list):
        course_details = ", ".join(str(item).strip() for item in courses if str(item).strip()[:1])
    else:
        course_details = str(courses).strip()

    if not course_details:
        course_details = "Course options vary by intake and department. Check official website for full catalog."

    scholarship = _to_bool(_pick_first_non_empty(raw, ["scholarship", "scholarship_available", "scholarship_offered"], False))
    fee_amount = _parse_fee_amount(f"{currency} {fee_structure}")

    return {
        "id": idx,
        "name": name,
        "country": country,
        "city": city,
        "rank": rank,
        "link": link,
        "fee_structure": fee_structure,
        "course_details": course_details,
        "scholarship": scholarship,
        "fee_amount": fee_amount,
        "budget_tier": _budget_tier_from_fee(fee_amount),
    }


def _load_universities() -> Tuple[List[Dict[str, Any]], Optional[str]]:
    if not DATA_PATH.exists():
        return FALLBACK_UNIVERSITIES[:], f"Data file missing at {DATA_PATH}. Showing fallback data."

    try:
        payload = json.loads(DATA_PATH.read_text(encoding="utf-8"))
    except Exception as exc:
        return FALLBACK_UNIVERSITIES[:], f"Could not parse {DATA_PATH}: {exc}. Showing fallback data."

    if not isinstance(payload, list):
        return FALLBACK_UNIVERSITIES[:], f"{DATA_PATH} must contain a JSON array. Showing fallback data."

    normalized = [_normalize_university(item, idx + 1) for idx, item in enumerate(payload) if isinstance(item, dict)]

    if not normalized:
        return FALLBACK_UNIVERSITIES[:], f"No valid university records found in {DATA_PATH}. Showing fallback data."

    return normalized, None


def _apply_filters(
    universities: List[Dict[str, Any]],
    search: str,
    country: str,
    budget: str,
    scholarship: str,
) -> List[Dict[str, Any]]:
    rows = universities[:]
    needle = search.strip().lower()

    if needle:
        rows = [
            uni
            for uni in rows
            if needle in str(uni.get("name", "")).lower()
            or needle in str(uni.get("country", "")).lower()
            or needle in str(uni.get("course_details", "")).lower()
        ]

    if country != "All":
        rows = [uni for uni in rows if str(uni.get("country", "")) == country]

    if budget != "All":
        rows = [uni for uni in rows if str(uni.get("budget_tier", "")) == budget]

    if scholarship == "Yes":
        rows = [uni for uni in rows if bool(uni.get("scholarship", False))]
    elif scholarship == "No":
        rows = [uni for uni in rows if not bool(uni.get("scholarship", False))]

    return rows


def _sort_universities(universities: List[Dict[str, Any]], sort_by: str) -> List[Dict[str, Any]]:
    rows = universities[:]

    if sort_by == "Name A-Z":
        rows.sort(key=lambda item: str(item.get("name", "")).lower())
        return rows

    if sort_by == "Fee: Low to High":
        rows.sort(key=lambda item: float(item.get("fee_amount") if item.get("fee_amount") is not None else 10**12))
        return rows

    if sort_by == "Fee: High to Low":
        rows.sort(key=lambda item: float(item.get("fee_amount") if item.get("fee_amount") is not None else -1), reverse=True)
        return rows

    rows.sort(key=lambda item: int(item.get("rank") if item.get("rank") is not None else 9999))
    return rows


def _paginate(rows: List[Dict[str, Any]], page: int, per_page: int) -> Tuple[List[Dict[str, Any]], int]:
    total_pages = max(1, (len(rows) + per_page - 1) // per_page)
    page = max(1, min(page, total_pages))
    start = (page - 1) * per_page
    end = start + per_page
    return rows[start:end], total_pages


def render() -> None:
    render_hero(
        kicker="Education Portal",
        title="Search global universities with clear tuition, course, and scholarship visibility.",
        subtitle=(
            "Use a structured search workflow: type a program or country, refine with budget and scholarship filters, "
            "then review university cards with direct links."
        ),
    )

    universities, warning_message = _load_universities()
    countries = ["All"] + sorted({str(u.get("country", "Unknown")) for u in universities if str(u.get("country", "")).strip()})

    st.markdown('<section class="k-section reveal">', unsafe_allow_html=True)
    st.markdown('<div class="k-filter-head">University Search</div>', unsafe_allow_html=True)

    c1, c2, c3, c4, c5, c6 = st.columns([1.8, 1.1, 1.0, 1.0, 1.2, 0.9])

    with c1:
        search = st.text_input(
            "Search",
            placeholder="University, course, or country",
            key="edu_search_query",
            label_visibility="collapsed",
        )

    with c2:
        country = st.selectbox("Country", options=countries, key="edu_country_filter", label_visibility="collapsed")

    with c3:
        budget = st.selectbox("Budget", options=BUDGET_OPTIONS, key="edu_budget_filter", label_visibility="collapsed")

    with c4:
        scholarship = st.selectbox(
            "Scholarship",
            options=SCHOLARSHIP_OPTIONS,
            key="edu_scholarship_filter",
            label_visibility="collapsed",
        )

    with c5:
        sort_by = st.selectbox("Sort", options=SORT_OPTIONS, key="edu_sort_filter", label_visibility="collapsed")

    with c6:
        per_page = st.selectbox("Page Size", options=[9, 18, 27], key="edu_page_size", label_visibility="collapsed")

    st.markdown('</section>', unsafe_allow_html=True)

    filtered_rows = _apply_filters(universities, search, country, budget, scholarship)
    sorted_rows = _sort_universities(filtered_rows, sort_by)

    if "edu_page" not in st.session_state:
        st.session_state.edu_page = 1

    page_rows, total_pages = _paginate(sorted_rows, int(st.session_state.edu_page), int(per_page))
    st.session_state.edu_page = max(1, min(int(st.session_state.edu_page), total_pages))

    st.markdown(
        f'<div class="k-result-count reveal"><strong>{len(sorted_rows)}</strong> universities matched your search.</div>',
        unsafe_allow_html=True,
    )

    if warning_message:
        st.warning(warning_message)

    if not page_rows:
        empty_state("No universities found", "Try broader search terms or reset your country and budget filters.")
        return

    for uni in page_rows:
        course_details = str(uni.get("course_details", "")).strip()
        if len(course_details) > 220:
            course_details = course_details[:220].rstrip() + "..."

        location = f"{uni.get('city', '').strip()}, {uni.get('country', '')}".strip(", ")
        scholarship_text = "Yes" if bool(uni.get("scholarship")) else "No"

        st.markdown(
            f"""
            <article class="k-uni-card reveal" id="uni_{uni['id']}">
                <h3 class="k-uni-title">#{int(uni.get('rank', 9999))} {uni.get('name', 'Unnamed University')}</h3>
                <div class="k-uni-meta">
                    <span>{location}</span>
                    <span>Budget: {uni.get('budget_tier', _budget_tier_from_fee(uni.get('fee_amount')))}</span>
                    <span>Scholarship: {scholarship_text}</span>
                </div>
                <div class="k-fee">{uni.get('fee_structure', 'Fee details on university website')}</div>
                <p class="k-course">{course_details}</p>
            </article>
            """,
            unsafe_allow_html=True,
        )

        a1, a2 = st.columns(2)
        with a1:
            if str(uni.get("link", "")).strip():
                st.link_button("University Website", str(uni.get("link")), use_container_width=True, key=f"uni_link_{uni['id']}")
            else:
                st.button("University Website", disabled=True, use_container_width=True, key=f"uni_link_missing_{uni['id']}")

        with a2:
            message = (
                f"Hello Kansalt, I want guidance for {uni.get('name')} in {uni.get('country')}. "
                "Please share admission steps, requirements, and timelines."
            )
            wa_url = _wa_link(message)
            if wa_url:
                st.link_button("Submit Application", wa_url, use_container_width=True, key=f"uni_apply_{uni['id']}")
            else:
                st.button("Submit Application", disabled=True, use_container_width=True, key=f"uni_apply_disabled_{uni['id']}")

    p1, p2, p3 = st.columns([1, 1, 1.8])
    with p1:
        if st.button(
            "Previous",
            use_container_width=True,
            disabled=st.session_state.edu_page <= 1,
            key="edu_prev_page",
        ):
            st.session_state.edu_page -= 1
            st.rerun()

    with p2:
        if st.button(
            "Next",
            use_container_width=True,
            disabled=st.session_state.edu_page >= total_pages,
            key="edu_next_page",
        ):
            st.session_state.edu_page += 1
            st.rerun()

    with p3:
        page_value = st.number_input(
            "Go to page",
            min_value=1,
            max_value=total_pages,
            value=int(st.session_state.edu_page),
            step=1,
            key="edu_page_input",
        )
        if int(page_value) != int(st.session_state.edu_page):
            st.session_state.edu_page = int(page_value)
            st.rerun()
