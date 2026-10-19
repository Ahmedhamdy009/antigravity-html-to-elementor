# Elementor JSON Template Specification & Conversion Reference

This reference documents the structural schema, element models, and styling patterns required to generate 100% valid, importable, and fully-editable Elementor templates from static HTML/CSS codebases.

---

## 1. File Formats: Importable vs. Raw Database

Elementor utilizes two distinct JSON structures depending on the execution workflow:

### A. The Importable Template Wrapper (`*-importable.json`)
Used for standard WordPress Admin import via **Templates -> Saved Templates -> Import Templates**:

```json
{
  "version": "0.4",
  "title": "Descriptive Page or Section Name",
  "type": "page",
  "content": [
    {
      "id": "sec_hero_01",
      "elType": "container",
      "isInner": false,
      "settings": { ... },
      "elements": [ ... ]
    }
  ]
}
```

* **Root Keys:**
  * `version`: Must be `"0.4"`.
  * `title`: Descriptive template title (visible in Elementor library).
  * `type`: Standard types are `"page"`, `"section"`, `"container"`, `"header"`, `"footer"`, `"single"`, or `"archive"`.
  * `content`: Ordered array of top-level containers/sections.

### B. Raw Postmeta Format (`*.json` / `_elementor_data`)
Used when injecting directly into WordPress database or via WordPress REST API (`update_post_meta($page_id, '_elementor_data', $json)`):

```json
[
  {
    "id": "sec_hero_01",
    "elType": "container",
    "isInner": false,
    "settings": { ... },
    "elements": [ ... ]
  }
]
```

---

## 2. Container Architecture (Modern Flexbox)

Modern Elementor builds rely on Flexbox Containers (`elType: "container"`).

### Core Container Schema
```json
{
  "id": "unique_container_id",
  "elType": "container",
  "isInner": false,
  "settings": {
    "content_width": "boxed",
    "boxed_width": { "unit": "px", "size": 1200 },
    "flex_direction": "row",
    "flex_wrap": "wrap",
    "justify_content": "space-between",
    "align_items": "center",
    "flex_gap": { "unit": "px", "size": 24, "column": "24", "row": "24" },
    "padding": { "unit": "px", "top": "80", "right": "24", "bottom": "80", "left": "24", "isLinked": false },
    "background_background": "classic",
    "background_color": "#0B1120",
    "border_radius": { "unit": "px", "top": "16", "right": "16", "bottom": "16", "left": "16", "isLinked": true }
  },
  "elements": []
}
```

### Layout Properties Reference
* `flex_direction`: `"row"`, `"column"`, `"row-reverse"`, `"column-reverse"`.
* `flex_wrap`: `"nowrap"`, `"wrap"`.
* `justify_content`: `"flex-start"`, `"center"`, `"flex-end"`, `"space-between"`, `"space-around"`, `"space-evenly"`.
* `align_items`: `"flex-start"`, `"center"`, `"flex-end"`, `"stretch"`.

---

## 3. Native Widgets Dictionary (Anti-HTML-Dump)

Every visual component in the source HTML must map to a native Elementor widget whenever possible to ensure client editability.

### 1. Heading (`widgetType: "heading"`)
Replaces `<h1>` through `<h6>` tags.
```json
{
  "id": "w_heading_01",
  "elType": "widget",
  "widgetType": "heading",
  "settings": {
    "title": "Engineered for High-Performance Growth",
    "header_size": "h2",
    "align": "left",
    "title_color": "#FFFFFF",
    "typography_typography": "custom",
    "typography_font_family": "Inter",
    "typography_font_size": { "unit": "px", "size": 42 },
    "typography_font_weight": "700",
    "typography_line_height": { "unit": "em", "size": 1.2 }
  }
}
```

### 2. Text Editor (`widgetType: "text-editor"`)
Replaces paragraphs `<p>`, rich descriptions, and multi-line content.
```json
{
  "id": "w_desc_01",
  "elType": "widget",
  "widgetType": "text-editor",
  "settings": {
    "editor": "<p>We design and construct digital products that command attention.</p>",
    "text_color": "#94A3B8",
    "typography_typography": "custom",
    "typography_font_size": { "unit": "px", "size": 16 },
    "typography_line_height": { "unit": "em", "size": 1.6 }
  }
}
```

### 3. Button (`widgetType: "button"`)
Replaces CTA links `<a class="btn">` and `<button>`.
```json
{
  "id": "w_btn_01",
  "elType": "widget",
  "widgetType": "button",
  "settings": {
    "text": "Start Project",
    "link": { "url": "#contact", "is_external": false, "nofollow": false },
    "size": "md",
    "button_text_color": "#FFFFFF",
    "background_color": "#2563EB",
    "border_radius": { "unit": "px", "top": "50", "right": "50", "bottom": "50", "left": "50", "isLinked": true },
    "button_padding": { "unit": "px", "top": "14", "right": "28", "bottom": "14", "left": "28", "isLinked": false }
  }
}
```

### 4. Image (`widgetType: "image"`)
Replaces `<img>` tags.
```json
{
  "id": "w_img_hero",
  "elType": "widget",
  "widgetType": "image",
  "settings": {
    "image": { "url": "assets/images/hero.webp", "id": "" },
    "image_size": "full",
    "align": "center",
    "border_radius": { "unit": "px", "top": "20", "right": "20", "bottom": "20", "left": "20", "isLinked": true }
  }
}
```

### 5. Icon (`widgetType: "icon"`)
Replaces SVG icons and FontAwesome icons (`<i>`).
```json
{
  "id": "w_icon_check",
  "elType": "widget",
  "widgetType": "icon",
  "settings": {
    "selected_icon": { "value": "fas fa-check", "library": "fa-solid" },
    "view": "default",
    "primary_color": "#38BDF8",
    "size": { "unit": "px", "size": 20 }
  }
}
```

### 6. Icon List (`widgetType: "icon-list"`)
Replaces feature bullet lists `<ul><li><i class="check"></i> Text</li></ul>`.
```json
{
  "id": "w_feature_list",
  "elType": "widget",
  "widgetType": "icon-list",
  "settings": {
    "icon_list": [
      {
        "text": "100% Native Editability",
        "selected_icon": { "value": "fas fa-check-circle", "library": "fa-solid" }
      },
      {
        "text": "Responsive Breakpoints Included",
        "selected_icon": { "value": "fas fa-check-circle", "library": "fa-solid" }
      }
    ]
  }
}
```

### 7. HTML Widget (`widgetType: "html"`) - STRICT RESTRICTIONS
**CRITICAL**: Use the HTML widget ONLY when dealing with non-standard elements that Elementor cannot represent natively:
- Complex multi-point interactive SVG animations or Canvas graphs.
- Custom inline script tags or third-party embeds (e.g. specialized trading charts, embeds).
**Rule of Thumb:** HTML widgets must NOT exceed 10% of total widgets in any converted template.

---

## 4. Responsive Breakpoint Settings

Elementor encodes responsive variations by appending suffixes to property names:
* **Desktop**: Default key (e.g., `flex_direction`, `font_size`, `padding`)
* **Tablet (768px - 1024px)**: `_tablet` suffix (e.g., `flex_direction_tablet: "column"`, `typography_font_size_tablet: {"unit": "px", "size": 32}`)
* **Mobile (<= 767px)**: `_mobile` suffix (e.g., `padding_mobile: {"unit": "px", "top": "40", "bottom": "40", ...}`)

---

## 5. Custom CSS Best Practices (`settings.custom_css`)

Elementor allows per-element Custom CSS inside `settings.custom_css`. Adhere strictly to these rules:

1. **Avoid Direct Child Selector (`>`)**:
   WordPress sanitization filters often convert `>` into `&gt;` in the database, breaking styles.
   * ❌ WRONG: `selector > .card-title { color: #fff; }`
   * ✅ CORRECT: `selector .card-title { color: #fff; }`

2. **Always Scope with `selector`**:
   `selector` automatically resolves to the unique class of the container or widget.
   ```css
   selector {
     backdrop-filter: blur(12px);
     -webkit-backdrop-filter: blur(12px);
   }
   selector:hover {
     transform: translateY(-4px);
   }
   ```

3. **Keyframe Animations**:
   Scope keyframe names to avoid global collisions:
   ```css
   @keyframes pulse_hero {
     0%, 100% { opacity: 1; transform: scale(1); }
     50% { opacity: 0.8; transform: scale(1.05); }
   }
   selector .glow-element {
     animation: pulse_hero 3s infinite ease-in-out;
   }
   ```
