"""Utility helper functions."""
from datetime import datetime
from typing import Any, Dict
import json


def format_datetime(dt: datetime, fmt: str = '%Y-%m-%d %H:%M:%S') -> str:
    """
    Format a datetime object to string.
    
    Args:
        dt: Datetime object to format
        fmt: Format string
        
    Returns:
        Formatted datetime string
    """
    if dt is None:
        return None
    return dt.strftime(fmt)


def safe_json_loads(data: str, default: Any = None) -> Any:
    """
    Safely load JSON data with error handling.
    
    Args:
        data: JSON string to parse
        default: Default value to return on error
        
    Returns:
        Parsed JSON data or default value
    """
    try:
        return json.loads(data)
    except (json.JSONDecodeError, TypeError):
        return default


def validate_required_fields(data: Dict, required_fields: list) -> tuple[bool, list]:
    """
    Validate that required fields are present in data.
    
    Args:
        data: Dictionary to validate
        required_fields: List of required field names
        
    Returns:
        Tuple of (is_valid, missing_fields)
    """
    if not isinstance(data, dict):
        return False, required_fields
    
    missing_fields = [field for field in required_fields if field not in data]
    return len(missing_fields) == 0, missing_fields


def sanitize_string(value: str, max_length: int = None) -> str:
    """
    Sanitize a string value.
    
    Args:
        value: String to sanitize
        max_length: Maximum length to truncate to
        
    Returns:
        Sanitized string
    """
    if not isinstance(value, str):
        return str(value)
    
    # Strip whitespace
    value = value.strip()
    
    # Truncate if max_length is specified
    if max_length and len(value) > max_length:
        value = value[:max_length]
    
    return value
