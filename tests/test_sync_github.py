#!/usr/bin/env python3
"""
Unit tests for sync_github.py SVG generation and color binning.
Runs with standard library unittest (no external dependencies required).
"""

import unittest
from sync_github import get_color, generate_svg

class TestSyncGitHub(unittest.TestCase):
    def test_get_color_thresholds(self):
        """Verify color hex values for various contribution volume bins."""
        self.assertEqual(get_color(0), "#eff1f5", "Zero contributions should be neutral background")
        self.assertEqual(get_color(1), "#9be9a8", "1 contribution should be light green")
        self.assertEqual(get_color(9), "#9be9a8", "9 contributions should be light green")
        self.assertEqual(get_color(10), "#40c463", "10 contributions should be medium green")
        self.assertEqual(get_color(29), "#40c463", "29 contributions should be medium green")
        self.assertEqual(get_color(30), "#30a14e", "30 contributions should be deep green")
        self.assertEqual(get_color(99), "#30a14e", "99 contributions should be deep green")
        self.assertEqual(get_color(100), "#216e39", "100+ contributions should be intense green")
        self.assertEqual(get_color(250), "#216e39", "High volume should be intense green")

    def test_generate_svg_structure(self):
        """Verify that generate_svg outputs well-formed SVG with labels and elements."""
        sample_calendar = {
            "totalContributions": 1420,
            "weeks": [
                {
                    "contributionDays": [
                        {"contributionCount": 0, "date": "2026-01-04", "weekday": 0},
                        {"contributionCount": 5, "date": "2026-01-05", "weekday": 1},
                        {"contributionCount": 12, "date": "2026-01-06", "weekday": 2},
                        {"contributionCount": 42, "date": "2026-01-07", "weekday": 3},
                        {"contributionCount": 105, "date": "2026-01-08", "weekday": 4},
                        {"contributionCount": 2, "date": "2026-01-09", "weekday": 5},
                        {"contributionCount": 0, "date": "2026-01-10", "weekday": 6},
                    ]
                }
            ]
        }
        svg = generate_svg(sample_calendar)
        self.assertTrue(svg.startswith('<svg xmlns="http://www.w3.org/2000/svg"'), "Should start with svg root element")
        self.assertTrue(svg.endswith('</svg>'), "Should end with svg closing tag")
        self.assertIn('1,420 contributions in the last year', svg, "Total contributions should be formatted with comma")
        self.assertIn('5 contributions on 2026-01-05', svg, "Tooltip should format plural contributions correctly")
        self.assertIn('105 contributions on 2026-01-08', svg, "Tooltip should reflect day count")
        self.assertIn('Mon', svg, "Weekday labels should include Mon")
        self.assertIn('Wed', svg, "Weekday labels should include Wed")
        self.assertIn('Fri', svg, "Weekday labels should include Fri")
        self.assertIn('Less', svg, "Legend should include Less")
        self.assertIn('More', svg, "Legend should include More")

if __name__ == "__main__":
    unittest.main()
