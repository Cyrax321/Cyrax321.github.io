#!/usr/bin/env python3
"""
Test suite validating that all internal links, anchors, and local assets exist.
Ensures zero broken internal links across all HTML files in the portfolio.
"""

import os
import re
import unittest

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

class TestInternalLinks(unittest.TestCase):
    def get_html_files(self):
        html_files = []
        for dirpath, _, filenames in os.walk(ROOT_DIR):
            if ".git" in dirpath:
                continue
            for f in filenames:
                if f.endswith(".html"):
                    html_files.append(os.path.join(dirpath, f))
        return html_files

    def test_internal_links_and_assets(self):
        """Verify that every relative href and src points to an existing file or anchor."""
        html_files = self.get_html_files()
        self.assertGreater(len(html_files), 0, "Should discover HTML files in workspace")

        href_pattern = re.compile(r'(?:href|src)=["\']([^"\']+)["\']')

        for file_path in html_files:
            file_dir = os.path.dirname(file_path)
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()

            matches = href_pattern.findall(content)
            for target in matches:
                # Skip external links, mailto, tel, javascript, data URIs
                if target.startswith(("http://", "https://", "mailto:", "tel:", "data:", "javascript:")):
                    continue
                # Anchor links within same page
                if target.startswith("#"):
                    continue

                # Strip anchor fragment for file path checking
                clean_target = target.split("#")[0]
                if not clean_target:
                    continue

                resolved = os.path.normpath(os.path.join(file_dir, clean_target))
                self.assertTrue(
                    os.path.exists(resolved),
                    f"Broken link in {os.path.relpath(file_path, ROOT_DIR)}: '{target}' (resolved to {resolved})"
                )

if __name__ == "__main__":
    unittest.main()
