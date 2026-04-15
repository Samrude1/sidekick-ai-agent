# Hugging Face Spaces Deployment Troubleshooting Guide

This guide summarizes the critical fixes and best practices discovered during the deployment of Sidekick AI. Use these solutions when deploying other multi-agent or Gradio-based projects to HF Spaces.

## 1. GitHub Action Sync Issues
**Error:** `Unable to resolve action huggingface/hub-sync@v1.0`
- **Solution:** Use the correct version tag: `huggingface/hub-sync@v0.1.0`.
- **Reference:** Ensure `HF_TOKEN` (Write access) is added to GitHub Repository Secrets.

## 2. README.md Metadata (Frontmatter)
**Error:** `Configuration error: Missing configuration in README`
- **Solution:** Add YAML metadata to the VERY top of `README.md`:
  ```yaml
  ---
  title: Project Name
  emoji: 🚀
  colorFrom: blue
  colorTo: indigo
  sdk: gradio
  sdk_version: 5.20.0
  python_version: 3.13
  app_file: app.py
  pinned: false
  ---
  ```
- **Constraint:** `colorTo` and `colorFrom` must be one of: `red, yellow, green, blue, indigo, purple, pink, gray`.

## 3. Version Compatibility (Gradio & huggingface_hub)
**Error:** `ImportError: cannot import name 'HfFolder' from 'huggingface_hub'`
- **Reason:** `huggingface_hub v1.0.0+` removed deprecated classes used by older Gradio versions.
- **Solution:** Set `sdk_version: 5.20.0` (or higher) in `README.md`.

## 4. Playwright (Headless Browser) on HF
**Error:** Agent fails to start the browser or crashes on startup.
- **Solution A (Headless):** Set `headless=True` in your Python code:
  ```python
  browser = await playwright.chromium.launch(headless=True)
  ```
- **Solution B (System Deps):** Create a `packages.txt` in the root folder to install Linux libraries:
  ```text
  libnss3
  libatk-bridge2.0-0
  libcups2
  libdrm2
  libxkbcommon0
  libxcomposite1
  libxdamage1
  libxfixes3
  libxrandr2
  libgbm1
  libasound2
  ```
- **Solution C (Auto-install):** Add this to your `app.py` start logic:
  ```python
  if os.environ.get("SPACE_ID"):
      os.system("playwright install chromium")
  ```

## 5. Gradio UI Bugs
**Error:** `TypeError: argument of type 'bool' is not iterable` (during `get_api_info`)
- **Reason:** A bug in Gradio 5.x schema parsing when using Boolean outputs.
- **Solution:** Disable API name generation for events:
  ```python
  btn.click(fn, inputs, outputs, api_name=False)
  ```

**Error:** `Data incompatible with tuples format`
- **Solution:** Force the modern message format in `gr.Chatbot`:
  ```python
  chatbot = gr.Chatbot(..., type="messages")
  ```

## 6. Anti-Spam & Cost Control
When hosting publicly without a password:
- **Concurrency:** Use `ui.queue(default_concurrency_limit=2, max_size=10).launch(...)` to limit simultaneous users.
- **Recursion:** Set a hard limit on agent loops in LangGraph:
  ```python
  # Sidekick usage:
  config = {"recursion_limit": 8}
  result = await graph.ainvoke(state, config=config)
  ```

## 7. The "Vertical Stripe" UI Cancer (Gradio 5)
**Error:** Persistent grey vertical lines (pinstripes) appearing next to chat messages that cannot be removed with standard CSS `border: none`.
- **Reason:** In Gradio 5's `type="messages"` layout, these lines are often rendered as **separate physical div elements** with background colors or **pseudo-elements (`::before`)** with background colors, rather than standard borders.
- **The "Pakkokeino" (Forced Measure):** Abandon the unstable `gr.Chatbot` component entirely and replace it with a custom-engineered `gr.HTML` log system.
- **Why it works:** By rendering the conversation manually using raw HTML/CSS, you gain 100% control over the DOM. This eliminates the "syöpä" (Gradio artifact cancer) and is the only guaranteed way to achieve a professional, zero-artifact "Enterprise Edition" UI.
- **Implementation:**
  1. Return conversation logs as a single HTML string from the backend.
  2. Display them in `gr.HTML(elem_id="log-window")`.
  3. Use CSS to style the logs (e.g., `JetBrains Mono` for a professional feel).
