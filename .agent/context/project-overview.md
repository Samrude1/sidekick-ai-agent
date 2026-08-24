# Project Overview: Sidekick AI Agent

## Mission & Purpose
Sidekick AI Agent is an enterprise-grade autonomous assistant and tech portfolio showcase. Unlike conversational chatbots (like raw ChatGPT) that deliver single-shot answers, Sidekick executes end-to-end multi-step missions with deterministic quality assurance via a self-correcting Evaluator-Optimizer loop.

## Target Audience & Use Cases
1. **Executive Leadership & CEOs:**
   - Autonomous competitive intelligence and pricing monitoring.
   - Comprehensive company background research and due diligence briefings.
   - Goal-oriented delegation with explicit *Success Criteria*.
2. **AI & Software Engineers:**
   - Multi-step web data extraction from dynamic, JavaScript-heavy websites without public APIs.
   - Data analysis and computational verification using isolated Python runtime.
   - Technical research and library/framework benchmarking.
3. **Portfolio Demonstrator:**
   - Production-grade demonstration of LangGraph multi-agent orchestration, AST security sandboxing, Playwright browser automation, and clean Gradio UI design.

## Key Capabilities
- **Autonomous Browsing:** Real-time web navigation, DOM parsing, and data scraping via Playwright headless Chromium.
- **Deep Search:** Multi-step query planning and search extraction using SerpAPI.
- **Sandboxed Code Execution:** Dynamic Python evaluation with AST security analysis and restricted builtins.
- **Factual Verification:** Wikipedia integration for instant ground-truth lookup.
- **Self-Correction (Evaluator-Optimizer):** Dual-agent verification where GPT-4o audits Claude Sonnet's output against defined success criteria before final delivery.
- **Smart Push Notifications:** Asynchronous Pushover alerts for long-running workflows.

## Deployment & Hosting
- **Target Platform:** Hugging Face Spaces / Docker / Local Python 3.13 environment.
- **Security Posture:** Hardened against SSRF, AST-level RCE, XSS, rate-limit exhaustion, and infinite recursion loops.
