# Contributing to nodetect

Thank you for your interest in contributing to **nodetect**! We welcome bug fixes, new evasion patches, fingerprint presets, and documentation improvements.

---

## Development Setup

1. **Fork and Clone the Repository:**
   ```bash
   git clone https://github.com/sudoxdev/nodetect.git
   cd nodetect
   ```

2. **Create a Virtual Environment:**
   ```bash
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On Linux / macOS:
   source venv/bin/activate
   ```

3. **Install Dependencies & Editable Package:**
   ```bash
   pip install -e .
   pip install pytest
   playwright install chromium
   ```

---

## Running Test Suite

Before submitting any Pull Request, ensure all automated tests pass:

```bash
pytest -v tests/
```

To run a headless detection benchmark against live Blink evasion checks:
```bash
nodetect test --headless
```

---

## Pull Request Guidelines

1. **Branch Naming:**
   - Feature: `feat/your-feature-name`
   - Bugfix: `fix/bug-description`
   - Docs: `docs/documentation-update`

2. **Commit Message Format:**
   Follow conventional commits:
   - `feat: add Akamai sensor_data evasion generator`
   - `fix: resolve WebRTC SDP candidate parsing edge case`
   - `docs: update quickstart guide`

3. **Submitting PR:**
   - Push your branch to your fork.
   - Open a Pull Request against `main`.
   - Provide a clear summary of changes and test results.

---

## AI Pair Programming & Co-Authorship

If you use AI assistance (such as Claude) during development, follow the standard Git trailer convention:

```bash
git commit -m "feat: your feature summary

Co-authored-by: Claude <noreply@anthropic.com>"
```

