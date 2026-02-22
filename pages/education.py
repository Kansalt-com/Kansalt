"""
Education page with JSON-backed university listings, filters, sorting, and pagination.
"""

from __future__ import annotations

import json
import re
import urllib.parse
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import streamlit as st


WHATSAPP_NUMBER = "+91-8555052189"
DATA_PATH = Path(__file__).resolve().parents[1] / "data" / "universities_top100.json"

COUNTRIES = ["All"]
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
        "course_details": "Strong programs in Computer Science, Data Science, and Engineering with co-op opportunities.",
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
        "fee_structure": "Minimal tuition/semester contribution | Living: EUR 12,000/year",
        "course_details": "Well known for engineering and applied sciences; strong research and industry collaboration.",
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
        "course_details": "Offers strong postgraduate pathways in Business, Law, and life sciences.",
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

    s = text.lower().replace(",", "")
    m = re.search(r"(\d+(?:\.\d+)?)\s*([kKmM])", s)
    if m:
        value = float(m.group(1))
        scale = m.group(2).lower()
        return value * (1000 if scale == "k" else 1000000)

    m2 = re.search(r"(\d{3,7}(?:\.\d+)?)", s)
    if m2:
        return float(m2.group(1))

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
        val = src.get(key)
        if val is not None and str(val).strip() != "":
            return val
    return default


def _to_bool(val: Any) -> bool:
    if isinstance(val, bool):
        return val
    if isinstance(val, str):
        return val.strip().lower() in {"yes", "true", "1", "y"}
    if isinstance(val, (int, float)):
        return bool(val)
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
        course_details = ", ".join([str(c).strip() for c in courses if str(c).strip()][:5])
    else:
        course_details = str(courses).strip()
    if not course_details:
        course_details = "Course options vary by intake and department. Check university link for full catalog."

    scholarship = _to_bool(
        _pick_first_non_empty(raw, ["scholarship", "scholarship_available", "scholarship_offered"], False)
    )

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
        return FALLBACK_UNIVERSITIES[:], f"Data file not found at {DATA_PATH}. Showing fallback list."

    try:
        payload = json.loads(DATA_PATH.read_text(encoding="utf-8"))
    except Exception as exc:
        return FALLBACK_UNIVERSITIES[:], (
            f"Could not parse {DATA_PATH}. Ensure it is valid JSON array. Error: {exc}. Showing fallback list."
        )

    if not isinstance(payload, list):
        return FALLBACK_UNIVERSITIES[:], f"{DATA_PATH} must be a JSON array. Showing fallback list."

    normalized = [_normalize_university(item, idx + 1) for idx, item in enumerate(payload) if isinstance(item, dict)]

    if not normalized:
        return FALLBACK_UNIVERSITIES[:], f"No valid university objects in {DATA_PATH}. Showing fallback list."

    return normalized, None


def _apply_filters(
    universities: List[Dict[str, Any]],
    search: str,
    country: str,
    budget: str,
    scholarship: str,
) -> List[Dict[str, Any]]:
    filtered = universities[:]

    s = search.strip().lower()
    if s:
        filtered = [
            u
            for u in filtered
            if s in str(u.get("name", "")).lower()
            or s in str(u.get("country", "")).lower()
            or s in str(u.get("course_details", "")).lower()
        ]

    if country != "All":
        filtered = [u for u in filtered if u.get("country") == country]

    if budget != "All":
        filtered = [u for u in filtered if u.get("budget_tier") == budget]

    if scholarship == "Yes":
        filtered = [u for u in filtered if bool(u.get("scholarship"))]
    elif scholarship == "No":
        filtered = [u for u in filtered if not bool(u.get("scholarship"))]

    return filtered


def _sort_universities(universities: List[Dict[str, Any]], sort_by: str) -> List[Dict[str, Any]]:
    rows = universities[:]

    if sort_by == "Name A-Z":
        rows.sort(key=lambda x: str(x.get("name", "")).lower())
        return rows

    if sort_by == "Fee: Low to High":
        rows.sort(key=lambda x: float(x.get("fee_amount") if x.get("fee_amount") is not None else 1e12))
        return rows

    if sort_by == "Fee: High to Low":
        rows.sort(key=lambda x: float(x.get("fee_amount") if x.get("fee_amount") is not None else -1), reverse=True)
        return rows

    rows.sort(key=lambda x: int(x.get("rank") if x.get("rank") is not None else 9999))
    return rows


def _paginate(rows: List[Dict[str, Any]], page: int, per_page: int) -> Tuple[List[Dict[str, Any]], int]:
    total = len(rows)
    total_pages = max(1, (total + per_page - 1) // per_page)
    page = max(1, min(page, total_pages))
    start = (page - 1) * per_page
    end = start + per_page
    return rows[start:end], total_pages


def render() -> None:
    st.markdown(
        """
        <section class="premium-hero">
            <div class="hero-kicker">Education</div>
            <h1 class="hero-title">Study Abroad Search</h1>
            <p class="hero-sub">Search by budget, destination country, scholarship, then sort and paginate results.</p>
        </section>
        """,
        unsafe_allow_html=True,
    )

    universities, warning_msg = _load_universities()

    countries = ["All"] + sorted({str(u.get("country", "Unknown")) for u in universities if str(u.get("country", "")).strip()})

    f1, f2, f3, f4, f5, f6 = st.columns([1.6, 1.1, 1.0, 1.0, 1.2, 0.8])

    with f1:
        search = st.text_input(
            "Search colleges/universities",
            placeholder="Search by university, country, or course",
            label_visibility="collapsed",
            key="edu_search_query",
        )

    with f2:
        country = st.selectbox("Country", options=countries, label_visibility="collapsed", key="edu_country_filter")

    with f3:
        budget = st.selectbox("Budget", options=BUDGET_OPTIONS, label_visibility="collapsed", key="edu_budget_filter")

    with f4:
        scholarship = st.selectbox(
            "Scholarship",
            options=SCHOLARSHIP_OPTIONS,
            label_visibility="collapsed",
            key="edu_scholarship_filter",
        )

    with f5:
        sort_by = st.selectbox("Sort", options=SORT_OPTIONS, label_visibility="collapsed", key="edu_sort_by")

    with f6:
        per_page = st.selectbox("Page size", options=[10, 20, 30], label_visibility="collapsed", key="edu_page_size")

    filtered = _apply_filters(universities, search, country, budget, scholarship)
    sorted_rows = _sort_universities(filtered, sort_by)

    if "edu_page" not in st.session_state:
        st.session_state.edu_page = 1

    page_rows, total_pages = _paginate(sorted_rows, int(st.session_state.edu_page), int(per_page))
    st.session_state.edu_page = max(1, min(int(st.session_state.edu_page), total_pages))

    cmeta1, cmeta2 = st.columns([2, 1])
    with cmeta1:
        st.markdown(
            f'<div class="section-subtitle"><strong>{len(sorted_rows)}</strong> result(s) found</div>',
            unsafe_allow_html=True,
        )
    with cmeta2:
        st.markdown(
            f'<div class="section-subtitle" style="text-align:right;">Page {st.session_state.edu_page} of {total_pages}</div>',
            unsafe_allow_html=True,
        )

    if warning_msg:
        st.warning(warning_msg)

    if not page_rows:
        st.info("No universities found for the selected filters.")
        return

    for uni in page_rows:
        st.markdown('<article class="premium-card education-card">', unsafe_allow_html=True)
        st.markdown(f'<h3 class="result-title">#{uni["rank"]} {uni["name"]}</h3>', unsafe_allow_html=True)

        city = str(uni.get("city", "")).strip()
        location_line = f"{city}, {uni['country']}" if city else f"{uni['country']}"
        scholarship_text = "Yes" if uni.get("scholarship") else "No"

        st.markdown(
            f'<div class="result-meta"><span>{location_line}</span><span>Budget: {uni.get("budget_tier", _budget_tier_from_fee(uni.get("fee_amount")))}</span><span>Scholarship: {scholarship_text}</span></div>',
            unsafe_allow_html=True,
        )

        st.markdown(f'<div class="fee-strip">{uni["fee_structure"]}</div>', unsafe_allow_html=True)

        course_text = str(uni.get("course_details", ""))
        if len(course_text) > 220:
            course_text = course_text[:220].rstrip() + "..."
        st.markdown(f'<p class="result-description">{course_text}</p>', unsafe_allow_html=True)

        c1, c2 = st.columns([1, 1])
        with c1:
            if str(uni.get("link", "")).strip():
                st.link_button("University Website", str(uni["link"]), use_container_width=True)
            else:
                st.button("University Website", disabled=True, use_container_width=True, key=f"missing_link_{uni['id']}")

        with c2:
            msg = (
                f"Hello Kansalt, I want to apply for {uni['name']} ({uni['country']}). "
                "Please share admission process, required documents, and next steps."
            )
            wa_url = _wa_link(msg)
            if wa_url:
                st.link_button("Submit Application", wa_url, use_container_width=True)
            else:
                st.button("Submit Application", disabled=True, use_container_width=True, key=f"apply_disabled_{uni['id']}")

        st.markdown('</article>', unsafe_allow_html=True)

    nav1, nav2, nav3 = st.columns([1, 1, 2])
    with nav1:
        if st.button("Previous", use_container_width=True, disabled=st.session_state.edu_page <= 1, key="edu_prev_page"):
            st.session_state.edu_page -= 1
            st.rerun()
    with nav2:
        if st.button("Next", use_container_width=True, disabled=st.session_state.edu_page >= total_pages, key="edu_next_page"):
            st.session_state.edu_page += 1
            st.rerun()
    with nav3:
        new_page = st.number_input(
            "Go to page",
            min_value=1,
            max_value=total_pages,
            value=int(st.session_state.edu_page),
            step=1,
            key="edu_page_input",
        )
        if int(new_page) != int(st.session_state.edu_page):
            st.session_state.edu_page = int(new_page)
            st.rerun()

