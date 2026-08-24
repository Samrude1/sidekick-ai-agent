# UI Registry: Sidekick AI Agent

## Baseline — Established 2026-08-24
> *Note: This baseline was established via `/imprint audit`.*

| Property | Standard Value | Description |
| :--- | :--- | :--- |
| **Page Background** | `#fdfdfd` | Clean, modern neutral canvas |
| **Card Background** | `#ffffff` | Elevated component surface |
| **Secondary Surface** | `#f9fafb` | Callout boxes, secondary action fills |
| **Card Border** | `1px solid #e5e7eb` | Slate-200 border for cards & containers |
| **Input Border** | `1px solid #d1d5db` | Slate-300 border for input textboxes |
| **Container Radius** | `8px` | Outer cards, panels, log window |
| **Control Radius** | `6px` | Buttons, textboxes, skill icon wrappers |
| **Badge Radius** | `4px` | Role tags, status pills |
| **Button Primary** | `bg: #111827, text: #ffffff` | Main CTA ("Execute Task") |
| **Button Secondary** | `bg: #f9fafb, text: #374151, border: #d1d5db` | Utility CTA ("Reset session") |
| **Text Primary** | `#111827` / `#1f2937` | Headings, user inputs, log text |
| **Text Secondary** | `#4b5563` | Subtitles, descriptions, captions |
| **Text Muted** | `#6b7280` | Timestamps, tertiary details |
| **Accent / Success** | `#047857` (text), `#ecfdf5` (fill) | Evaluator feedback & positive evaluations |
| **Typography** | `'Inter', sans-serif` | Clean geometric sans-serif |
| **Monospace** | `'JetBrains Mono', monospace` | Timestamps, code & telemetry tags |

---

## Registered UI Components

### 1. Header & Title Block
File: `app.py`

| Property | Class / Rule |
| :--- | :--- |
| **Title Typography** | `h1 { font-size: 2.2rem; font-weight: 700; color: #111827; }` |
| **Subtitle Typography** | `#header p, #header em { font-size: 1rem; color: #4b5563; font-weight: 500; }` |
| **Reset Action** | `.reset-btn { background: #f9fafb; color: #374151; border: 1px solid #d1d5db; border-radius: 6px; }` |

### 2. Task Input Panel (`.left-panel`)
File: `app.py`

| Property | Class / Rule |
| :--- | :--- |
| **Container** | `.gr-group { background: #ffffff; border: 1px solid #e5e7eb; border-radius: 8px; padding: 18px; }` |
| **Labels** | `label, label span { color: #111827; font-weight: 600; font-size: 0.9rem; }` |
| **Input Fields** | `textarea, input { background: #ffffff; color: #111827; border: 1px solid #d1d5db; border-radius: 6px; }` |
| **Primary Action** | `button.primary { background: #111827; color: #ffffff; border-radius: 6px; font-weight: 600; }` |

### 3. Agent Capabilities Grid (`.skills-container`)
File: `app.py`

| Property | Class / Rule |
| :--- | :--- |
| **Layout** | `.skills-container { display: grid; gap: 12px; margin-top: 20px; }` |
| **Section Title** | `.section-title { font-size: 0.9rem; font-weight: 600; color: #111827; }` |
| **Skill Card** | `.skill-card { background: #ffffff; border: 1px solid #e5e7eb; border-radius: 8px; padding: 12px 15px; }` |
| **Skill Icon** | `.skill-icon { background: #f3f4f6; width: 36px; height: 36px; border-radius: 6px; }` |
| **Hover State** | `.skill-card:hover { border-color: #111827; transform: translateY(-2px); box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1); }` |

### 4. Live Log Window (`#log-window`)
Files: `app.py`, `sidekick.py`

| Property | Class / Rule |
| :--- | :--- |
| **Container** | `#log-window { background: #ffffff; border: 1px solid #e5e7eb; border-radius: 8px; height: 650px; }` |
| **Log Entry** | `.log-entry { padding: 20px 25px; border-bottom: 1px solid #f3f4f6; }` |
| **Header Meta** | `.log-header { font-family: 'JetBrains Mono'; font-size: 0.8rem; }` |
| **User Role Badge** | `.role-user { color: #374151; background: #f3f4f6; border-radius: 4px; }` |
| **Agent Role Badge** | `.role-agent { color: #111827; background: #e5e7eb; border-left: 3px solid #111827; }` |
| **Evaluator Badge** | `.role-eval { color: #047857; background: #ecfdf5; border-radius: 4px; }` |
| **Feedback Callout** | `.feedback-box { background: #f0fdf4; color: #065f46; border-left: 3px solid #10b981; border-radius: 0 6px 6px 0; }` |

### 5. Tip & Callout Badge (`.tip-box`)
File: `app.py`

| Property | Class / Rule |
| :--- | :--- |
| **Container** | `.tip-box { padding: 14px 16px; margin-top: 15px; background: #f9fafb; border: 1px solid #e5e7eb; border-radius: 8px; }` |
| **Typography** | `.tip-box p { font-size: 0.85rem; color: #374151; margin: 0; line-height: 1.5; }` |
