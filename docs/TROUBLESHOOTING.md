# Setup Problems & Solutions

This document catalogs all issues encountered during initial project setup and their solutions. Use this as a reference for troubleshooting.

---

## Problem 1: Missing `python-dotenv` Dependency

**Error:**
```
ModuleNotFoundError: No module named 'dotenv'
```

**Root Cause:**
The `python-dotenv` package was not listed in the original installation instructions, but both `sidekick.py` and `sidekick_tools.py` import it via `from dotenv import load_dotenv`.

**Solution:**
- Added `python-dotenv` to `requirements.txt`
- Installed via: `pip install python-dotenv`

**Prevention:**
Always run `pip freeze > requirements.txt` after development to capture all dependencies.

---

## Problem 2: Missing `langchain-community` Dependency

**Error:**
```
ModuleNotFoundError: No module named 'langchain_community'
```

**Root Cause:**
`sidekick_tools.py` imports several tools from `langchain_community`:
- `PlayWrightBrowserToolkit`
- `FileManagementToolkit`
- `SerpAPIWrapper`
- `WikipediaAPIWrapper`

**Solution:**
- Added `langchain-community` to `requirements.txt`
- Installed via: `pip install langchain-community`

---

## Problem 3: Missing `langchain-experimental` Dependency

**Error:**
```
ModuleNotFoundError: No module named 'langchain_experimental'
```

**Root Cause:**
`sidekick_tools.py` imports `PythonREPLTool` from `langchain_experimental.tools`.

**Solution:**
- Added `langchain-experimental` to `requirements.txt`
- Installed via: `pip install langchain-experimental`

---

## Problem 4: Missing `google-search-results` (SerpAPI) Dependency

**Error:**
```
ModuleNotFoundError: No module named 'google-search-results'
```

**Root Cause:**
`SerpAPIWrapper` requires the `google-search-results` package to function.

**Solution:**
- Added `google-search-results` to `requirements.txt`
- Installed via: `pip install google-search-results`

**Note:**
Requires `SERPAPI_API_KEY` in `.env` file.

---

## Problem 5: Missing `wikipedia` Dependency

**Error:**
```
(Implicit error when WikipediaAPIWrapper tries to use the package)
```

**Root Cause:**
`WikipediaAPIWrapper` requires the `wikipedia` package.

**Solution:**
- Added `wikipedia` to `requirements.txt`
- Installed via: `pip install wikipedia`

---

## Problem 6: Incorrect `.env` File Path

**Error:**
```
(Silent failure - environment variables not loaded)
```

**Root Cause:**
Both `sidekick.py` and `sidekick_tools.py` had:
```python
load_dotenv("../.env", override=True)
```

This assumes `.env` is in the parent directory, which was incorrect for this project structure.

**Solution:**
Changed both files to:
```python
load_dotenv(".env", override=True)
```

**Files Modified:**
- `sidekick.py` (line 18)
- `sidekick_tools.py` (line 14)

---

## Problem 7: Gradio API Incompatibility

**Error:**
```
TypeError: Chatbot.__init__() got an unexpected keyword argument 'type'
```

**Root Cause:**
The code used `gr.Chatbot(type="messages")`, which was valid in Gradio 4.x but removed in Gradio 5.x+. The installed version was Gradio 6.5.1.

**Technical Details:**
- In Gradio 5+, `Chatbot` accepts `MessageDict` format by default
- The `type` parameter was removed from the API
- The code was written for an older Gradio version

**Solution:**
Removed the `type="messages"` argument from `app.py`:
```python
# Before:
chatbot = gr.Chatbot(label="Sidekick conversation", height=450, type="messages")

# After:
chatbot = gr.Chatbot(label="Sidekick conversation", height=450)
```

**File Modified:**
- `app.py` (line 37)

---

## Problem 8: Python 3.14 Compatibility Warning

**Warning:**
```
UserWarning: Core Pydantic V1 functionality isn't compatible with Python 3.14 or greater.
```

**Root Cause:**
Python 3.14.0 was installed in the virtual environment. Some LangChain dependencies still use Pydantic V1, which has compatibility issues with Python 3.14+.

**Current Status:**
- Warning appears but doesn't prevent execution
- Application runs successfully despite the warning

**Recommended Solution (for production):**
Use Python 3.13.x instead:
```powershell
# Create venv with Python 3.13
py -3.13 -m venv .venv
```

**Note:**
The user mentioned they had "huge problems with Python 3.14 and had to use older version 3.13" in previous projects. This is a known issue with the LangChain ecosystem.

---

## Summary of All Required Dependencies

The complete `requirements.txt` should include:

```
langgraph
langchain-google-genai
gradio
playwright
nest-asyncio
python-dotenv
langchain-community
langchain-experimental
google-search-results
wikipedia
```

Plus post-install step:
```bash
playwright install
```

---

## Lessons Learned

1. **Incomplete Dependency Documentation**: The original README only listed 5 packages, but 10 were actually required.

2. **Environment Path Assumptions**: Code assumed a specific directory structure that didn't match the actual project layout.

3. **Version Compatibility**: Gradio API changes between major versions broke the code silently.

4. **Python Version Sensitivity**: LangChain ecosystem has specific Python version requirements (3.13.x recommended).

5. **Hidden Dependencies**: Some packages (like `google-search-results` for SerpAPI) aren't obvious from the import statements.

---

## Debugging Methodology Used

1. **Iterative Error Resolution**: Fixed errors one at a time by running `python app.py` repeatedly.

2. **Debug Script**: Created `debug_setup.py` to isolate import and initialization issues.

3. **Version Inspection**: Used `pip show gradio` and Python introspection to understand API changes.

4. **Signature Analysis**: Used `inspect.signature()` to examine the actual Gradio Chatbot parameters.

This systematic approach helped identify all issues efficiently.
