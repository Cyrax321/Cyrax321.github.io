#!/usr/bin/env python3
"""
Syncs GitHub contribution calendar and PR stats for Cyrax321.
Generates an SVG chart matching the site's typography and parsiad aesthetic.
Works both locally (using gh CLI) and in GitHub Actions (using GITHUB_TOKEN).
"""

import json
import os
import subprocess
import urllib.request
from datetime import datetime
from typing import Any, Dict, List, Optional

USERNAME = "Cyrax321"
GRAPHQL_QUERY = """
query($username: String!) {
  user(login: $username) {
    contributionsCollection {
      contributionCalendar {
        totalContributions
        weeks {
          contributionDays {
            contributionCount
            date
            weekday
          }
        }
      }
    }
  }
}
"""

def fetch_contributions_data(username: str = USERNAME, token: Optional[str] = None) -> Dict[str, Any]:
    """Fetch GitHub contribution calendar data using GraphQL API.
    
    Uses GITHUB_TOKEN if available; otherwise falls back to local gh CLI.
    """
    token = token or os.environ.get("GITHUB_TOKEN")
    if token:
        # Running in GitHub Actions or with GITHUB_TOKEN
        req = urllib.request.Request(
            "https://api.github.com/graphql",
            data=json.dumps({"query": GRAPHQL_QUERY, "variables": {"username": username}}).encode("utf-8"),
            headers={"Authorization": f"Bearer {token}", "User-Agent": "Portfolio-Sync"}
        )
        with urllib.request.urlopen(req) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            return data["data"]["user"]["contributionsCollection"]["contributionCalendar"]
    else:
        # Running locally with gh CLI
        cmd = [
            "gh", "api", "graphql",
            "-F", f"username={username}",
            "-f", f"query={GRAPHQL_QUERY}"
        ]
        res = subprocess.run(cmd, capture_output=True, text=True, check=True)
        data = json.loads(res.stdout)
        return data["data"]["user"]["contributionsCollection"]["contributionCalendar"]

def get_color(count: int) -> str:
    """Return hex fill color corresponding to daily contribution count."""
    if count == 0:
        return "#eff1f5"  # parsiad --code-bg neutral
    elif count < 10:
        return "#9be9a8"  # light green
    elif count < 30:
        return "#40c463"  # medium green
    elif count < 100:
        return "#30a14e"  # deep green
    else:
        return "#216e39"  # intense green

def generate_svg(calendar: Dict[str, Any]) -> str:
    """Generate SVG document representing contribution activity heatmap."""
    total: int = calendar["totalContributions"]
    weeks: List[Dict[str, Any]] = calendar["weeks"]
    
    # SVG Dimensions
    box_size = 10
    box_gap = 3
    col_width = box_size + box_gap
    row_height = box_size + box_gap
    
    left_padding = 28
    top_padding = 22
    
    num_weeks = len(weeks)
    svg_width = left_padding + (num_weeks * col_width) + 10
    svg_height = top_padding + (7 * row_height) + 26
    
    svg = []
    svg.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {svg_width} {svg_height}" width="100%" height="auto" class="github-chart">')
    svg.append('<style>')
    svg.append('  .month-label { font-family: "Source Code Pro", monospace; font-size: 10px; fill: #666; }')
    svg.append('  .day-label { font-family: "Source Code Pro", monospace; font-size: 9px; fill: #888; }')
    svg.append('  .stat-label { font-family: "EB Garamond", serif; font-size: 14px; fill: #1a1a1a; }')
    svg.append('  .legend-label { font-family: "Source Code Pro", monospace; font-size: 9px; fill: #888; }')
    svg.append('  .day-cell { rx: 2px; ry: 2px; stroke: rgba(0,0,0,0.04); stroke-width: 0.5px; transition: opacity 0.15s ease; }')
    svg.append('  .day-cell:hover { opacity: 0.8; stroke: #1a1a1a; stroke-width: 1px; }')
    svg.append('</style>')
    
    # Weekday labels (Mon, Wed, Fri)
    day_names = {1: "Mon", 3: "Wed", 5: "Fri"}
    for day_idx, name in day_names.items():
        y = top_padding + (day_idx * row_height) + 8
        svg.append(f'  <text x="2" y="{y}" class="day-label">{name}</text>')
    
    # Track months to draw month labels
    month_names = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    last_month = None
    
    # Cells
    for w_idx, week in enumerate(weeks):
        x = left_padding + (w_idx * col_width)
        first_day = week["contributionDays"][0]
        dt = datetime.strptime(first_day["date"], "%Y-%m-%d")
        current_month = dt.month
        
        # Month header
        if current_month != last_month and w_idx < num_weeks - 2:
            month_label = month_names[current_month - 1]
            svg.append(f'  <text x="{x}" y="{top_padding - 7}" class="month-label">{month_label}</text>')
            last_month = current_month
            
        for day in week["contributionDays"]:
            weekday = day["weekday"]
            count = day["contributionCount"]
            date = day["date"]
            color = get_color(count)
            y = top_padding + (weekday * row_height)
            
            tooltip = f"{count} contribution{'s' if count != 1 else ''} on {date}"
            svg.append(f'  <rect class="day-cell" x="{x}" y="{y}" width="{box_size}" height="{box_size}" fill="{color}">')
            svg.append(f'    <title>{tooltip}</title>')
            svg.append('  </rect>')
    
    # Footer stats and legend
    footer_y = top_padding + (7 * row_height) + 18
    formatted_total = f"{total:,}"
    svg.append(f'  <text x="{left_padding}" y="{footer_y}" class="stat-label">{formatted_total} contributions in the last year</text>')
    
    # Legend on right
    legend_right_x = left_padding + (num_weeks * col_width)
    legend_colors = ["#eff1f5", "#9be9a8", "#40c463", "#30a14e", "#216e39"]
    legend_start_x = legend_right_x - (len(legend_colors) * 12) - 36
    
    svg.append(f'  <text x="{legend_start_x}" y="{footer_y}" class="legend-label">Less</text>')
    for l_idx, l_color in enumerate(legend_colors):
        lx = legend_start_x + 28 + (l_idx * 12)
        ly = footer_y - 8
        svg.append(f'  <rect x="{lx}" y="{ly}" width="9" height="9" rx="1.5" fill="{l_color}" stroke="rgba(0,0,0,0.04)" stroke-width="0.5px" />')
    svg.append(f'  <text x="{legend_start_x + 28 + (len(legend_colors) * 12) + 6}" y="{footer_y}" class="legend-label">More</text>')
    
    svg.append('</svg>')
    return "\n".join(svg)

def main() -> None:
    """CLI entry point for syncing GitHub contributions."""
    import argparse
    parser = argparse.ArgumentParser(description="Fetch and render GitHub contribution graph to SVG.")
    parser.add_argument("--username", "-u", default=USERNAME, help=f"GitHub username (default: {USERNAME})")
    parser.add_argument("--output", "-o", default="assets/github_contributions.svg", help="Output path for SVG file")
    parser.add_argument("--token", "-t", default=None, help="GitHub Personal Access Token (defaults to GITHUB_TOKEN env var)")
    parser.add_argument("--dry-run", action="store_true", help="Fetch and render without writing to file")
    args = parser.parse_args()

    print(f"Fetching GitHub contribution calendar for @{args.username}...")
    calendar = fetch_contributions_data(username=args.username, token=args.token)
    total = calendar["totalContributions"]
    print(f"Successfully fetched {total:,} contributions.")
    
    svg_content = generate_svg(calendar)
    
    if args.dry_run:
        print(f"Dry run complete. SVG size: {len(svg_content)} bytes (not written).")
        return

    output_dir = os.path.dirname(args.output)
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)
    with open(args.output, "w", encoding="utf-8") as f:
        f.write(svg_content)
    print(f"Generated {args.output}")

if __name__ == "__main__":
    main()
