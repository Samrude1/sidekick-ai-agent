# VS Code Development Guide for Sidekick

**Last Updated:** February 2026  
**For:** Development version of the Sidekick multi-agent system

This guide assumes you're returning after a long break and need to get the development environment up and running quickly in VS Code.

---

## 🎯 Quick Start Checklist

Before you start development:

- [ ] Python 3.13.x installed (NOT 3.14+)
- [ ] VS Code installed
- [ ] PowerShell terminal available
- [ ] API keys ready (Google AI, SerpAPI)
- [ ] Git repository up to date

---

## 📁 Project Structure

```
sidekick/
├── .venv/                  # Virtual environment (create this)
├── .env                    # API keys (create this, see template below)
├── sandbox/                # Agent file operations directory
├── app.py                  # Gradio web UI
├── sidekick.py            # Core LangGraph agent logic
├── sidekick_tools.py      # Tool definitions
├── requirements.txt       # Python dependencies
├── README.md              # User setup guide
├── USAGE_GUIDE.md         # How to use Sidekick
├── TROUBLESHOOTING.md     # Common issues
├── VSCODE_DEV_GUIDE.md    # This file
└── GUIDE_FOR_AI.md        # Instructions for AI assistants
```

---

## 🛠️ VS Code Setup

### 1. Open Project in VS Code

```powershell
# Navigate to project
cd C:\Users\samru\DEVELOPER\PROJECTS\Assistant\sidekick

# Open in VS Code
code .
```

### 2. Recommended Extensions

Install these VS Code extensions for the best development experience:

**Essential:**
- **Python** (Microsoft) - Python language support
- **Pylance** (Microsoft) - Fast Python language server
- **Python Debugger** (Microsoft) - Debugging support

**Recommended:**
- **Better Comments** - Colorful comment highlighting
- **Error Lens** - Inline error display
- **GitLens** - Enhanced Git integration
- **Markdown All in One** - Markdown editing support
- **indent-rainbow** - Better indentation visibility

**Optional:**
- **Live Server** - For testing documentation HTML
- **TODO Highlight** - Highlight TODO comments

### 3. Python Interpreter Setup

**CRITICAL: Must use Python 3.13.x (NOT 3.14+)**

#### Check Python Version

```powershell
python --version
```

If you have Python 3.14, you must install 3.13 separately.

#### Create Virtual Environment

```powershell
# In the sidekick/ folder
python -m venv .venv

# Or if you have multiple Python versions:
py -3.13 -m venv .venv
```

#### Activate in VS Code Terminal

VS Code should auto-detect the `.venv` folder, but you can manually activate:

```powershell
# PowerShell (Windows)
.\.venv\Scripts\activate

# You should see (.venv) in your prompt
```

#### Select Python Interpreter in VS Code

1. Press `Ctrl+Shift+P`
2. Type "Python: Select Interpreter"
3. Choose `.venv\Scripts\python.exe`

**Verify selection:** Check bottom-right corner of VS Code - should show Python version with (.venv)

---

## 📦 Installing Dependencies

### 1. Install Python Packages

```powershell
# Make sure .venv is activated first!
pip install -r requirements.txt
```

**What gets installed:**
- `langgraph` - Multi-agent orchestration framework
- `langchain-google-genai` - Gemini 2.5 Flash integration
- `langchain-community` - Community tools (Browser, Wikipedia, etc.)
- `langchain-experimental` - Python REPL tool
- `gradio` - Web UI framework
- `playwright` - Headless browser automation
- `nest-asyncio` - Async loop compatibility (Windows)
- `python-dotenv` - Environment variable loading
- `google-search-results` - SerpAPI integration
- `wikipedia` - Wikipedia API wrapper

### 2. Install Playwright Browsers

```powershell
playwright install
```

This downloads Chromium, Firefox, and WebKit for browser automation.

### 3. Create Sandbox Directory

```powershell
# If it doesn't exist
mkdir sandbox
```

---

## 🔐 Environment Configuration

### Create `.env` File

Create a `.env` file **in the `sidekick/` directory** (same folder as `app.py`):

```env
# Required
GOOGLE_API_KEY=your_google_api_key_here
SERPAPI_API_KEY=your_serpapi_key_here

# Optional (for push notifications)
PUSHOVER_TOKEN=your_pushover_token
PUSHOVER_USER=your_pushover_user
```

**Get API Keys:**
- **Google AI Studio:** https://aistudio.google.com/app/apikey
- **SerpAPI:** https://serpapi.com/ (100 free searches/month)
- **Pushover (optional):** https://pushover.net/

**Important:**
- No quotes around values
- No spaces before/after the `=`
- Keep this file private (it's in `.gitignore`)

---

## 🚀 Running the Development Server

### Method 1: VS Code Terminal

```powershell
# Activate virtual environment (if not already)
.\.venv\Scripts\activate

# Run the app
python app.py
```

**Expected output:**
```
Running on local URL:  http://127.0.0.1:7860
```

The app should automatically open in your default browser.

### Method 2: VS Code Debugger (Recommended for Development)

1. Create `.vscode/launch.json`:

```json
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Python: Sidekick App",
            "type": "debugpy",
            "request": "launch",
            "program": "${workspaceFolder}/app.py",
            "console": "integratedTerminal",
            "justMyCode": false,
            "env": {
                "PYTHONPATH": "${workspaceFolder}"
            }
        }
    ]
}
```

2. Press `F5` or click **Run > Start Debugging**
3. Set breakpoints by clicking left of line numbers
4. Debug variables, step through code, etc.

### Method 3: VS Code Task (Quick Launch)

Create `.vscode/tasks.json`:

```json
{
    "version": "2.0.0",
    "tasks": [
        {
            "label": "Run Sidekick",
            "type": "shell",
            "command": "${workspaceFolder}/.venv/Scripts/python",
            "args": ["app.py"],
            "group": {
                "kind": "build",
                "isDefault": true
            },
            "presentation": {
                "reveal": "always",
                "panel": "new"
            },
            "problemMatcher": []
        }
    ]
}
```

Then press `Ctrl+Shift+B` to run.

---

## 🧪 Development Workflow

### Typical Development Session

1. **Open VS Code**
   ```powershell
   cd C:\Users\samru\DEVELOPER\PROJECTS\Assistant\sidekick
   code .
   ```

2. **Activate Virtual Environment**
   - VS Code should auto-activate
   - Or manually: `.\.venv\Scripts\activate`

3. **Check Python Interpreter**
   - Bottom-right should show: `Python 3.13.x (.venv)`

4. **Run the App**
   - Terminal: `python app.py`
   - Or press `F5` for debugging

5. **Make Changes**
   - Edit code in VS Code
   - Save files (`Ctrl+S`)

6. **Restart App** (to see changes)
   - Stop app: `Ctrl+C` in terminal
   - Restart: `python app.py`

7. **Test Changes**
   - Use web UI at http://127.0.0.1:7860
   - Monitor terminal for errors/logs

### Hot Reload (Gradio Feature)

Gradio supports automatic reloading when you save files:

```python
# In app.py, change the last line to:
if __name__ == "__main__":
    ui.launch(inbrowser=True, share=False, debug=True)
```

Changes to some components will auto-reload without restart.

---

## 🐛 Debugging Tips

### 1. Using VS Code Debugger

**Set Breakpoints:**
- Click left of line number
- Red dot appears
- Run with `F5`
- Execution pauses at breakpoints

**Debug Controls:**
- `F5` - Continue
- `F10` - Step Over
- `F11` - Step Into
- `Shift+F11` - Step Out
- `Shift+F5` - Stop

**Watch Variables:**
- Hover over variables to see values
- Use "Variables" panel in left sidebar
- Add watches in "Watch" panel

### 2. Print Debugging

```python
# Add strategic prints
print(f"DEBUG: Variable value = {variable}")
print(f"DEBUG: Type = {type(variable)}")

# Or use logging
import logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
logger.debug(f"Debugging info: {variable}")
```

### 3. Gradio Console

Check the Gradio web interface console for errors:
- Browser DevTools: `F12`
- Console tab shows JavaScript errors
- Network tab shows API calls

### 4. VS Code Problems Panel

- View > Problems (`Ctrl+Shift+M`)
- Shows Python linting errors
- Click to jump to error location

---

## 📝 Code Editing Best Practices

### 1. IntelliSense and Autocomplete

VS Code with Pylance provides:
- Auto-completion (`Ctrl+Space`)
- Parameter hints (`Ctrl+Shift+Space`)
- Quick documentation (hover)
- Go to definition (`F12`)
- Find all references (`Shift+F12`)

### 2. Code Navigation

```
Ctrl+P         Quick file open
Ctrl+Shift+O   Go to symbol in file
Ctrl+T         Go to symbol in workspace
F12            Go to definition
Alt+F12        Peek definition
Shift+F12      Find all references
Ctrl+F         Find in file
Ctrl+Shift+F   Find in all files
```

### 3. Refactoring

```
F2             Rename symbol
Ctrl+.         Quick fix / refactor
```

### 4. Multi-Cursor Editing

```
Alt+Click              Add cursor
Ctrl+Alt+Up/Down       Add cursor above/below
Ctrl+D                 Select next occurrence
Ctrl+Shift+L           Select all occurrences
```

---

## 🔧 Modifying the Agent

### Key Files to Understand

#### `app.py` - Gradio UI
- Web interface setup
- User input handling
- Session management

**Common modifications:**
- Change UI layout
- Add new input fields
- Customize theme/colors

#### `sidekick.py` - Core Agent Logic
- LangGraph state machine
- Worker and Evaluator agents
- Tool execution flow

**Common modifications:**
- Add new agents to the graph
- Modify agent prompts
- Change execution flow
- Add new tool integrations

#### `sidekick_tools.py` - Tool Definitions
- Tool implementations
- Custom tool creation
- Tool configuration

**Common modifications:**
- Add new custom tools
- Modify existing tool behavior
- Add tool-specific configuration

### Example: Adding a New Tool

1. **Define tool in `sidekick_tools.py`:**

```python
from langchain.tools import tool

@tool
def my_custom_tool(query: str) -> str:
    """Custom tool that does something useful.
    
    Args:
        query: The input query
        
    Returns:
        str: Result of the operation
    """
    # Your implementation here
    result = process_query(query)
    return result
```

2. **Register tool in `sidekick.py`:**

```python
from sidekick_tools import create_browser_tool, my_custom_tool

# In setup() method
self.tools = [
    create_browser_tool(),
    # ... other tools ...
    my_custom_tool,  # Add your tool
]
```

3. **Update Worker prompt** (in `sidekick.py`):

```python
WORKER_PROMPT = """You are a Worker agent with access to:
- Browser navigation
- Web search
- Wikipedia
- Python REPL
- File operations
- My Custom Tool  # Document it
...
"""
```

---

## 🧪 Testing Changes

### Manual Testing via UI

1. Start app: `python app.py`
2. Navigate to http://127.0.0.1:7860
3. Enter test task and success criteria
4. Click "Execute Task"
5. Monitor terminal for logs
6. Check `sandbox/` for generated files

### Testing Specific Components

Create a test script (e.g., `test_local.py`):

```python
import asyncio
from sidekick import Sidekick

async def test_sidekick():
    sk = Sidekick()
    await sk.setup()
    
    result = await sk.run_superstep(
        task="Test task here",
        success_criteria="Success criteria here",
        history=[]
    )
    
    print(result)
    sk.cleanup()

if __name__ == "__main__":
    asyncio.run(test_sidekick())
```

Run with: `python test_local.py`

### Checking API Connectivity

```python
# test_apis.py
import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()

# Test Gemini
llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash-exp")
response = llm.invoke("Say hello!")
print(f"Gemini response: {response.content}")

# Test SerpAPI
from langchain_community.utilities import SerpAPIWrapper
search = SerpAPIWrapper()
result = search.run("Python LangGraph")
print(f"Search result: {result}")
```

---

## 📊 Monitoring and Logs

### Terminal Output

The app prints detailed logs to the terminal:

```
Worker Agent Thinking...
[Tool: browser] Navigating to https://example.com
[Tool: search] Searching for "AI news"
Worker Result: ...

Evaluator Agent Reviewing...
Evaluator Decision: SUCCESS
```

### Redirect Logs to File

```powershell
# Run with output logging
python app.py 2>&1 | Tee-Object -FilePath "logs.txt"
```

### Add Structured Logging

```python
# In sidekick.py or app.py
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('sidekick.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)
```

---

## 🔄 Version Control (Git)

### Typical Git Workflow

```powershell
# Check status
git status

# Stage changes
git add .

# Commit with descriptive message
git commit -m "feat: Add custom weather tool"

# Push to remote
git push origin main
```

### Good Commit Messages

```
feat: Add new custom tool for weather data
fix: Resolve browser cleanup issue
docs: Update VS Code development guide
refactor: Simplify agent prompt structure
chore: Update dependencies
```

### Before Committing

1. **Check `.gitignore` includes:**
   ```
   .env
   .venv/
   __pycache__/
   sandbox/
   *.pyc
   .vscode/
   ```

2. **Don't commit:**
   - API keys (`.env`)
   - Virtual environment (`.venv/`)
   - Generated files (`sandbox/`)
   - IDE settings (`.vscode/`)

---

## 🚨 Common Issues & Solutions

### Issue 1: "ModuleNotFoundError"

**Symptom:** Import errors when running the app

**Solution:**
```powershell
# Check if venv is activated
# Should see (.venv) in prompt

# Reinstall dependencies
pip install -r requirements.txt
playwright install
```

### Issue 2: "Python Version Mismatch"

**Symptom:** Pydantic V1 warnings or compatibility errors

**Solution:**
```powershell
# Check version
python --version

# If 3.14+, recreate venv with 3.13
Remove-Item -Recurse -Force .venv
py -3.13 -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
```

### Issue 3: "VS Code Not Finding Interpreter"

**Symptom:** VS Code shows no Python interpreter or wrong one

**Solution:**
1. `Ctrl+Shift+P`
2. "Python: Select Interpreter"
3. Choose `.venv\Scripts\python.exe`
4. Restart VS Code if needed

### Issue 4: "Gradio Won't Start"

**Symptom:** App crashes on startup

**Solution:**
```powershell
# Update Gradio
pip install --upgrade gradio

# Check for port conflicts (if 7860 is in use)
# In app.py, change:
ui.launch(inbrowser=True, server_port=7861)
```

### Issue 5: "Playwright Browser Not Found"

**Symptom:** Browser tool fails with "Executable doesn't exist"

**Solution:**
```powershell
playwright install
```

### Issue 6: "API Key Not Found"

**Symptom:** "GOOGLE_API_KEY not set" or similar errors

**Solution:**
1. Check `.env` file exists in `sidekick/` folder
2. No quotes around values
3. No spaces: `GOOGLE_API_KEY=abc123`
4. Restart app after editing `.env`

---

## 📚 Additional Resources

### Documentation

- **LangGraph:** https://langchain-ai.github.io/langgraph/
- **LangChain:** https://python.langchain.com/docs/get_started/introduction
- **Gradio:** https://gradio.app/docs/
- **Playwright:** https://playwright.dev/python/
- **Gemini API:** https://ai.google.dev/docs

### Project Documentation

- `README.md` - User setup and quick start
- `USAGE_GUIDE.md` - How to use Sidekick effectively
- `TROUBLESHOOTING.md` - Common user issues
- `GUIDE_FOR_AI.md` - Instructions for AI coding assistants
- `EVOLUTION_STRATEGY.md` - Design philosophy and roadmap

### Learning Resources

**LangGraph Multi-Agent Systems:**
- DeepLearning.AI course on LangGraph
- LangGraph examples repository
- LangChain blog posts on agentic workflows

**Gradio UI Development:**
- Gradio documentation and tutorials
- Example apps in Gradio gallery

---

## 🎯 Quick Reference Commands

### Setup (One-time)

```powershell
# Create virtual environment
python -m venv .venv

# Activate
.\.venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
playwright install

# Create sandbox
mkdir sandbox

# Create .env file (use template above)
```

### Daily Development

```powershell
# Open project
cd C:\Users\samru\DEVELOPER\PROJECTS\Assistant\sidekick
code .

# Activate venv (if needed)
.\.venv\Scripts\activate

# Run app
python app.py

# Stop app
Ctrl+C
```

### Updating Dependencies

```powershell
# Update all packages
pip install --upgrade -r requirements.txt

# Update specific package
pip install --upgrade langgraph

# Reinstall Playwright browsers
playwright install
```

### When Returning After Long Break

1. **Pull latest changes:**
   ```powershell
   git pull origin main
   ```

2. **Check Python version:**
   ```powershell
   python --version  # Should be 3.13.x
   ```

3. **Recreate virtual environment if needed:**
   ```powershell
   Remove-Item -Recurse -Force .venv
   python -m venv .venv
   .\.venv\Scripts\activate
   ```

4. **Update dependencies:**
   ```powershell
   pip install --upgrade pip
   pip install -r requirements.txt
   playwright install
   ```

5. **Verify .env file:**
   - Check API keys are still valid
   - Update if expired

6. **Test run:**
   ```powershell
   python app.py
   ```

---

## 💡 Pro Tips

### 1. Use VS Code Workspace Settings

Create `.vscode/settings.json`:

```json
{
    "python.defaultInterpreterPath": "${workspaceFolder}/.venv/Scripts/python.exe",
    "python.terminal.activateEnvironment": true,
    "python.linting.enabled": true,
    "python.linting.pylintEnabled": false,
    "python.linting.flake8Enabled": true,
    "python.formatting.provider": "black",
    "editor.formatOnSave": true,
    "files.exclude": {
        "**/__pycache__": true,
        "**/*.pyc": true
    },
    "[python]": {
        "editor.defaultFormatter": "ms-python.black-formatter",
        "editor.formatOnSave": true,
        "editor.codeActionsOnSave": {
            "source.organizeImports": true
        }
    }
}
```

### 2. Use Code Snippets

Create `.vscode/python.code-snippets`:

```json
{
    "LangChain Tool": {
        "prefix": "lctool",
        "body": [
            "@tool",
            "def ${1:tool_name}(${2:param}: ${3:str}) -> ${4:str}:",
            "    \"\"\"${5:Tool description}",
            "    ",
            "    Args:",
            "        ${2:param}: ${6:Parameter description}",
            "        ",
            "    Returns:",
            "        ${4:str}: ${7:Return description}",
            "    \"\"\"",
            "    ${0:# Implementation}",
            "    return result"
        ],
        "description": "Create a LangChain tool"
    }
}
```

Then type `lctool` and press `Tab` for quick tool template.

### 3. Terminal Shortcuts

```powershell
# Create PowerShell alias for quick access
# Add to PowerShell profile:
notepad $PROFILE

# Add this line:
function sidekick { cd C:\Users\samru\DEVELOPER\PROJECTS\Assistant\sidekick; code . }

# Now just type: sidekick
```

### 4. Multiple Terminals

Use VS Code's split terminal feature:
- Terminal 1: Run the app
- Terminal 2: Run tests
- Terminal 3: Git commands

Split with `Ctrl+Shift+5` or click split icon in terminal.

### 5. Extension: REST Client

For testing API calls directly from VS Code:

Install "REST Client" extension, then create `test.http`:

```http
### Test Gemini API
POST https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash-exp:generateContent?key={{googleApiKey}}
Content-Type: application/json

{
  "contents": [{
    "parts": [{
      "text": "Hello, Gemini!"
    }]
  }]
}
```

---

## 🎓 Next Steps

Now that you have the dev environment set up:

1. **Familiarize yourself with the codebase:**
   - Read `USAGE_GUIDE.md` to understand what Sidekick can do
   - Review `sidekick.py` to understand the agent architecture
   - Check `EVOLUTION_STRATEGY.md` for design philosophy

2. **Make a simple change:**
   - Modify an agent prompt
   - Add a custom tool
   - Customize the Gradio UI

3. **Test thoroughly:**
   - Run the app and test your changes
   - Check logs for errors
   - Test edge cases

4. **Document your changes:**
   - Update relevant .md files
   - Add comments to code
   - Update README if needed

5. **Commit and push:**
   - Use descriptive commit messages
   - Keep commits focused and atomic

---

## 🤝 Getting Help

If you encounter issues:

1. **Check terminal output** for error messages
2. **Review `TROUBLESHOOTING.md`** for common issues
3. **Search GitHub issues** in LangChain/LangGraph repos
4. **Check VS Code Python extension** output panel
5. **Verify environment:** Python version, activated venv, API keys

---

**Happy coding! 🚀**

*Last updated: February 2026*
