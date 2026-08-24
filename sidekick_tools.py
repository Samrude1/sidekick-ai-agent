from playwright.async_api import async_playwright
from langchain_community.agent_toolkits import PlayWrightBrowserToolkit
from dotenv import load_dotenv
import os
import requests
import ast
import io
import contextlib
import math
import statistics
import random
import datetime
import json
import re
import collections
import itertools
import ipaddress
import socket
import urllib.parse
from langchain_core.tools import Tool
from langchain_community.tools.wikipedia.tool import WikipediaQueryRun
from langchain_community.utilities import SerpAPIWrapper
from langchain_community.utilities.wikipedia import WikipediaAPIWrapper

# Load environment from root folder
load_dotenv(".env", override=True)

pushover_token = os.getenv("PUSHOVER_TOKEN")
pushover_user = os.getenv("PUSHOVER_USER")
pushover_url = "https://api.pushover.net/1/messages.json"

# Using SerpAPI (as per Lab 2 fix)
serp = SerpAPIWrapper()


def is_safe_url(url: str) -> tuple[bool, str]:
    """Validate URLs against SSRF, loopback, private networks, and cloud metadata endpoints."""
    try:
        url_str = url.strip()
        parsed = urllib.parse.urlparse(url_str)
        if parsed.scheme not in ("http", "https"):
            return False, f"Blocked: Protocol '{parsed.scheme}' is not permitted. Only 'http' and 'https' are allowed."
        
        hostname = parsed.hostname
        if not hostname:
            return False, "Blocked: Missing hostname in URL."
        
        hostname_lower = hostname.lower()
        if hostname_lower in ("localhost", "127.0.0.1", "0.0.0.0", "::1") or hostname_lower.endswith(".localhost") or hostname_lower.endswith(".local"):
            return False, f"Blocked: Navigation to local host '{hostname}' is forbidden for security."
        
        # Check IP literal or resolve hostname to IP
        try:
            ip_obj = ipaddress.ip_address(hostname_lower)
            ips = [ip_obj]
        except ValueError:
            try:
                addr_info = socket.getaddrinfo(hostname, None, socket.AF_UNSPEC, socket.SOCK_STREAM)
                ips = [ipaddress.ip_address(item[4][0]) for item in addr_info]
            except Exception as e:
                return False, f"Blocked: Unable to resolve hostname '{hostname}' ({e})."
        
        for ip in ips:
            if ip.is_loopback or ip.is_private or ip.is_link_local or ip.is_reserved or ip.is_unspecified:
                return False, f"Blocked: Target resolves to private/restricted IP address {ip}."
        
        return True, ""
    except Exception as e:
        return False, f"Blocked: Invalid URL format ({e})."


async def playwright_tools():
    playwright = await async_playwright().start()
    browser = await playwright.chromium.launch(headless=True)
    toolkit = PlayWrightBrowserToolkit.from_browser(async_browser=browser)
    tools = toolkit.get_tools()

    # Wrap navigation tools with SSRF validation
    for tool in tools:
        if tool.name == "navigate_browser":
            original_arun = tool._arun
            original_run = tool._run

            async def safe_navigate_arun(url: str, **kwargs):
                safe, reason = is_safe_url(url)
                if not safe:
                    return reason
                return await original_arun(url=url, **kwargs)

            def safe_navigate_run(url: str, **kwargs):
                safe, reason = is_safe_url(url)
                if not safe:
                    return reason
                return original_run(url=url, **kwargs)

            tool._arun = safe_navigate_arun
            tool._run = safe_navigate_run

    return tools, browser, playwright


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


ALLOWED_MODULES = {
    "math": math,
    "statistics": statistics,
    "random": random,
    "datetime": datetime,
    "json": json,
    "re": re,
    "collections": collections,
    "itertools": itertools,
}

def safe_import(name, globals=None, locals=None, fromlist=(), level=0):
    """Runtime import filter allowing only pre-approved safe modules."""
    root_mod = name.split(".")[0]
    if root_mod in ALLOWED_MODULES:
        return __import__(name, globals, locals, fromlist, level)
    raise ImportError(f"Importing '{name}' is forbidden for security. Allowed: {list(ALLOWED_MODULES.keys())}")

# Safe sandbox definitions for Python REPL
SAFE_BUILTINS = {
    "__import__": safe_import,
    "abs": abs,
    "all": all,
    "any": any,
    "bin": bin,
    "bool": bool,
    "chr": chr,
    "dict": dict,
    "divmod": divmod,
    "enumerate": enumerate,
    "filter": filter,
    "float": float,
    "format": format,
    "frozenset": frozenset,
    "hex": hex,
    "int": int,
    "isinstance": isinstance,
    "issubclass": issubclass,
    "iter": iter,
    "len": len,
    "list": list,
    "map": map,
    "max": max,
    "min": min,
    "next": next,
    "oct": oct,
    "ord": ord,
    "pow": pow,
    "print": print,
    "range": range,
    "repr": repr,
    "reversed": reversed,
    "round": round,
    "set": set,
    "slice": slice,
    "sorted": sorted,
    "str": str,
    "sum": sum,
    "tuple": tuple,
    "zip": zip,
}

BLOCKED_NAMES = {
    "open", "eval", "exec", "compile", "getattr", "setattr", "delattr", 
    "globals", "locals", "vars", "input", "breakpoint", "exit", "quit",
    "help", "memoryview", "super"
}


def validate_python_code_ast(code_str: str) -> tuple[bool, str]:
    """Perform AST validation to ensure the code does not use dangerous constructs or imports."""
    try:
        tree = ast.parse(code_str)
    except SyntaxError as e:
        return False, f"SyntaxError: {e}"

    for node in ast.walk(tree):
        # Block private/dunder attribute access (__class__, __subclasses__, __globals__, etc.)
        if isinstance(node, ast.Attribute):
            if node.attr.startswith("_"):
                return False, f"Security Error: Access to private/dunder attribute '{node.attr}' is forbidden."
        
        # Block dunder names and dangerous built-in identifiers
        if isinstance(node, ast.Name):
            if node.id.startswith("__") and node.id.endswith("__"):
                return False, f"Security Error: Access to special identifier '{node.id}' is forbidden."
            if node.id in BLOCKED_NAMES:
                return False, f"Security Error: Call or access to '{node.id}' is forbidden."
        
        # Block imports outside of the strict whitelist
        if isinstance(node, ast.Import):
            for alias in node.names:
                root_mod = alias.name.split(".")[0]
                if root_mod not in ALLOWED_MODULES:
                    return False, f"Security Error: Importing '{alias.name}' is forbidden. Allowed modules: {list(ALLOWED_MODULES.keys())}."
        
        if isinstance(node, ast.ImportFrom):
            if node.module:
                root_mod = node.module.split(".")[0]
                if root_mod not in ALLOWED_MODULES:
                    return False, f"Security Error: Importing from '{node.module}' is forbidden. Allowed modules: {list(ALLOWED_MODULES.keys())}."

    return True, ""


def run_safe_python_code(query: str) -> str:
    """Execute Python code in a secure restricted namespace with AST inspection."""
    code = query.strip()
    if code.startswith("```python"):
        code = code[len("```python"):].strip()
    elif code.startswith("```"):
        code = code[len("```"):].strip()
    if code.endswith("```"):
        code = code[:-3].strip()

    is_safe, error_msg = validate_python_code_ast(code)
    if not is_safe:
        return error_msg

    namespace = {
        "__builtins__": SAFE_BUILTINS,
        **ALLOWED_MODULES
    }

    buffer = io.StringIO()
    try:
        with contextlib.redirect_stdout(buffer):
            exec(code, namespace, namespace)
        output = buffer.getvalue()
        return output if output else "Code executed successfully (no output produced. Remember to use print() if you need to see a result)."
    except Exception as e:
        return f"Execution Error: {type(e).__name__}: {e}"


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

    python_repl = Tool(
        name="python_repl",
        func=run_safe_python_code,
        description="A sandboxed Python shell. Use this to execute mathematical calculations, algorithms, or data processing. "
                    "Input must be valid Python code. You must use print(...) to see output. "
                    "File system, OS, and network operations are disabled for security."
    )
    
    return [push_tool, tool_search, python_repl, wiki_tool]
