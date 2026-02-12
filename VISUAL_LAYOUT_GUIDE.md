# 🎨 Visual Layout Guide

## Full Page Layout

```
╔════════════════════════════════════════════════════════════════════════════╗
║  💼 kunsalt    [🏠 Home] [🎓 Education] [💼 Jobs] [🏢 Business]    👤 Login║
║  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━║
║                                                                              ║
║  ┌─────────────────────┬──────────────────────────────────────────────────┐ ║
║  │  🔍 FILTERS         │  [Search] [Sort ▼]  15 jobs found                │ ║
║  │                     │                                                    │ ║
║  │  ┌─────────────────┐│  [Python] [React] [AWS] ✕  ✕  ✕                 │ ║
║  │  │ Role / Title    ││                                                    │ ║
║  │  │ [Search Box]    ││  ┌────────────────────────────────────────────┐   │ ║
║  │  └─────────────────┘│  │ Senior Full Stack Developer                │   │ ║
║  │                     │  │ TechCorp                    2 days ago       │   │ ║
║  │  ┌─────────────────┐│  │ 📍 San Francisco, CA  💰 $120K-$160K  🕐 FT │   │ ║
║  │  │ Location        ││  │                                              │   │ ║
║  │  │ [All ▼]         ││  │ Looking for an experienced full stack...     │   │ ║
║  │  └─────────────────┘│  │                                              │   │ ║
║  │                     │  │ [Python] [React] [AWS] [PostgreSQL]         │   │ ║
║  │  ┌─────────────────┐│  │                          [✓ Apply]           │   │ ║
║  │  │ Job Type        ││  └────────────────────────────────────────────┘   │ ║
║  │  │ ☐ Full-time     ││  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━  │ ║
║  │  │ ☐ Contract      ││                                                    │ ║
║  │  │ ☐ Part-time     ││  ┌────────────────────────────────────────────┐   │ ║
║  │  └─────────────────┘│  │ Product Manager                            │   │ ║
║  │                     │  │ StartupXYZ                  1 day ago        │   │ ║
║  │  ┌─────────────────┐│  │ 📍 New York, NY  💰 $100K-$140K  🕐 FT     │   │ ║
║  │  │ Level           ││  │                                              │   │ ║
║  │  │ [All ▼]         ││  │ Shape the future of our SaaS platform...    │   │ ║
║  │  └─────────────────┘│  │                                              │   │ ║
║  │                     │  │ [Product Strategy] [Analytics] [Comm] [UX]  │   │ ║
║  │  ┌─────────────────┐│  │                      [✓ Apply]               │   │ ║
║  │  │ Skills          ││  └────────────────────────────────────────────┘   │ ║
║  │  │ ☐ Python        ││  ... (more results)                               │ ║
║  │  │ ☐ React         ││                                                    │ ║
║  │  │ ☐ AWS           ││  [← Previous] Page 1 of 3 [Next →]                │ ║
║  │  │ ☐ JavaScript    ││                                                    │ ║
║  │  └─────────────────┘│                                                    │ ║
║  │                     │                                                    │ ║
║  │  ☐ Remote only      │                                                    │ ║
║  │                     │                                                    │ ║
║  │  [Clear All ▼]      │                                                    │ ║
║  │                     │                                                    │ ║
║  └─────────────────────┴──────────────────────────────────────────────────┘ ║
║                                                                              ║
╚════════════════════════════════════════════════════════════════════════════╝

COLORS:
  Background:     #F7F3EE (warm beige)
  Cards:          #FFFFFF (white)
  Sidebar:        #EFE8DF (light beige)
  Accent:         #8B6F4E (brown)
  Border:         #E2D9CC (tan)
  Text Primary:   #2B2B2B (dark)
  Text Secondary: #5A5A5A (gray)
```

---

## Component: Result Card (Detailed)

```
┌────────────────────────────────────────────────────────┐
│ ┌──────────────────────────────────┐ 2 days ago       │
│ │ Senior Full Stack Developer      │                  │
│ │ TechCorp (in brown #8B6F4E)       │                  │
│ └──────────────────────────────────┘                  │
│                                                        │
│ 📍 San Francisco, CA  | 💰 $120K - $160K | 🕐 Full-time
│                                                        │
│ Looking for an experienced full stack developer to    │
│ lead our engineering team. You'll work on scalable    │
│ web applications and mentor junior developers.        │
│                                                        │
│ [Python] [React] [AWS] [PostgreSQL]                   │
│                                                        │
│                                         [✓ APPLY]     │
└────────────────────────────────────────────────────────┘
  △
  │
  └─ Hover: Subtle shadow, slight lift
```

---

## Component: Sidebar Filter

```
┌─────────────────────────────────┐
│ 🔍 FILTERS                      │
├─────────────────────────────────┤
│                                 │
│ ROLE / TITLE                    │  ← Uppercase label
│ [Search jobs...............]    │
│                                 │
├─────────────────────────────────┤ ← Tan border
│                                 │
│ LOCATION                        │
│ [Remote             ▼]          │
│                                 │
├─────────────────────────────────┤
│                                 │
│ JOB TYPE                        │
│ [All Types          ▼]          │
│                                 │
├─────────────────────────────────┤
│                                 │
│ LEVEL                           │
│ [All Levels         ▼]          │
│                                 │
├─────────────────────────────────┤
│                                 │
│ SKILLS                          │
│ [✓] Python                      │
│ [✓] React                       │
│ [ ] AWS                         │
│ [ ] JavaScript                  │
│                                 │
├─────────────────────────────────┤
│ [ ] Remote only                 │
├─────────────────────────────────┤
│                                 │
│  [Clear All Filters]            │
│                                 │
└─────────────────────────────────┘
  ↑
  Sticky on desktop (top: 80px)
```

---

## Component: Skills Chips

```
Active Filter Display:
┌──────────────────────────────────────────────────┐
│ [Python ✕] [React ✕] [AWS ✕] [PostgreSQL ✕]   │
└──────────────────────────────────────────────────┘

      ↓ Click ✕

Removed from filter!
```

---

## Mobile Layout (< 768px)

```
┌──────────────────────────────────┐
│ 💼 kunsalt          👤           │
├──────────────────────────────────┤
│ 🏠 🎓 💼 🏢 →                    │  ← Horizontal scroll
├──────────────────────────────────┤
│                                  │
│ 🔍 FILTERS (collapse/expand)    │
│ [Search Box]                     │
│ [Location ▼]                     │
│ [Type ▼]                         │
│ [Level ▼]                        │
│ [Skills ▼]                       │
│                                  │
├──────────────────────────────────┤
│                                  │
│ [Results]                        │
│                                  │
│ ┌────────────────────────────┐   │
│ │ Senior Dev                 │   │
│ │ TechCorp   2 days ago      │   │
│ │ 📍 SF | 💰 $120K | FT      │   │
│ │ Description...             │   │
│ │ [Python] [React]           │   │
│ │ [      ✓ APPLY      ]      │   │
│ └────────────────────────────┘   │
│                                  │
│ ... (more cards stacked)         │
│                                  │
│   [← Previous] Page 1 [Next →]   │
│                                  │
└──────────────────────────────────┘
  ↑
  Single column, full width
```

---

## Interactive States

### Button Hover (Primary)
```
NORMAL:        HOVER:
┌──────────┐   ┌──────────┐
│ ✓ APPLY  │   │ ✓ APPLY  │ ← Darker brown
└──────────┘   └──────────┘    + soft shadow
#8B6F4E        #7A5D3F         ↑ slight lift
```

### Card Hover
```
NORMAL:                    HOVER:
┌────────────────┐        ┌────────────────┐
│ Job Title      │        │ Job Title      │ ← Brown border
│ Company        │  ───→  │ Company        │   + shadow
│ Location       │        │ Location       │   ↑ lift (2px)
└────────────────┘        └────────────────┘
tan border              accent border
subtle shadow          stronger shadow
```

### Filter Label Style
```
LOCATION                  ← Uppercase
font-size: 0.85rem
font-weight: 600
letter-spacing: 0.5px
color: #2B2B2B (dark)
```

---

## Color Swatches

```
#F7F3EE ████████████████ Primary Background (Warm Beige)
#EFE8DF ████████████████ Sidebar Surface (Light Beige)
#FFFFFF ████████████████ Card/Input Surface (White)
#8B6F4E ████████████████ Accent & Buttons (Brown)
#E2D9CC ████████████████ Borders (Tan)
#2B2B2B ████████████████ Primary Text (Dark Gray)
#5A5A5A ████████████████ Secondary Text (Gray)
#8A8A8A ████████████████ Muted Text (Light Gray)
```

---

## Spacing Reference

```
Navbar height:        60px
Sticky sidebar top:   80px (below navbar)

Sidebar width:        250px
Gap between cols:     24px (1.5rem)

Card padding:         20px (1.25rem)
Card border-radius:   8px

Filter margin:        24px (1.5rem) bottom
Filter border:        1px solid tan

Button padding:       10px 20px
Button border-radius: 6px

Badge padding:        6px 12px
Badge border-radius:  6px

Skill chip:           
  padding:            6px 12px
  border-radius:      20px (pill shape)
```

---

## Typography Hierarchy

```
Page Title (H1):
  font-size: 1.5rem
  font-weight: 700
  color: #2B2B2B

Section (H2):
  font-size: 1.25rem
  font-weight: 600
  color: #2B2B2B

Card Title (H3):
  font-size: 0.95rem
  font-weight: 600
  color: #2B2B2B

Label (Filter):
  font-size: 0.85rem
  font-weight: 600
  text-transform: uppercase
  letter-spacing: 0.5px
  color: #2B2B2B

Body Text:
  font-size: 0.9rem
  color: #5A5A5A
  line-height: 1.5

Meta Text:
  font-size: 0.85rem
  color: #8A8A8A
```

---

## Responsive Breakpoints

```
Desktop:    > 1200px   │  Sidebar (250px) + Results (flex)
Tablet:     768-1200px │  Sidebar (250px) + Results (flex)
Mobile:     < 768px    │  Single column (full width)

At < 768px:
  - Sidebar shifts to top
  - Results go full width
  - Buttons become full width
  - Spacing reduces (1rem instead of 1.5rem)
```

---

**Visual Reference Complete** - Use these diagrams when building/updating UI components
