# AI Agent Technical Brief: Sidekick Project

This document is for AI agents working on this codebase.
Current year is 2026.

## Core Tech Stack
- **Framework**: LangGraph (StateGraph)
- **Model**: Gemini 2.5 Flash (`ChatGoogleGenerativeAI`)
- **Interface**: Gradio (Chatbot with `messages` type)
- **Tools**: Playwright (Browser), SerpApi (Search), PythonREPL, FileManagement.

## Critical Patterns
1. **Text Extraction**: Gemini 2026 responses often include metadata dictionaries or lists. Always use the `extract_text()` helper found in `sidekick.py` before sending content to Gradio or Loggers to avoid `OSError [Errno 22]`.
2. **State Management**: The graph uses `TypedDict` and `MemorySaver`. Reducer `add_messages` is used for the conversation history.
3. **Loop Control**: The `evaluator` node is the gatekeeper. It must return `success_criteria_met=True` or `user_input_needed=True` to terminate the loop.
4. **Environment**: `.env` is loaded from `../.env` by default.

## Deployment Notes
- Windows requires `nest_asyncio.apply()` because of loop policy conflicts between Playwright and Jupyter/Gradio.
- Playwright is running in `headless=False` mode currently; change in `sidekick_tools.py` for cloud deployment.
