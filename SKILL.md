---
name: html-to-elementor
description: "Universal engine for converting static HTML/CSS/JavaScript websites into native, fully-editable WordPress Elementor pages, theme components, and exportable/importable JSON templates without HTML dumping."
risk: safe
source: user-global
date_added: "2026-10-19"
---

# HTML to Elementor Conversion Engine

A universal, high-fidelity skill for converting any static HTML/CSS/JavaScript codebase into native, client-editable WordPress Elementor pages, components, and exportable/importable JSON templates (`version: 0.4, type: page|section`).

---

## 1. Core Philosophy & Non-Negotiable Standards

When invoked, this skill acts as a **Senior WordPress Architect**, **Elementor Specialist**, and **Forensic Frontend Engineer**. It enforces these standards:

### A. True Native Editability (Strict Anti-HTML-Dump Rule)
* **Never dump static HTML into an `html` widget or `<iframe>`**. Dumps defeat the purpose of Elementor and prevent the end user from managing content.
* **Atomic Widget Mapping**: Every headline becomes a `heading` widget, body text becomes a `text-editor`, buttons become `button` widgets, pictures become `image` widgets, and lists become `icon-list` widgets.
* **Modern Flexbox Containers**: Structure all layouts using modern Elementor Flexbox Containers (`elType: "container"`), configuring `flex_direction`, `justify_content`, `align_items`, and `gap` directly in native settings.
* **Scoped Enhancements Only**: Reserve `settings.custom_css` strictly for glassmorphism (`backdrop-filter`), keyframe animations, pseudo-elements (`::before`/`::after`), or gradient text that native controls cannot render.
* **Zero Entity Sanitization Bugs**: In `custom_css`, never use the direct child combinator (`>`) because WordPress sanitization transforms it into `&gt;`. Always use descendant whitespace selectors (`selector .child-class`).

### B. Pixel-Perfect Design Preservation
* **Visual Identity**: Extract and honor exact design tokens (colors, gradients, typography, font families, line-heights, letter-spacing, radii, box shadows, borders, and margins).
* **Responsive Breakpoints**: Explicitly define desktop (default), tablet (`_tablet`), and mobile (`_mobile`) values so designs adapt cleanly across all viewports.
* **RTL & LTR Direction**: Preserve text direction, flex reversal, and mirrored padding/margins for Arabic/Hebrew (RTL) or English/Latin (LTR).
* **Dark / Light Modes**: Retain CSS custom property structures or create dedicated variant templates.

### C. Universal & Agnostic Operation
* Make no assumptions based on specific frameworks. The skill seamlessly converts vanilla HTML/CSS, Tailwind, Bootstrap, multi-page architectures, or single-page portfolios.

### D. 100% Local Execution (Zero-Bandwidth Protocol)
* Execute all parsing, AST analysis, template generation, JSON schema validation, and reporting **locally on the host machine**.
* Never trigger external web searches, browser bots, or external package installations unless explicitly ordered.

---

## 2. Five-Phase Conversion Workflow

```
[Phase 1: Discovery & Audit]
       │
       ▼
[Phase 2: Strategy & Delivery Definition]
       │
       ▼
[Phase 3: Deep Elementor Synthesis]
       │
       ▼
[Phase 4: Multi-Tier Verification & Self-Correction]
       │
       ▼
[Phase 5: Packaging & Client Delivery]
```

---

### Phase 1: Discovery, Forensic Audit & Architecture Mapping

1. **Asset & Structure Inventory**:
   * Scan local repository to identify all HTML pages, CSS files, JavaScript scripts, images, SVG icons, and web fonts.
   * Document page hierarchy, reusable partials (Header, Footer, Navigation, Modals, Call-to-Actions), and dynamic widgets.
2. **Design System Forensic Extraction**:
   * Inspect stylesheet roots (`:root`, `tokens.css`, Tailwind config, or inline styles).
   * Construct an internal palette and typography map:
     * Primary, secondary, surface, and accent colors.
     * Font families, weights, and modular type scales.
     * Container max-widths, section vertical padding, and grid gutters.
3. **Interactive & JS Behavior Audit**:
   * Catalogue interactive elements: dropdowns, mobile navigation drawers, sliders (e.g. Swiper), tabs, filterable grids, modals, accordions, and contact forms.
   * Classify each interaction:
     * *Native Elementor*: Can be implemented via standard widgets, nested tabs, or Menu widgets.
     * *CSS-Driven*: Handled via transitions, keyframes, or `:hover` states.
     * *Custom Script*: Requires lightweight, scoped vanilla JavaScript.
4. **Produce Conversion Matrix**:
   * Present an explicit section-by-section mapping table before generating files.

---

### Phase 2: Strategy & Delivery Definition

Establish the delivery scope with the user:

#### Mode A: Elementor JSON Templates Only
* Generate importable templates (`*-importable.json`) conforming to Elementor's export schema (`version: 0.4`, `type: page|section`).
* Also provide raw `_elementor_data` JSON arrays for direct REST API or CLI insertion.
* Do not alter source codebase or build a traditional PHP WordPress theme unless requested.

#### Mode B: Complete WordPress Site Deployment
* When a connected WordPress environment (local or remote REST API) is provided:
  * Check WordPress and Elementor version and active features (e.g., Flexbox Container experiment status).
  * Check Elementor Free vs. Elementor Pro availability.
  * Create/update pages via REST API (`/wp-json/wp/v2/pages` and `_elementor_data` postmeta).
  * Configure Global Header/Footer templates.

---

### Phase 3: Deep Elementor Synthesis (The Conversion Engine)

1. **Top-Level Container Hierarchy**:
   * Map each HTML `<section>` to an outer Elementor container:
     ```json
     {
       "id": "sec_hero",
       "elType": "container",
       "isInner": false,
       "settings": {
         "content_width": "boxed",
         "boxed_width": { "unit": "px", "size": 1200 },
         "flex_direction": "column",
         "padding": { "unit": "px", "top": "100", "right": "24", "bottom": "100", "left": "24", "isLinked": false }
       },
       "elements": [ ... ]
     }
     ```
2. **Inner Columns & Grid Layouts**:
   * Transform nested grid/flex wrappers (`<div class="row">`, `<div class="grid">`) into child containers (`"isInner": true`).
   * Set `flex_direction` to `"row"` (or `"column"`), configure `flex_wrap: "wrap"`, and distribute column widths via `width: { "unit": "%", "size": 50 }` or `flex_grow: 1`.
3. **Atomic Widget Transformation**:
   * **Headings**: Map `<h1>`-`<h6>` to `heading` widgets with explicit typography, tag hierarchy, and color tokens.
   * **Paragraphs & Copy**: Map `<p>` and descriptive spans to `text-editor` widgets.
   * **Action Buttons**: Map `<a>` and `<button>` to `button` widgets with hover states and border-radius pill styling.
   * **Media**: Map `<img>` to `image` widgets with explicit sizing and alt tags.
   * **Icons**: Map `<i>` / SVGs to `icon` or `icon-box` widgets.
   * **Bullet Points**: Map `<ul><li>` to `icon-list` widgets.
4. **Styling Injection & Micro-CSS**:
   * Inject visual design directly into `settings`:
     * Background colors, gradients, and images.
     * Box shadows, borders, border-radius.
   * Use `settings.custom_css` exclusively for scoped advanced CSS:
     ```css
     selector {
       backdrop-filter: blur(16px);
       -webkit-backdrop-filter: blur(16px);
       transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
     }
     selector:hover {
       transform: translateY(-6px);
       box-shadow: 0 20px 40px rgba(0, 0, 0, 0.3);
     }
     ```

---

### Phase 4: Multi-Tier Verification & Self-Correction

Never declare a template complete without programmatic validation.

1. **Schema & Syntax Validation**:
   * Execute the included local validation utility:
     ```bash
     python "<SKILL_DIR>/scripts/validate_elementor_template.py" "<PATH_TO_GENERATED_TEMPLATE.json>"
     ```
   * The validator programmatically verifies:
     * ✅ Root structure (`version: 0.4`, `title`, `type`, `content: [...]`).
     * ✅ Structural integrity (`id`, `elType`, `settings`, `elements`).
     * ✅ **Strict ID Uniqueness** (no duplicate IDs across the template).
     * ✅ **Editability Index** (calculates percentage of native widgets; flags if raw `html` widgets exceed threshold).
     * ✅ **Sanitization Safety** (checks for forbidden `&gt;` entities in custom CSS).
2. **Responsive Verification**:
   * Verify that responsive breakpoints (`_tablet`, `_mobile`) are present on layout containers and font sizes.
3. **Live Import Verification (When Environment Is Active)**:
   * If REST API is active, push the JSON payload and verify HTTP 200/201 response.
4. **Self-Correction Protocol**:
   * If the validator reports errors or warnings, parse the exact error report, locate the faulty container or widget ID, apply the fix, and re-run validation until 100% compliant.

---

### Phase 5: Packaging & Client Delivery

Organize all output assets in a clean, professional structure:

```
elementor-output/
├── templates/
│   ├── page-home-importable.json          # Ready for Elementor Import Template UI
│   ├── page-about-importable.json
│   ├── section-header-importable.json
│   └── section-footer-importable.json
├── raw-data/
│   ├── page-home.json                     # Raw _elementor_data postmeta
│   └── page-about.json
├── assets-manifest.json                   # List of images/fonts used and WP target paths
├── README-IMPORT-GUIDE.md                 # Clear, concise import instructions
└── VERIFICATION-REPORT.md                 # Forensic audit results & editability scores
```

Deliverables must always include:
1. **Importable JSON files** ready for WordPress Admin -> Templates -> Saved Templates -> Import Templates.
2. **Step-by-step import instructions**.
3. **Validation Summary** confirming zero schema errors and high Editability Index.

---

## 3. Reference Documentation & Tooling

* **Detailed Schema Reference**: Consult [`references/elementor-template-schema.md`](references/elementor-template-schema.md) for complete Container JSON schemas, widget models, responsive suffix conventions, and property tables.
* **Validation Script**: Use [`scripts/validate_elementor_template.py`](scripts/validate_elementor_template.py) to validate any JSON template instantly with zero dependencies.
