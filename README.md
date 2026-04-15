---
title: Sidekick AI
emoji: 🚀
colorFrom: blue
colorTo: indigo
sdk: gradio
sdk_version: 5.20.0
python_version: 3.13
app_file: app.py
pinned: false
---

# Sidekick AI Agent (Gemini Edition)

Welcome to your personal AI Sidekick! Sidekick is a high-performance, standalone multi-agent system designed for autonomous task execution and research.

## 🚀 Overview
Sidekick is a multi-agent system built with **LangGraph** and **Gemini 2.5 Flash**. It uses a **Worker-Evaluator** pattern:
1. **Worker**: Uses tools (Browser, Search, Wikipedia, Python) to execute your task.
2. **Evaluator**: Reviews the Worker's output based on your specific success criteria.

## 🛠️ Setup

### Prerequisites

**Important:** This project requires **Python 3.13.x**. Python 3.14+ has compatibility issues with some LangChain dependencies (Pydantic V1).

**Check your Python version:**
```powershell
python --version
```

If you have Python 3.14, install Python 3.13 and use it explicitly:
```powershell
# Windows - use py launcher to specify version
py -3.13 -m venv .venv
```

### Step-by-Step Installation

#### 1. Environment Variables

Create a `.env` file **in the project root** (same folder as `app.py`) with:

```env
GOOGLE_API_KEY=your_google_api_key_here
SERPAPI_API_KEY=your_serpapi_key_here

# Optional (for push notifications)
PUSHOVER_TOKEN=your_pushover_token
PUSHOVER_USER=your_pushover_user
```

**Get API Keys:**
- Google API Key: https://aistudio.google.com/app/apikey
- SerpAPI Key: https://serpapi.com/

#### 2. Virtual Environment Setup

**Windows (PowerShell):**
```powershell
# Create environment with Python 3.13
python -m venv .venv

# Activate it
.\.venv\Scripts\activate

# Verify activation - you should see (.venv) in prompt
```

**Mac/Linux:**
```bash
# Create environment
python3 -m venv .venv

# Activate it
source .venv/bin/activate
```

#### 3. Install Dependencies

**With the environment activated:**

```bash
# Install all Python packages
pip install -r requirements.txt

# Install Playwright browsers (required for web browsing)
playwright install
```

**What gets installed:**
- `langgraph` - Multi-agent orchestration
- `langchain-google-genai` - Gemini integration
- `langchain-community` - Community tools (Browser, Wikipedia, etc.)
- `langchain-experimental` - Python REPL tool
- `gradio` - Web UI framework
- `playwright` - Headless browser automation
- `nest-asyncio` - Async loop compatibility (Windows)
- `python-dotenv` - Environment variable loading
- `google-search-results` - SerpAPI integration
- `wikipedia` - Wikipedia API wrapper

#### 4. Create Sandbox Directory

```bash
# Create directory for agent file operations
mkdir sandbox
```

## 🏃 Running the App

**From the project root:**
```powershell
# Make sure virtual environment is activated first!
.\.venv\Scripts\activate  # Windows
# source .venv/bin/activate  # Mac/Linux

# Run the app
python app.py
```

**Access the UI:**
Open your browser to http://127.0.0.1:7860

**Stop the app:**
Press `Ctrl+C` in the terminal

## 🏗️ Architecture
- `app.py`: Gradio interface.
- `sidekick.py`: LangGraph logic & Gemini integration.
- `sidekick_tools.py`: Tool definitions (Playwright, Search, etc.).
- `sandbox/`: Local directory for the agent to write/read files.
- `.env`: API keys and configuration (create this yourself).

## 🐛 Troubleshooting

### "ModuleNotFoundError: No module named 'X'"
**Solution:** Make sure virtual environment is activated and all dependencies are installed:
```bash
pip install -r requirements.txt
playwright install
```

### "TypeError: Chatbot.__init__() got an unexpected keyword argument 'type'"
**Solution:** You have an incompatible Gradio version. This should be fixed in the current code, but if you see it:
```bash
pip install --upgrade gradio
```

### "Pydantic V1 compatibility warning with Python 3.14"
**Solution:** Use Python 3.13.x instead:
```powershell
# Remove old venv
rmdir /s .venv

# Create new venv with Python 3.13
py -3.13 -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
```

### "API Key errors" or "Gemini not responding"
**Solution:** Check your `.env` file:
- Must be in the project root (same folder as `app.py`)
- Must contain valid `GOOGLE_API_KEY`
- No quotes around the key value

### Browser doesn't open or Playwright errors
**Solution:** Install Playwright browsers:
```bash
playwright install
```

### For more detailed problem documentation
See [TROUBLESHOOTING.md](docs/TROUBLESHOOTING.md) for a complete list of issues encountered during setup and their solutions.
