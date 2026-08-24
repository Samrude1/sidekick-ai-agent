# Code Standards & Conventions: Sidekick AI Agent

## 1. Python Architecture & Style
- **Python Version:** Strict adherence to Python 3.13 syntax.
- **Type Annotations:** Full type hints on all public methods and coroutines (`async def func() -> ReturnType:`).
- **Asynchronous Design:**
  - All network, browser, and LLM calls must be non-blocking (`async` / `await`).
  - Playwright browser instances must always be closed cleanly in exception / cleanup handlers (`finally` / `free_resources`).
- **Modularity:**
  - `app.py`: UI, theming, session management only.
  - `sidekick.py`: LangGraph graph construction, state transitions, evaluator logic.
  - `sidekick_tools.py`: Tool definitions, validation, security sandboxes.

## 2. Security Standards
- **Zero Raw Execution:** Never use unvalidated `eval()`, `exec()`, or raw shell commands without AST validation and strict module whitelisting.
- **SSRF Prevention:** All URL inputs destined for Playwright browser automation must pass through `is_safe_url()`.
- **Output Sanitization:** Any dynamic LLM or user text rendered in HTML components must be escaped with `html.escape()`.
- **Secret Isolation:** Environment variables containing API keys must never be logged or rendered in the UI.

## 3. UI & Theming Conventions
- **Clean Enterprise Theme:** Inter typography, slate palette (`#111827`, `#374151`, `#f9fafb`, `#ffffff`, `#e5e7eb`).
- **High Contrast Rule:** Never use light gray font colors on light backgrounds; ensure WCAG AA contrast compliance.
- **No Boilerplate Footers:** Do not expose default Gradio footer links or debug interfaces in production UI.

## 4. Git & Version Control
- **Conventional Commits:** `feat:`, `fix:`, `docs:`, `refactor:`, `test:`, `chore:`.
- **Ignored Files:** Virtual environments (`.venv`), secrets (`.env`), cache files (`__pycache__`), Playwright profile caches.
