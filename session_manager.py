import os
import shutil
import glob
from typing import List

BASE_REPORTS_DIR = os.path.join(os.path.dirname(__file__), "sandbox", "reports")


def ensure_base_dir() -> None:
    """Ensure base reports directory exists."""
    os.makedirs(BASE_REPORTS_DIR, exist_ok=True)


def get_session_dir(session_id: str) -> str:
    """Get or create the ephemeral directory for a specific session."""
    ensure_base_dir()
    # Sanitize session_id to prevent path traversal
    safe_session_id = "".join(c for c in session_id if c.isalnum() or c in "-_")
    session_dir = os.path.join(BASE_REPORTS_DIR, safe_session_id)
    os.makedirs(session_dir, exist_ok=True)
    return session_dir


def cleanup_session_dir(session_id: str) -> None:
    """Purge all ephemeral files generated during this browser session."""
    if not session_id:
        return
    safe_session_id = "".join(c for c in session_id if c.isalnum() or c in "-_")
    session_dir = os.path.join(BASE_REPORTS_DIR, safe_session_id)
    if os.path.exists(session_dir):
        try:
            shutil.rmtree(session_dir, ignore_errors=True)
            print(f"Purged ephemeral session artifacts for {safe_session_id}")
        except Exception as e:
            print(f"Error cleaning session artifacts: {e}")


def list_session_files(session_id: str) -> List[str]:
    """List all downloadable reports (.xlsx, .pdf, .csv, .json) created in this session."""
    if not session_id:
        return []
    safe_session_id = "".join(c for c in session_id if c.isalnum() or c in "-_")
    session_dir = os.path.join(BASE_REPORTS_DIR, safe_session_id)
    if not os.path.exists(session_dir):
        return []
    
    files = []
    for ext in ("*.xlsx", "*.pdf", "*.pptx", "*.csv", "*.json", "*.html"):
        files.extend(glob.glob(os.path.join(session_dir, ext)))
    return sorted(files, key=os.path.getmtime, reverse=True)


def cleanup_all_stale_sessions() -> None:
    """Clean up any leftover temporary session files on application startup."""
    ensure_base_dir()
    try:
        for item in os.listdir(BASE_REPORTS_DIR):
            item_path = os.path.join(BASE_REPORTS_DIR, item)
            if os.path.isdir(item_path):
                shutil.rmtree(item_path, ignore_errors=True)
    except Exception as e:
        print(f"Startup cleanup note: {e}")
