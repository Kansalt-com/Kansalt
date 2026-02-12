# 💼 Dashboard UI Component Reference

## CSS Classes & Structure

### Main Layout Grid
```css
.dashboard-container {
    display: grid;
    grid-template-columns: 250px 1fr;
    gap: 1.5rem;
}

.sidebar-filters {
    background: var(--card-bg);
    border: 1px solid var(--border);
    border-radius: 8px;
    padding: 1.5rem;
    position: sticky;
    top: 80px;  /* Below navbar */
}

.results-area {
    display: flex;
    flex-direction: column;
    gap: 1rem;
}
```

### Filter Sections
```css
.filter-section {
    margin-bottom: 1.5rem;
    padding-bottom: 1.5rem;
    border-bottom: 1px solid var(--border);
}

.filter-label {
    font-size: 0.85rem;
    font-weight: 600;
    color: var(--text-primary);
    margin-bottom: 0.75rem;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}
```

### Result Cards
```css
.result-item {
    background: var(--card-bg);
    border: 1px solid var(--border);
    border-radius: 8px;
    padding: 1.25rem;
    margin-bottom: 1rem;
    transition: all 200ms ease;
}

.result-item:hover {
    box-shadow: 0 4px 12px rgba(139, 111, 78, 0.12);
    border-color: var(--accent);
    transform: translateY(-2px);
}

.result-title {
    font-size: 0.95rem;
    font-weight: 600;
    color: var(--text-primary);
}

.result-meta {
    display: flex;
    gap: 1.5rem;
    margin-bottom: 0.75rem;
    font-size: 0.85rem;
    color: var(--text-muted);
}

.result-description {
    color: var(--text-secondary);
    font-size: 0.9rem;
    margin-bottom: 1rem;
    line-height: 1.5;
}
```

### Skills/Badges
```css
.badge {
    display: inline-block;
    padding: 6px 12px;
    border-radius: 6px;
    font-size: 0.8rem;
    font-weight: 500;
    background: var(--sidebar-bg);
    color: var(--accent);
    border: 1px solid var(--border);
}

.skill-chip {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    padding: 6px 12px;
    background: var(--sidebar-bg);
    color: var(--accent);
    border: 1px solid var(--border);
    border-radius: 20px;  /* Rounded pill shape */
    font-size: 0.85rem;
}

.skill-chip .remove-btn {
    cursor: pointer;
    font-weight: bold;
    color: var(--text-muted);
}

.skill-chip .remove-btn:hover {
    color: #d32f2f;
}
```

### Buttons
```css
button[kind="primary"] {
    background: var(--accent) !important;        /* #8B6F4E */
    color: white !important;
    padding: 10px 20px !important;
    border-radius: 6px !important;
    border: 1px solid var(--accent) !important;
    font-weight: 600 !important;
}

button[kind="primary"]:hover {
    background: #7A5D3F !important;              /* Darker brown */
    box-shadow: 0 4px 12px rgba(139, 111, 78, 0.15) !important;
    transform: translateY(-1px) !important;
}

button[kind="secondary"] {
    background: var(--primary-bg) !important;
    color: var(--accent) !important;
    border: 1px solid var(--border) !important;
}

button[kind="secondary"]:hover {
    background: var(--sidebar-bg) !important;
    border-color: var(--accent) !important;
}
```

### Navbar
```css
.navbar-container {
    position: sticky;
    top: 0;
    z-index: 999;
    background: white;
    border-bottom: 1px solid var(--border);
    padding: 0.75rem 2rem;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
}

.navbar-brand {
    font-size: 1.2rem;
    font-weight: 700;
    color: var(--accent);
}

.tab-btn {
    padding: 0.75rem 1.5rem;
    border: none;
    background: transparent;
    color: var(--text-secondary);
    font-weight: 500;
    font-size: 0.95rem;
    border-bottom: 2px solid transparent;
}

.tab-btn:hover {
    color: var(--accent);
}

.tab-btn.active {
    color: var(--accent);
    border-bottom: 2px solid var(--accent);
    font-weight: 600;
}
```

### Pagination
```css
.pagination {
    display: flex;
    justify-content: center;
    align-items: center;
    gap: 0.5rem;
    margin-top: 2rem;
    padding: 1.5rem;
}

.pagination button {
    min-width: 40px;
    height: 40px;
    padding: 0;
    border-radius: 6px;
    border: 1px solid var(--border);
    background: white;
    color: var(--text-primary);
    font-weight: 500;
    cursor: pointer;
}

.pagination button:hover {
    border-color: var(--accent);
    background: var(--sidebar-bg);
}

.pagination button.active {
    background: var(--accent);
    color: white;
    border-color: var(--accent);
}
```

---

## HTML Structure Examples

### Complete Job Card
```html
<div class="result-item">
    <!-- Header with title and meta -->
    <div style="display: flex; justify-content: space-between; align-items: flex-start;">
        <div>
            <h3 class="result-title">Senior Full Stack Developer</h3>
            <p style="color: var(--accent); font-weight: 500;">TechCorp</p>
        </div>
        <div style="text-align: right; font-size: 0.85rem; color: var(--text-muted);">2 days ago</div>
    </div>
    
    <!-- Metadata row -->
    <div class="result-meta">
        <span>📍 San Francisco, CA</span>
        <span>💰 $120K - $160K</span>
        <span>🕐 Full-time</span>
    </div>
    
    <!-- Description -->
    <p class="result-description">
        Looking for an experienced full stack developer to lead our engineering team...
    </p>
    
    <!-- Skills badges -->
    <div class="result-tags">
        <span class="badge">Python</span>
        <span class="badge">React</span>
        <span class="badge">AWS</span>
        <span class="badge">PostgreSQL</span>
    </div>
    
    <!-- Action button -->
    <button kind="primary" style="width: 100%;">✓ Apply</button>
</div>
```

### Sidebar Filter Section
```html
<div class="sidebar-filters">
    <h3>🔍 Filters</h3>
    
    <!-- Search -->
    <div class="filter-section">
        <div class="filter-label">Role / Title</div>
        <input type="text" placeholder="e.g., Developer" class="search-input" />
    </div>
    
    <!-- Location Dropdown -->
    <div class="filter-section">
        <div class="filter-label">Location</div>
        <select>
            <option>All Locations</option>
            <option>Remote</option>
            <option>San Francisco, CA</option>
            <option>New York, NY</option>
        </select>
    </div>
    
    <!-- Checkbox Group -->
    <div class="filter-section">
        <div class="filter-label">Job Type</div>
        <label><input type="checkbox" /> Full-time</label>
        <label><input type="checkbox" /> Contract</label>
        <label><input type="checkbox" /> Part-time</label>
    </div>
    
    <!-- Clear Button -->
    <button kind="secondary" style="width: 100%; margin-top: 1rem;">Clear All Filters</button>
</div>
```

### Sort & Filter Bar
```html
<div class="sort-row">
    <div class="sort-label"><strong>15 jobs found</strong></div>
    <select>
        <option>Newest</option>
        <option>Most Relevant</option>
        <option>Salary (High to Low)</option>
    </select>
</div>

<!-- Active filters as chips -->
<div class="skills-container">
    <span class="skill-chip">Python <span class="remove-btn">✕</span></span>
    <span class="skill-chip">React <span class="remove-btn">✕</span></span>
</div>
```

---

## Streamlit Integration Examples

### Creating Sidebar Filters (Streamlit)
```python
col_sidebar, col_results = st.columns([1, 3.5], gap="large")

with col_sidebar:
    st.markdown('<div class="sidebar-filters">', unsafe_allow_html=True)
    st.markdown("### 🔍 Filters")
    
    # Search input
    st.markdown('<div class="filter-section">', unsafe_allow_html=True)
    st.markdown('<div class="filter-label">Role / Title</div>', unsafe_allow_html=True)
    search = st.text_input("Search", placeholder="e.g., Developer", label_visibility="collapsed")
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Dropdown
    st.markdown('<div class="filter-section">', unsafe_allow_html=True)
    st.markdown('<div class="filter-label">Location</div>', unsafe_allow_html=True)
    location = st.selectbox("Location", ["All", "Remote", "SF", "NYC"], label_visibility="collapsed")
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
```

### Creating Result Cards
```python
with col_results:
    for job in jobs:
        st.markdown('<div class="result-item">', unsafe_allow_html=True)
        
        col1, col2 = st.columns([5, 1])
        with col1:
            st.markdown(f'<h3 class="result-title">{job["title"]}</h3>', unsafe_allow_html=True)
            st.markdown(f'<p style="color: var(--accent);">{job["company"]}</p>', unsafe_allow_html=True)
        
        with col2:
            st.markdown(f'<div style="text-align: right;">{job["posted"]}</div>', unsafe_allow_html=True)
        
        st.markdown(f'<div class="result-meta"><span>📍 {job["location"]}</span></div>', unsafe_allow_html=True)
        st.markdown(f'<p class="result-description">{job["description"]}</p>', unsafe_allow_html=True)
        
        # Skills
        st.markdown('<div class="result-tags">', unsafe_allow_html=True)
        for skill in job["skills"]:
            st.markdown(f'<span class="badge">{skill}</span>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        if st.button("✓ Apply", key=f"apply_{job['id']}", use_container_width=True):
            st.success(f"Applied to {job['title']}")
        
        st.markdown('</div>', unsafe_allow_html=True)
```

---

## Responsive Design Breakpoints

```css
@media (max-width: 768px) {
    /* Single column on mobile */
    .dashboard-container {
        grid-template-columns: 1fr;
    }
    
    /* Sticky sidebar becomes static */
    .sidebar-filters {
        position: static;
        top: auto;
    }
    
    /* Sort bar stacks */
    .sort-row {
        flex-direction: column;
        align-items: flex-start;
    }
    
    /* Full-width buttons */
    button {
        width: 100%;
    }
    
    /* Smaller headings */
    h1 { font-size: 1.25rem; }
    h2 { font-size: 1.1rem; }
}
```

---

## Color Usage Quick Reference

| Element | Color | Code |
|---------|-------|------|
| Main Background | Beige | #F7F3EE |
| Sidebar | Light Beige | #EFE8DF |
| Cards/Input | White | #FFFFFF |
| Buttons/Headers | Brown | #8B6F4E |
| Borders | Tan | #E2D9CC |
| Primary Text | Dark Gray | #2B2B2B |
| Secondary Text | Gray | #5A5A5A |
| Muted Text | Light Gray | #8A8A8A |

**Shadow Pattern**: `0 4px 12px rgba(139, 111, 78, 0.12)` (subtle brown shadow on hover)

---

## Do's ✅ and Don'ts ❌

### ✅ DO:
- Use tan borders for subtle separation
- Show results above fold with compact spacing
- Apply brown accent (#8B6F4E) to active/hover states
- Stack filters vertically in sidebar
- Show action buttons (Apply, Contact) prominently
- Use badge styling for skills/tags
- Keep cards clean with white backgrounds

### ❌ DON'T:
- Add giant hero sections or banners
- Use neon colors or glowing effects
- Write marketing paragraphs or copy
- Hide results below long sections
- Use drop shadows on every element
- Add unnecessary animations
- Change the font to monospace
- Make the sidebar dark or colorful

---

**Dashboard Component Library** - Ready for production use!
