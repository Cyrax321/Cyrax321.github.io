# Anandhu P Shaji &mdash; Academic Portfolio

[![Validation Checks](https://github.com/Cyrax321/portfolio/actions/workflows/validate.yml/badge.svg)](https://github.com/Cyrax321/portfolio/actions/workflows/validate.yml)
[![Sync Activity](https://github.com/Cyrax321/portfolio/actions/workflows/update-github.yml/badge.svg)](https://github.com/Cyrax321/portfolio/actions/workflows/update-github.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

Personal academic and engineering portfolio of [Anandhu P Shaji](https://anandhupshaji.me), undergraduate researcher at GEC Idukki and final-year Computer Science student at College of Engineering Munnar.

Live URL: **[anandhupshaji.me](https://anandhupshaji.me)**

---

## Overview

A lightweight, typography-first academic website built with pure HTML5 and vanilla CSS. Designed for clarity, reading speed, and archival longevity:
- **Zero build steps:** Fast, native browser loading with no client-side JavaScript frameworks or runtime bundles.
- **Typography:** Typeset in [EB Garamond](https://fonts.google.com/specimen/EB+Garamond) with [Source Code Pro](https://fonts.google.com/specimen/Source+Code+Pro) for code blocks and tabular data.
- **Academic Aesthetic:** Inspired by minimalist scholar homepages with clean margins, responsive tables, and elegant link transitions.
- **Mobile Optimized:** Fluid layouts with touch-friendly navigation, readable tables, and contained code scroll areas.

---

## Directory Structure

```text
.
├── index.html                  # About, bio, and recent updates
├── research.html               # Publications, preprints, and research experience
├── code.html                   # Open-source projects (CONTINUUM, SNAGLINE) and TensorFlow PRs
├── activities.html             # Leadership (IEEE CS chair), outreach, and coursework
├── blog.html                   # Index of technical essays and research writeups
├── style.css                   # Core typography, responsive layout, and design system
├── CNAME                       # Custom domain routing (anandhupshaji.me)
├── sync_github.py              # Automated script fetching GitHub GraphQL activity to SVG
├── assets/
│   ├── photo.jpg               # Profile avatar
│   └── github_contributions.svg# Generated GitHub annual activity heatmap
├── posts/
│   └── tensorflow-stories.html # Technical breakdown of 24 TensorFlow pull requests
└── .github/
    └── workflows/
        └── update-github.yml   # Daily cron job updating contribution graph
```

---

## Automated GitHub Activity Sync

The repository includes a standalone Python utility (`sync_github.py`) that queries GitHub's GraphQL API and generates a lightweight SVG contribution calendar (`assets/github_contributions.svg`) styled to match the site's serif and monospace palette.

### Running locally
Using GitHub CLI (`gh`):
```bash
python3 sync_github.py
```

### GitHub Actions
A scheduled workflow runs daily via `.github/workflows/update-github.yml` to refresh the activity heatmap with zero manual maintenance.

---

## Local Development

Preview the site locally using any standard static server:

```bash
# Python 3
python3 -m http.server 8000

# or Node.js
npx serve .
```

Open `http://localhost:8000` in your browser.

---

## Contact

- **Email:** `reach.anandhu.me@gmail.com`
- **GitHub:** [@Cyrax321](https://github.com/Cyrax321)
- **LinkedIn:** [anandhupshaji](https://www.linkedin.com/in/anandhupshaji/)
- **Hugging Face:** [@Cyrax321](https://huggingface.co/Cyrax321)

---

## License

This project is licensed under the [MIT License](LICENSE).
