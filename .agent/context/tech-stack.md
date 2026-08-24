# Tech Stack: Sidekick AI Agent

## Core Runtime & Language
- **Python:** `3.13.x` (Recommended for LangChain / Pydantic V1 compatibility)

## Agent & LLM Frameworks
- **Orchestration:** `langgraph` (v0.2+)
- **LLM Integrations:** `langchain-openai`, `langchain-core`, `langchain-community`, `langchain-experimental`
- **Models Used via OpenRouter:**
  - **Worker Agent:** `anthropic/claude-3.5-haiku` (High-speed tool execution & multi-step browsing)
  - **Evaluator Agent:** `openai/gpt-4o-mini` (Fast structured success verification)
- **State Checkpointing:** `langgraph.checkpoint.memory.MemorySaver`

## User Interface & Presentation
- **Frontend / UI:** `gradio` (v5.27.0)
- **Typography:** Google Fonts (`Inter`, `JetBrains Mono`)
- **Rendering:** Custom sanitizing HTML logger with CSS animation stream and responsive enterprise theme

## Tooling & Automation
- **Browser Automation:** `playwright` (Chromium headless)
- **Search Engine:** `google-search-results` (SerpAPIWrapper)
- **Executive PDF Export:** `reportlab` (v5.x)
- **Excel Spreadsheet Export:** `openpyxl` (v3.1+), `pandas` (v3.x)
- **Encyclopedia Lookup:** `wikipedia`
- **Push Alerts:** `requests` -> Pushover API
- **Async Runtime:** `nest-asyncio`, `asyncio`

## Security & Sandboxing
- **Code AST Analysis:** Python standard library `ast` (custom whitelist visitor)
- **SSRF / IP Filtering:** `ipaddress`, `socket`, `urllib.parse`
- **Sanitization:** `html.escape`
- **Environment Management:** `python-dotenv` with memory-level key isolation
