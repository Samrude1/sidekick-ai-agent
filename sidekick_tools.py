from playwright.async_api import async_playwright
from langchain_community.agent_toolkits import PlayWrightBrowserToolkit
from dotenv import load_dotenv
import os
import requests
from langchain_core.tools import Tool
from langchain_community.tools.wikipedia.tool import WikipediaQueryRun
from langchain_experimental.tools import PythonREPLTool
from langchain_community.utilities import SerpAPIWrapper
from langchain_community.utilities.wikipedia import WikipediaAPIWrapper

# Load environment from root folder
load_dotenv(".env", override=True)

pushover_token = os.getenv("PUSHOVER_TOKEN")
pushover_user = os.getenv("PUSHOVER_USER")
pushover_url = "https://api.pushover.net/1/messages.json"

# Using SerpAPI (as per Lab 2 fix)
serp = SerpAPIWrapper()

async def playwright_tools():
    playwright = await async_playwright().start()
    browser = await playwright.chromium.launch(headless=True)
    toolkit = PlayWrightBrowserToolkit.from_browser(async_browser=browser)
    return toolkit.get_tools(), browser, playwright


push_count = 0

def push(text: str):
    """Send a push notification to the user"""
    global push_count
    if push_count >= 2:
        return "Push limit reached for this session."
    push_count += 1
    # Note: If Pushover trial is expired, this will log but not buzz
    requests.post(pushover_url, data = {"token": pushover_token, "user": pushover_user, "message": text})
    return "success"


async def other_tools():
    push_tool = Tool(
        name="send_push_notification", 
        func=push, 
        description="Use this tool when you want to send a push notification"
    )
    
    tool_search = Tool(
        name="search",
        func=serp.run,
        description="Use this tool when you want to get the results of an online web search"
    )

    wikipedia = WikipediaAPIWrapper()
    wiki_tool = WikipediaQueryRun(api_wrapper=wikipedia)

    class SafePythonREPLTool(PythonREPLTool):
        def _run(self, query: str, **kwargs) -> str:
            forbidden_imports = ["import os", "from os", "import sys", "from sys", "import subprocess", "from subprocess"]
            if any(bad in query for bad in forbidden_imports):
                return "Error: For security reasons, importing os, sys, or subprocess is not allowed."
            return super()._run(query, **kwargs)

    python_repl = SafePythonREPLTool()
    
    return [push_tool, tool_search, python_repl, wiki_tool]
