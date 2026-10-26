# Contributing Guidelines

Thank you for your interest in contributing to Anandhu P Shaji's portfolio and open-source infrastructure.

## Development Workflow

1. **Fork & Branch**: Create a feature branch from `main`:
   ```bash
   git checkout -b feat/your-feature-name
   ```
2. **Typography & Styling**:
   - Keep layout minimal and pure HTML5/CSS3.
   - Do not introduce heavy frontend frameworks or build steps.
   - Maintain the EB Garamond serif aesthetic and responsive table patterns.
3. **Testing**:
   - Ensure tests pass prior to submitting changes:
     ```bash
     python3 -m unittest discover -s tests -v
     ```
   - If adding Python utilities or data sync scripts, include corresponding unit tests under `tests/`.
4. **Commit Conventions**:
   - Follow conventional commit style:
     - `feat(...)`: New pages, sections, or user-facing capabilities
     - `fix(...)`: Bug fixes or rendering corrections
     - `docs(...)`: Documentation and copy edits
     - `style(...)`: CSS and visual styling tweaks
     - `test(...)`: Unit and regression test additions
     - `chore(...)`: Tooling, workflow, and dependency updates

## Pull Requests

Submit pull requests against `main`. All pull requests trigger automated GitHub Actions checks (`.github/workflows/validate.yml`) for unit tests and XML schema validation.
