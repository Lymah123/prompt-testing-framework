from datetime import datetime
import re

def format_timestamp(timestamp_str: str) -> str:
    """Format ISO timestamp to readable string"""
    try:
        dt = datetime.fromisoformat(timestamp_str)
        return dt.strftime("%Y-%m-%d %H:%M:%S")
    except:
        return timestamp_str

def truncate_text(text: str, max_length: int = 100) -> str:
    """Truncate text with ellipsis"""
    if len(text) <= max_length:
        return text
    return text[:max_length] + "..."

def sanitize_filename(name: str) -> str:
    """Convert string to valid filename"""
    return re.sub(r'[^\w\-_.]', '_', name)

def validate_regex(pattern: str) -> bool:
    """Check if regex pattern is valid"""
    try:
        re.compile(pattern)
        return True
    except re.error:
        return False