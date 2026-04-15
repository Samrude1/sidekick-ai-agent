---
description: Complete workflow for developing, testing, and debugging the Sidekick multi-agent system
---

# Sidekick Multi-Agent Development Workflow

This workflow guides you through the complete development cycle for the Sidekick multi-agent system, from initial setup to debugging production issues.

---

## 🚀 Initial Setup (First Time Only)

### 1. Verify Python Version
**CRITICAL:** Use Python 3.13.x (NOT 3.14+)

```powershell
python --version
```

If you have Python 3.14, use the py launcher:
```powershell
py -3.13 --version
```

### 2. Create Virtual Environment
```powershell
# Navigate to sidekick directory
cd c:\Users\samru\DEVELOPER\PROJECTS\Assistant\sidekick

# Create venv with Python 3.13
python -m venv .venv
# OR if you have 3.14: py -3.13 -m venv .venv
```

### 3. Activate Virtual Environment
```powershell
.\.venv\Scripts\activate
```

You should see `(.venv)` in your prompt.

// turbo
### 4. Install All Dependencies
```powershell
pip install -r requirements.txt
```

// turbo
### 5. Install Playwright Browsers
```powershell
playwright install
```

// turbo
### 6. Create Sandbox Directory
```powershell
mkdir sandbox
```

### 7. Configure Environment Variables
Create `.env` file in the `sidekick/` directory:

```env
GOOGLE_API_KEY=your_key_here
SERPAPI_API_KEY=your_key_here
PUSHOVER_TOKEN=optional
PUSHOVER_USER=optional
```

**Get API Keys:**
- Google: https://aistudio.google.com/app/apikey
- SerpAPI: https://serpapi.com/

---

## 🔄 Daily Development Workflow

### 1. Start Development Session
```powershell
# Navigate to project
cd c:\Users\samru\DEVELOPER\PROJECTS\Assistant\sidekick

# Activate environment
.\.venv\Scripts\activate

# Verify activation
python --version
```

### 2. Update Dependencies (if requirements.txt changed)
```powershell
pip install -r requirements.txt
```

### 3. Run the Application
```powershell
python app.py
```

**Expected Output:**
- `Running on local URL: http://127.0.0.1:7860`
- Browser should open automatically
- No error messages in console

### 4. Stop the Application
Press `Ctrl+C` in the terminal

---

## 🧪 Testing Workflow

### Test 1: Environment Validation
Run this before making changes:

```powershell
python -c "from dotenv import load_dotenv; import os; load_dotenv('.env'); print('GOOGLE_API_KEY:', 'SET' if os.getenv('GOOGLE_API_KEY') else 'MISSING'); print('SERPAPI_API_KEY:', 'SET' if os.getenv('SERPAPI_API_KEY') else 'MISSING')"
```

### Test 2: Import Validation
Test all critical imports:

```powershell
python -c "from sidekick import Sidekick; from sidekick_tools import playwright_tools, other_tools; print('All imports successful')"
```

### Test 3: LLM Connection Test
Test Gemini API connection:

```powershell
python -c "from langchain_google_genai import ChatGoogleGenerativeAI; from dotenv import load_dotenv; load_dotenv('.env'); llm = ChatGoogleGenerativeAI(model='gemini-2.5-flash'); print('LLM initialized:', llm.invoke('Hello').content[:50])"
```

### Test 4: Full Application Test
1. Start app: `python app.py`
2. Open http://127.0.0.1:7860
3. Test simple task: "What is 2+2?"
4. Verify response appears
5. Check console for errors

### Test 5: Tool Integration Test
Test a task that uses tools:
- **Search Test**: "Search for the current weather in Helsinki"
- **Browser Test**: "Navigate to example.com and tell me what you see"
- **Python Test**: "Calculate the factorial of 5 using Python"
- **File Test**: "Create a file called test.txt with 'Hello World'"

---

## 🐛 Debugging Workflow

### Debug Level 1: Quick Checks

**Check 1: Virtual Environment Active?**
```powershell
# Should show path inside .venv
where python
```

**Check 2: Dependencies Installed?**
```powershell
pip list | Select-String "langgraph|gradio|playwright"
```

**Check 3: Environment Variables Loaded?**
```powershell
python -c "from dotenv import load_dotenv; import os; load_dotenv('.env'); print(os.getenv('GOOGLE_API_KEY')[:10] if os.getenv('GOOGLE_API_KEY') else 'NOT FOUND')"
```

### Debug Level 2: Module Import Issues

**Create debug script:**
```powershell
# Create debug_imports.py
@"
import sys
print(f'Python: {sys.version}')

modules = [
    'dotenv',
    'langgraph',
    'langchain_google_genai',
    'langchain_community',
    'langchain_experimental',
    'gradio',
    'playwright',
]

for module in modules:
    try:
        __import__(module)
        print(f'✓ {module}')
    except ImportError as e:
        print(f'✗ {module}: {e}')
"@ | Out-File -Encoding utf8 debug_imports.py

python debug_imports.py
```

**If any module fails:**
```powershell
pip install <missing-module>
```

### Debug Level 3: Application Errors

**Enable verbose logging:**
Edit `sidekick.py` and add at the top:
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

**Run with error output:**
```powershell
python app.py 2>&1 | Tee-Object -FilePath debug_log.txt
```

**Common errors and fixes:**

1. **"ModuleNotFoundError"**
   - Solution: `pip install -r requirements.txt`

2. **"Chatbot.__init__() got unexpected keyword"**
   - Solution: Check `app.py` line 37, ensure no `type="messages"`

3. **"API Key not found"**
   - Solution: Check `.env` file location (must be in `sidekick/` folder)

4. **"Playwright browser not found"**
   - Solution: `playwright install`

5. **"Pydantic V1 compatibility warning"**
   - Solution: Use Python 3.13.x instead of 3.14+

### Debug Level 4: Agent Behavior Issues

**Enable LangGraph debugging:**
```python
# In sidekick.py, before graph.compile():
from langgraph.graph import StateGraph
import os
os.environ["LANGCHAIN_TRACING_V2"] = "true"
```

**Test individual nodes:**
```powershell
python -c "from sidekick import Sidekick; import asyncio; sk = Sidekick(); asyncio.run(sk.setup()); print('Setup successful')"
```

**Inspect graph structure:**
```python
# Add to sidekick.py after graph compilation
print(self.graph.get_graph().draw_ascii())
```

---

## 🔧 Adding New Agents/Tools

### 1. Create New Tool

**In `sidekick_tools.py`:**
```python
def my_new_tool(input: str) -> str:
    \"\"\"Description of what this tool does\"\"\"
    # Your implementation
    return result

# Add to other_tools() function:
new_tool = Tool(
    name="my_tool_name",
    func=my_new_tool,
    description="When to use this tool"
)
return list(file_tools) + [push_tool, tool_search, python_repl, wiki_tool, new_tool]
```

### 2. Test New Tool Independently
```powershell
python -c "from sidekick_tools import my_new_tool; print(my_new_tool('test input'))"
```

### 3. Test Tool in Agent
```powershell
python app.py
# In UI: "Use my_tool_name to process 'test data'"
```

### 4. Add New Agent Node

**In `sidekick.py`:**
```python
def my_new_agent(self, state: State) -> Dict[str, Any]:
    \"\"\"New agent logic\"\"\"
    # Implementation
    return {"messages": [response]}

# In build_graph():
graph_builder.add_node("my_agent", self.my_new_agent)
graph_builder.add_edge("worker", "my_agent")
```

### 5. Update Dependencies
```powershell
# After adding new imports
pip freeze > requirements.txt
```

---

## 📊 Performance Monitoring

### Monitor Token Usage
```python
# Add to sidekick.py
import time
start = time.time()
result = llm.invoke(messages)
print(f"LLM call took {time.time() - start:.2f}s")
```

### Monitor Memory Usage
```powershell
# While app is running
python -c "import psutil; import os; p = psutil.Process(os.getpid()); print(f'Memory: {p.memory_info().rss / 1024 / 1024:.2f} MB')"
```

---

## 🚢 Pre-Deployment Checklist

- [ ] All tests pass
- [ ] No console errors when running
- [ ] `.env` file not committed to git
- [ ] `requirements.txt` is up to date
- [ ] README.md reflects current setup
- [ ] Python 3.13.x specified in documentation
- [ ] All API keys are valid
- [ ] Playwright browsers installed
- [ ] Sandbox directory exists

---

## 🆘 Emergency Fixes

### Nuclear Option: Complete Reset
```powershell
# Stop app (Ctrl+C)

# Remove virtual environment
deactivate
Remove-Item -Recurse -Force .venv

# Recreate from scratch
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
playwright install

# Test
python app.py
```

### Dependency Conflict Resolution
```powershell
# Clear pip cache
pip cache purge

# Reinstall everything
pip uninstall -y -r requirements.txt
pip install -r requirements.txt
```

---

## 📝 Development Notes

### File Structure
```
sidekick/
├── .env                    # API keys (DO NOT COMMIT)
├── .venv/                  # Virtual environment
├── app.py                  # Gradio UI
├── sidekick.py            # Main agent logic
├── sidekick_tools.py      # Tool definitions
├── requirements.txt        # Dependencies
├── sandbox/               # Agent workspace
├── README.md              # User documentation
└── TROUBLESHOOTING.md     # Problem solutions
```

### Key Configuration Points
- **Python Version**: Line 1 of this workflow
- **Environment Loading**: `sidekick.py` line 18, `sidekick_tools.py` line 14
- **Gradio Chatbot**: `app.py` line 37 (no `type` argument)
- **LLM Model**: `sidekick.py` line 71, 75 (`gemini-2.5-flash`)

### When Adding Dependencies
1. Install: `pip install <package>`
2. Test: `python -c "import <package>"`
3. Update: `pip freeze > requirements.txt`
4. Document: Update README.md if user-facing

---

## 🎯 Quick Reference Commands

```powershell
# Activate environment
.\.venv\Scripts\activate

# Run app
python app.py

# Test imports
python -c "from sidekick import Sidekick; print('OK')"

# Check dependencies
pip list

# Update dependencies
pip install -r requirements.txt

# Reinstall Playwright
playwright install

# Check Python version
python --version

# Deactivate environment
deactivate
```
