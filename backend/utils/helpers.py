"""
Common utility functions for RAG++ system.
"""

from typing import Any, Dict, List, Optional
import hashlib
import json
from datetime import datetime, timedelta
import pandas as pd


def generate_hash(data: Any) -> str:
    """Generate a deterministic hash for any data structure."""
    json_str = json.dumps(data, sort_keys=True, default=str)
    return hashlib.sha256(json_str.encode()).hexdigest()


def safe_divide(numerator: float, denominator: float, default: float = 0.0) -> float:
    """Safely divide two numbers, returning default if denominator is zero."""
    if denominator == 0:
        return default
    return numerator / denominator


def calculate_percentage_change(old_value: float, new_value: float) -> Optional[float]:
    """Calculate percentage change between two values."""
    if old_value == 0:
        return None
    return ((new_value - old_value) / abs(old_value)) * 100


def parse_time_window(time_str: str) -> tuple[datetime, datetime]:
    """
    Parse time window strings like 'last_7_days', 'last_month', 'Q1_2024'.
    Returns (start_date, end_date).
    """
    now = datetime.now()
    
    if time_str.startswith("last_"):
        parts = time_str.split("_")
        if len(parts) == 3:  # e.g., last_7_days
            num = int(parts[1])
            unit = parts[2]
            
            if unit.startswith("day"):
                delta = timedelta(days=num)
            elif unit.startswith("week"):
                delta = timedelta(weeks=num)
            elif unit.startswith("month"):
                delta = timedelta(days=num * 30)  # Approximate
            else:
                delta = timedelta(days=7)  # Default
            
            return now - delta, now
    
    # Default: last 7 days
    return now - timedelta(days=7), now


def format_metric_value(value: float, metric_type: str = "number") -> str:
    """Format metric values for display."""
    if metric_type == "percentage":
        return f"{value:.2f}%"
    elif metric_type == "currency":
        return f"${value:,.2f}"
    elif metric_type == "count":
        return f"{int(value):,}"
    else:
        return f"{value:.2f}"


def is_significant_change(change_pct: float, threshold: float = 10.0) -> bool:
    """Determine if a percentage change is significant."""
    return abs(change_pct) >= threshold


def clean_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """Clean a dataframe by removing duplicates and handling missing values."""
    df = df.drop_duplicates()
    # Fill numeric columns with 0, categorical with 'Unknown'
    for col in df.columns:
        if df[col].dtype in ['float64', 'int64']:
            df[col] = df[col].fillna(0)
        else:
            df[col] = df[col].fillna('Unknown')
    return df


def truncate_text(text: str, max_length: int = 500) -> str:
    """Truncate text to a maximum length."""
    if len(text) <= max_length:
        return text
    return text[:max_length] + "..."
