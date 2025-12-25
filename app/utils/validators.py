"""
BERTopic Pro - Input Validators
Validation utilities for data preprocessing.
"""

from typing import Optional, List, Tuple
import pandas as pd
import re
from datetime import datetime
from app.utils.logger import get_logger
import config


logger = get_logger(__name__)


class ValidationError(Exception):
    """Custom exception for validation errors."""
    pass


def validate_dataframe(df: pd.DataFrame) -> Tuple[bool, Optional[str]]:
    """
    Validate that DataFrame is suitable for processing.

    Args:
        df: DataFrame to validate

    Returns:
        Tuple of (is_valid, error_message)
    """
    if df is None:
        return False, "DataFrame is None"

    if df.empty:
        return False, "DataFrame is empty"

    if len(df.columns) == 0:
        return False, "DataFrame has no columns"

    return True, None


def validate_column_exists(df: pd.DataFrame, column_name: str) -> Tuple[bool, Optional[str]]:
    """
    Validate that a column exists in DataFrame.

    Args:
        df: DataFrame to check
        column_name: Column name to validate

    Returns:
        Tuple of (is_valid, error_message)
    """
    if column_name not in df.columns:
        return False, f"Column '{column_name}' not found in DataFrame"

    return True, None


def validate_column_not_empty(df: pd.DataFrame, column_name: str) -> Tuple[bool, Optional[str]]:
    """
    Validate that a column is not entirely empty.

    Args:
        df: DataFrame to check
        column_name: Column name to validate

    Returns:
        Tuple of (is_valid, error_message)
    """
    is_valid, error = validate_column_exists(df, column_name)
    if not is_valid:
        return is_valid, error

    if df[column_name].isna().all():
        return False, f"Column '{column_name}' contains only null values"

    non_null_count = df[column_name].notna().sum()
    if non_null_count == 0:
        return False, f"Column '{column_name}' has no valid data"

    return True, None


def validate_text_column(
    df: pd.DataFrame,
    column_name: str,
    min_length: Optional[int] = None,
    allow_empty: bool = False
) -> Tuple[bool, Optional[str], dict]:
    """
    Validate a text column for text processing.

    Args:
        df: DataFrame to check
        column_name: Column name to validate
        min_length: Minimum text length (from config if None)
        allow_empty: Whether to allow empty strings

    Returns:
        Tuple of (is_valid, error_message, statistics_dict)
    """
    min_length = min_length or config.DEFAULT_MIN_TEXT_LENGTH

    # Check existence and non-empty
    is_valid, error = validate_column_not_empty(df, column_name)
    if not is_valid:
        return is_valid, error, {}

    # Convert to string and analyze
    text_series = df[column_name].astype(str)

    # Statistics
    total_count = len(text_series)
    empty_count = (text_series.str.strip() == '').sum()
    too_short_count = (text_series.str.len() < min_length).sum()
    valid_count = total_count - empty_count - too_short_count

    stats = {
        'total': total_count,
        'empty': empty_count,
        'too_short': too_short_count,
        'valid': valid_count,
        'valid_ratio': valid_count / total_count if total_count > 0 else 0,
        'avg_length': text_series.str.len().mean(),
        'max_length': text_series.str.len().max(),
    }

    # Validation
    if not allow_empty and empty_count > 0:
        return False, f"Column '{column_name}' contains {empty_count} empty values", stats

    if valid_count == 0:
        return False, f"Column '{column_name}' has no valid text (min length: {min_length})", stats

    if valid_count / total_count < 0.5:
        return False, f"Column '{column_name}' has too few valid texts ({valid_count}/{total_count})", stats

    logger.info(f"Text column '{column_name}' validated: {valid_count}/{total_count} valid")
    return True, None, stats


def validate_timestamp_column(
    df: pd.DataFrame,
    column_name: str,
    date_formats: Optional[List[str]] = None
) -> Tuple[bool, Optional[str], dict]:
    """
    Validate a timestamp column.

    Args:
        df: DataFrame to check
        column_name: Column name to validate
        date_formats: List of date formats to try (common formats if None)

    Returns:
        Tuple of (is_valid, error_message, statistics_dict)
    """
    # Check existence
    is_valid, error = validate_column_exists(df, column_name)
    if not is_valid:
        return is_valid, error, {}

    # Common date formats
    if date_formats is None:
        date_formats = [
            '%Y-%m-%d',
            '%Y/%m/%d',
            '%Y-%m-%d %H:%M:%S',
            '%Y/%m/%d %H:%M:%S',
            '%d-%m-%Y',
            '%d/%m/%Y',
        ]

    # Try parsing
    timestamp_series = df[column_name]
    total_count = len(timestamp_series)
    parsed_count = 0
    parse_errors = 0

    for fmt in date_formats:
        try:
            parsed = pd.to_datetime(timestamp_series, format=fmt, errors='coerce')
            valid = parsed.notna().sum()
            if valid > parsed_count:
                parsed_count = valid
                best_format = fmt
        except:
            continue

    # Try without format (pandas auto-detection)
    try:
        parsed = pd.to_datetime(timestamp_series, errors='coerce')
        valid = parsed.notna().sum()
        if valid > parsed_count:
            parsed_count = valid
            best_format = 'auto'
    except:
        pass

    stats = {
        'total': total_count,
        'parsed': parsed_count,
        'parse_ratio': parsed_count / total_count if total_count > 0 else 0,
        'best_format': best_format if parsed_count > 0 else None,
    }

    # Validation
    if parsed_count == 0:
        return False, f"Column '{column_name}' cannot be parsed as timestamps", stats

    if parsed_count / total_count < 0.8:
        return False, f"Column '{column_name}' has too many invalid timestamps ({parsed_count}/{total_count})", stats

    logger.info(f"Timestamp column '{column_name}' validated: {parsed_count}/{total_count} valid")
    return True, None, stats


def validate_file_path(file_path: str) -> Tuple[bool, Optional[str]]:
    """
    Validate file path and format.

    Args:
        file_path: Path to validate

    Returns:
        Tuple of (is_valid, error_message)
    """
    from pathlib import Path

    if not file_path:
        return False, "File path is empty"

    path = Path(file_path)

    if not path.exists():
        return False, f"File does not exist: {file_path}"

    if not path.is_file():
        return False, f"Path is not a file: {file_path}"

    suffix = path.suffix.lower()
    if suffix not in config.SUPPORTED_DATA_FORMATS:
        return False, f"Unsupported file format: {suffix}. Supported: {', '.join(config.SUPPORTED_DATA_FORMATS)}"

    return True, None


def validate_stopwords_file(file_path: str) -> Tuple[bool, Optional[str]]:
    """
    Validate stopwords file.

    Args:
        file_path: Path to stopwords file

    Returns:
        Tuple of (is_valid, error_message)
    """
    from pathlib import Path

    if not file_path:
        return True, None  # Optional

    path = Path(file_path)

    if not path.exists():
        return False, f"Stopwords file not found: {file_path}"

    if not path.is_file():
        return False, f"Stopwords path is not a file: {file_path}"

    try:
        with open(path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            if len(lines) == 0:
                return False, "Stopwords file is empty"

        logger.info(f"Stopwords file validated: {len(lines)} words")
        return True, None

    except Exception as e:
        return False, f"Failed to read stopwords file: {str(e)}"


def get_recommended_columns(
    df: pd.DataFrame,
    for_text: bool = True
) -> List[str]:
    """
    Get recommended columns for text or timestamp.

    Args:
        df: DataFrame to analyze
        for_text: If True, recommend text columns; if False, recommend timestamp columns

    Returns:
        List of recommended column names
    """
    recommendations = []

    if for_text:
        # Look for likely text columns
        for col in df.columns:
            # Check dtype
            if df[col].dtype == 'object':
                # Check average length
                avg_len = df[col].astype(str).str.len().mean()
                if avg_len > 10:  # Likely text, not categories
                    recommendations.append(col)

        # Keywords in column names
        text_keywords = ['text', 'content', 'message', 'comment', 'description', '内容', '文本', '评论']
        for col in df.columns:
            if any(keyword in col.lower() for keyword in text_keywords):
                if col not in recommendations:
                    recommendations.append(col)

    else:
        # Look for likely timestamp columns
        for col in df.columns:
            # Check dtype
            if pd.api.types.is_datetime64_any_dtype(df[col]):
                recommendations.append(col)

        # Keywords in column names
        time_keywords = ['date', 'time', 'timestamp', 'created', 'published', '时间', '日期']
        for col in df.columns:
            if any(keyword in col.lower() for keyword in time_keywords):
                if col not in recommendations:
                    recommendations.append(col)

    return recommendations
