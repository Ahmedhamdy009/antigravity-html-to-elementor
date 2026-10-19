#!/usr/bin/env python3
"""
Elementor Template JSON Validator
Author: Antigravity Global Skill 'html-to-elementor'
Zero external dependencies (uses standard library only).
"""

import sys
import os
import json
import argparse
from typing import Dict, List, Set, Any, Tuple

if sys.stdout.encoding and sys.stdout.encoding.lower() != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

REQUIRED_ROOT_IMPORTABLE_KEYS = {"version", "title", "type", "content"}
VALID_TEMPLATE_TYPES = {"page", "section", "container", "header", "footer", "single", "archive", "popup"}
VALID_EL_TYPES = {"container", "section", "column", "widget"}

class ElementorTemplateValidator:
    def __init__(self, file_path: str, max_html_widget_ratio: float = 0.20):
        self.file_path = file_path
        self.max_html_widget_ratio = max_html_widget_ratio
        self.errors: List[str] = []
        self.warnings: List[str] = []
        self.seen_ids: Set[str] = set()
        self.duplicate_ids: Set[str] = set()
        self.stats = {
            "is_importable_wrapper": False,
            "template_type": "unknown",
            "template_title": "unknown",
            "version": "unknown",
            "total_elements": 0,
            "containers": 0,
            "sections": 0,
            "columns": 0,
            "widgets": 0,
            "widget_breakdown": {},
            "custom_css_blocks": 0,
            "editability_score": 100.0
        }

    def validate(self) -> bool:
        if not os.path.exists(self.file_path):
            self.errors.append(f"File not found: {self.file_path}")
            return False

        try:
            with open(self.file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
        except json.JSONDecodeError as e:
            self.errors.append(f"Invalid JSON syntax: {str(e)}")
            return False
        except Exception as e:
            self.errors.append(f"Error reading file: {str(e)}")
            return False

        content_elements: List[Dict[str, Any]] = []

        if isinstance(data, dict):
            # Check for importable format
            missing_keys = REQUIRED_ROOT_IMPORTABLE_KEYS - set(data.keys())
            if not missing_keys:
                self.stats["is_importable_wrapper"] = True
                self.stats["template_type"] = data.get("type", "unknown")
                self.stats["template_title"] = data.get("title", "unknown")
                self.stats["version"] = data.get("version", "unknown")

                if data.get("type") not in VALID_TEMPLATE_TYPES:
                    self.warnings.append(
                        f"Unconventional template type '{data.get('type')}'. Recommended types: {sorted(list(VALID_TEMPLATE_TYPES))}"
                    )

                raw_content = data.get("content")
                if not isinstance(raw_content, list):
                    self.errors.append("'content' field in importable template must be a JSON array of sections/containers.")
                    return False
                content_elements = raw_content
            else:
                self.warnings.append(
                    f"JSON object is missing standard Elementor importable wrapper keys: {sorted(list(missing_keys))}. "
                    "If importing via WordPress Admin (Templates -> Import), structure must be: {'version': '0.4', 'title': '...', 'type': 'page', 'content': [...]}"
                )
                if "content" in data and isinstance(data["content"], list):
                    content_elements = data["content"]
                else:
                    self.errors.append("Unrecognized Elementor dictionary structure: expected 'content' array or raw list of elements.")
                    return False

        elif isinstance(data, list):
            self.stats["is_importable_wrapper"] = False
            self.stats["template_type"] = "raw_elementor_data_array"
            self.warnings.append(
                "File contains a raw Elementor array (suitable for direct _elementor_data DB/REST postmeta), "
                "not the export/import JSON wrapper format with title/version/type."
            )
            content_elements = data
        else:
            self.errors.append(f"Root JSON must be an object or array, got {type(data).__name__}.")
            return False

        if not content_elements:
            self.warnings.append("Elementor content tree is empty.")

        # Walk the element tree
        for root_el in content_elements:
            self._walk_element(root_el, path="content")

        if self.duplicate_ids:
            self.errors.append(
                f"Duplicate element IDs found ({len(self.duplicate_ids)}): {list(self.duplicate_ids)[:10]}... "
                "Elementor requires strictly unique IDs for all elements."
            )

        # Calculate Editability Score
        total_widgets = self.stats["widgets"]
        html_widgets = self.stats["widget_breakdown"].get("html", 0)

        if total_widgets > 0:
            native_widgets = total_widgets - html_widgets
            score = (native_widgets / total_widgets) * 100.0
            self.stats["editability_score"] = round(score, 2)
            html_ratio = html_widgets / total_widgets

            if html_ratio > self.max_html_widget_ratio:
                self.warnings.append(
                    f"High HTML widget ratio ({round(html_ratio * 100, 1)}% of total widgets are 'html'). "
                    f"To ensure true CMS editability for the client, convert headings, paragraphs, buttons, "
                    f"and images into native Elementor widgets instead of raw HTML blocks."
                )
        else:
            self.stats["editability_score"] = 100.0

        return len(self.errors) == 0

    def _walk_element(self, el: Any, path: str):
        if not isinstance(el, dict):
            self.errors.append(f"Invalid element at '{path}': expected object, got {type(el).__name__}")
            return

        self.stats["total_elements"] += 1
        el_id = el.get("id")
        el_type = el.get("elType")

        if not el_id or not isinstance(el_id, str):
            self.errors.append(f"Element at '{path}' is missing a valid non-empty string 'id'.")
        else:
            if el_id in self.seen_ids:
                self.duplicate_ids.add(el_id)
            else:
                self.seen_ids.add(el_id)

        if not el_type or not isinstance(el_type, str):
            self.errors.append(f"Element '{el_id or path}' is missing valid 'elType'.")
        else:
            if el_type == "container":
                self.stats["containers"] += 1
            elif el_type == "section":
                self.stats["sections"] += 1
            elif el_type == "column":
                self.stats["columns"] += 1
            elif el_type == "widget":
                self.stats["widgets"] += 1
                widget_type = el.get("widgetType", "unknown")
                self.stats["widget_breakdown"][widget_type] = (
                    self.stats["widget_breakdown"].get(widget_type, 0) + 1
                )
            else:
                self.warnings.append(f"Uncommon elType '{el_type}' found at element '{el_id}'.")

        # Inspect settings
        settings = el.get("settings", {})
        if isinstance(settings, dict):
            custom_css = settings.get("custom_css", "")
            if custom_css and isinstance(custom_css, str):
                self.stats["custom_css_blocks"] += 1
                if "&gt;" in custom_css:
                    self.warnings.append(
                        f"Found '&gt;' entity in custom_css for element '{el_id}'. "
                        "Avoid direct child selector '>' in Elementor custom CSS to prevent entity encoding issues; "
                        "use descendant selector (space) instead."
                    )
        elif settings is not None:
            self.warnings.append(f"Element '{el_id}' settings should be a dictionary/object.")

        # Recurse children
        children = el.get("elements", [])
        if isinstance(children, list):
            for idx, child in enumerate(children):
                self._walk_element(child, path=f"{path}->{el_id or 'el'}[{idx}]")
        elif children is not None:
            self.errors.append(f"Child 'elements' of '{el_id}' must be an array.")

    def summary(self) -> str:
        status = "PASSED" if not self.errors else "FAILED"
        lines = [
            f"=== Elementor Template Validation Summary: {status} ===",
            f"File: {self.file_path}",
            f"Importable Wrapper: {'Yes' if self.stats['is_importable_wrapper'] else 'No (Raw Postmeta Array)'}",
            f"Template Type: {self.stats['template_type']} | Title: {self.stats['template_title']} | Version: {self.stats['version']}",
            f"Total Elements: {self.stats['total_elements']} (Containers: {self.stats['containers']}, Sections: {self.stats['sections']}, Columns: {self.stats['columns']}, Widgets: {self.stats['widgets']})",
            f"Editability Score: {self.stats['editability_score']}% native widgets",
            f"Custom CSS Blocks: {self.stats['custom_css_blocks']}"
        ]

        if self.stats["widget_breakdown"]:
            breakdown_str = ", ".join(f"{k}: {v}" for k, v in sorted(self.stats["widget_breakdown"].items()))
            lines.append(f"Widget Breakdown: {breakdown_str}")

        if self.errors:
            lines.append(f"\n[!] ERRORS ({len(self.errors)}):")
            for err in self.errors:
                lines.append(f"  - {err}")

        if self.warnings:
            lines.append(f"\n[*] WARNINGS ({len(self.warnings)}):")
            for warn in self.warnings:
                lines.append(f"  - {warn}")

        if not self.errors and not self.warnings:
            lines.append("\n[+] Verification successful: Perfectly formatted Elementor Template.")

        return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Validate Elementor JSON Template files for syntax, schema, and editability.")
    parser.add_argument("file", help="Path to Elementor JSON file")
    parser.add_argument("--json", action="store_true", help="Output results in JSON format")
    parser.add_argument("--threshold", type=float, default=0.20, help="Max ratio of HTML widgets allowed before warning (default 0.20)")
    args = parser.parse_args()

    validator = ElementorTemplateValidator(args.file, max_html_widget_ratio=args.threshold)
    is_valid = validator.validate()

    if args.json:
        output_payload = {
            "valid": is_valid,
            "errors": validator.errors,
            "warnings": validator.warnings,
            "stats": validator.stats
        }
        print(json.dumps(output_payload, indent=2))
    else:
        print(validator.summary())

    sys.exit(0 if is_valid else 1)

if __name__ == "__main__":
    main()
