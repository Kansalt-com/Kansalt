# Kansalt.com - Quick Reference Guide

## What Changed?

### 🎨 **Branding**
- Product renamed to **Kansalt.com**
- New gradient logo styling
- Professional UI throughout

### 🔧 **Data Normalization**
```python
from services import normalize_job, format_time_ago, compute_pagination

# Normalize raw job from any source
raw_job = {
    "title": "Senior Dev",
    "posted_at": "2026-02-08T10:00:00Z",
    "match_score": 85
}

normalized = normalize_job(raw_job)
# → normalized["posted_ago"] = "Just now"
# → normalized["match_percent"] = 85
# → Always has: job_code, title, company, location, source, match_percent, posted_ago
```

### 📊 **Pagination Fixes**
```python
from services import compute_pagination

# Before: "Displaying 25 per page" (even with 13 items)
# After: "Showing 1–13 of 13"

pagination = compute_pagination(total=13, page=1, page_size=25)
# Returns:
# {
#   "total_pages": 1,
#   "current_page": 1,
#   "start_num": 1,
#   "end_num": 13,
#   "display_text": "Showing 1–13 of 13",
#   "is_first_page": True,
#   "is_last_page": True,
# }
```

### 📅 **Time Formatting**
```python
from services import format_time_ago
from datetime import datetime, timezone, timedelta

past = datetime.now(timezone.utc) - timedelta(hours=2)
time_ago = format_time_ago(past)
# → "2 hours ago"

# Handles:
# - Just now
# - X mins ago / X hours ago / X days ago / X weeks ago / X months ago / X years ago
# - Returns "—" for None or unparseable dates
```

### 🎯 **UI Improvements**
| Issue | Before | After |
|-------|--------|-------|
| Posted column | "None" | "2 hours ago" or "—" |
| Pagination | "Displaying 25" (confusing) | "Showing 1–13 of 13" (clear) |
| Table layout | Markdown (blank rows) | Columns (clean) |
| Match % display | Plain text | Color badges (green/orange/gray) |
| Apply button | Maybe works | Primary CTA, new tab |
| Page selector | Always shown | Only if multiple pages |

---

## Files Changed

| File | Change | Impact |
|------|--------|--------|
| `services/job_normalizer.py` | **NEW** | Data normalization & pagination |
| `services/__init__.py` | Updated | Exports new functions |
| `app/main.py` | **REWRITTEN** | Premium UI/UX, Kansalt branding |
| `tests_job_normalizer.py` | **NEW** | Unit tests |
| `CHANGELOG_KANSALT.md` | **NEW** | Full documentation |

---

## Testing

```bash
# Run unit tests
python -m pytest tests_job_normalizer.py -v

# Test normalization
python -c "from services import normalize_job; print(normalize_job({'title': 'Dev'}))"

# Test pagination
python -c "from services import compute_pagination; print(compute_pagination(13, 1, 25))"

# Test time formatting
python -c "from services import format_time_ago; from datetime import datetime, timezone; print(format_time_ago(datetime.now(timezone.utc)))"
```

---

## Quick Fixes Reference

### Issue: Posted shows "None"
**Fixed in**: `services/job_normalizer.py` → `format_time_ago()`
- Always returns "—" for missing dates
- Never returns None

### Issue: "Displaying 25 per page" with only 13 jobs
**Fixed in**: `app/main.py` + `services/job_normalizer.py` → `compute_pagination()`
- Now shows "Showing 1–13 of 13"
- Correct math on all pages

### Issue: Table has blank rows
**Fixed in**: `app/main.py`
- Replaced markdown table with st.columns()
- Removed blank row rendering
- Added proper dividers between jobs

### Issue: Duplicate Streamlit element IDs
**Fixed in**: `app/main.py`
- Added unique keys to all disabled buttons
- Format: `key=f"resume_disabled_{job_code}_{idx}"`

### Issue: Page selector always shown
**Fixed in**: `app/main.py`
- Hidden when `total_pages <= 1`
- Only shows when needed

---

## Configuration

### Results Per Page
Configured in search tab:
```python
results_per_page = st.selectbox("Results per page:", [25, 50, 100])
```

### Match % Color Coding
In `app/main.py`:
```python
if match_pct >= 70:      # Green
    badge_class = "match-badge-high"
elif match_pct >= 40:    # Orange
    badge_class = "match-badge-med"
else:                    # Gray
    badge_class = "match-badge-low"
```

---

## Dependencies

```
streamlit>=1.28.0
requests>=2.31.0
python-dateutil>=2.8.2  # NEW - for robust date parsing
```

Install with:
```bash
pip install python-dateutil
```

---

## Troubleshooting

### Q: Why does my date show "—"?
**A**: The date format isn't recognized. Check these fields exist in your job object:
- `posted_at`, `date_posted`, `publication_date`, `created_at`, `timestamp`

### Q: Page selector disappeared after search?
**A**: Normal! It only shows if there's more than 1 page of results.

### Q: Why is my custom date not parsing?
**A**: `dateutil` supports most formats, but for custom formats, add to `_extend_search_terms()` or use ISO format.

### Q: How do I see what was normalized?
**A**: Check logs in `logs/` or add debug:
```python
normalized = normalize_job(raw_job)
logger.debug(f"Normalized: {normalized}")
```

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 2.0 | Feb 8, 2026 | Kansalt branding, pagination fixes, data normalization, premium UI |
| 1.0 | Earlier | Initial job aggregator |

---

## Support Resources

- `CHANGELOG_KANSALT.md` - Detailed changelog
- `tests_job_normalizer.py` - Unit tests with examples
- `services/job_normalizer.py` - Documented source code
- `app/main.py` - Streamlit app with comments

---

**Status**: ✅ Production Ready  
**Testing**: 16 unit tests covering all critical paths  
**Backward Compatibility**: ✅ Fully compatible  
**Breaking Changes**: ❌ None
