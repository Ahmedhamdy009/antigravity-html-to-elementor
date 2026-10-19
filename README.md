# HTML to Elementor Conversion Skill (Antigravity Global Skill)

A professional, reusable **Global Skill** for Google DeepMind Antigravity and AI coding agents to convert static HTML/CSS/JavaScript websites into native, fully-editable WordPress Elementor pages, theme components, and exportable/importable JSON templates (`version: 0.4, type: page`).

## 🚀 Key Features

* **Strict Anti-HTML-Dump**: Converts headings, paragraphs, buttons, icons, and media into native Elementor widgets instead of raw HTML blocks.
* **Flexbox Containers Architecture**: Builds modern Flexbox layouts (`elType: "container"`) with native gap, wrap, direction, and alignment controls.
* **Pixel-Perfect Preservation**: Retains exact typography, colors, gradients, borders, shadows, and responsive breakpoints (Desktop, Tablet, Mobile).
* **RTL & LTR Support**: Fully supports bidirectional layouts (Arabic / Hebrew / English).
* **Built-in Schema & Editability Validator**: Includes a zero-dependency local Python script (`validate_elementor_template.py`) that audits template integrity, ID uniqueness, and computes an automated Editability Score.

## 📂 Repository Structure

```
html-to-elementor/
├── SKILL.md                                 # Core agent instructions & 5-phase conversion workflow
├── README.md                                # Project overview & setup instructions
├── references/
│   └── elementor-template-schema.md         # Full Elementor JSON schema specification & widget dictionary
└── scripts/
    └── validate_elementor_template.py       # Standalone Python validator (zero external dependencies)
```

## 🛠️ How to Install in Antigravity

Clone or copy this folder into your Antigravity global skills directory:

```bash
# Windows
git clone https://github.com/YOUR_USERNAME/html-to-elementor.git "%USERPROFILE%\.gemini\config\skills\html-to-elementor"

# Linux / macOS
git clone https://github.com/YOUR_USERNAME/html-to-elementor.git ~/.gemini/config/skills/html-to-elementor
```

## 💡 How to Use

> "استخدم مهارة html-to-elementor وحول الموقع"

In any Antigravity chat workspace, simply prompt the agent:
> *"Using the `html-to-elementor` skill, convert this website into importable Elementor JSON templates."*
## 🧪 Testing Templates

Validate any generated Elementor JSON template locally:

```bash
python scripts/validate_elementor_template.py "path/to/template-importable.json"
```

## 📄 License
MIT License. Free to use and customize.
