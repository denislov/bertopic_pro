"""
BERTopic Pro - File Helpers
Utilities for reading various file formats with encoding detection.
"""

from pathlib import Path
from typing import Optional, List, Tuple
import pandas as pd
import chardet
from app.utils.logger import get_logger
import config


logger = get_logger(__name__)


class FileReadError(Exception):
    """Custom exception for file reading errors."""
    pass


def detect_encoding(file_path: Path, sample_size: int = 10000) -> str:
    """
    Detect file encoding using chardet.

    Args:
        file_path: Path to the file
        sample_size: Number of bytes to read for detection

    Returns:
        Detected encoding name (e.g., 'utf-8', 'gbk')
    """
    try:
        with open(file_path, 'rb') as f:
            raw_data = f.read(sample_size)
            result = chardet.detect(raw_data)
            encoding = result['encoding']
            confidence = result['confidence']

            logger.info(f"Detected encoding: {encoding} (confidence: {confidence:.2%})")

            # If confidence is too low, default to utf-8
            if confidence < 0.7:
                logger.warning(f"Low confidence ({confidence:.2%}), defaulting to utf-8")
                return 'utf-8'

            return encoding or 'utf-8'

    except Exception as e:
        logger.error(f"Encoding detection failed: {e}, defaulting to utf-8")
        return 'utf-8'


def read_csv_file(
    file_path: Path,
    encoding: Optional[str] = None,
    **kwargs
) -> pd.DataFrame:
    """
    Read CSV file with automatic encoding detection.

    Args:
        file_path: Path to CSV file
        encoding: Explicit encoding (if None, will auto-detect)
        **kwargs: Additional arguments for pd.read_csv

    Returns:
        DataFrame with loaded data

    Raises:
        FileReadError: If file cannot be read
    """
    try:
        # Auto-detect encoding if not provided
        if encoding is None:
            encoding = detect_encoding(file_path)

        # Try reading with detected encoding
        df = pd.read_csv(file_path, encoding=encoding, **kwargs)

        logger.info(f"CSV loaded: {len(df)} rows, {len(df.columns)} columns")
        return df

    except UnicodeDecodeError:
        # Retry with alternative encodings
        logger.warning(f"Failed with {encoding}, trying alternatives...")

        for alt_encoding in ['utf-8', 'gbk', 'gb2312', 'latin1']:
            try:
                df = pd.read_csv(file_path, encoding=alt_encoding, **kwargs)
                logger.info(f"Success with {alt_encoding}: {len(df)} rows")
                return df
            except UnicodeDecodeError:
                continue

        raise FileReadError("Failed to read CSV with any encoding")

    except Exception as e:
        logger.error(f"CSV read error: {e}")
        raise FileReadError(f"Failed to read CSV: {str(e)}")


def read_excel_file(
    file_path: Path,
    sheet_name: Optional[str] = None,
    **kwargs
) -> pd.DataFrame:
    """
    Read Excel file (.xlsx, .xls).

    Args:
        file_path: Path to Excel file
        sheet_name: Sheet name to read (None = first sheet)
        **kwargs: Additional arguments for pd.read_excel

    Returns:
        DataFrame with loaded data

    Raises:
        FileReadError: If file cannot be read
    """
    try:
        df = pd.read_excel(file_path, sheet_name=sheet_name or 0, **kwargs)
        logger.info(f"Excel loaded: {len(df)} rows, {len(df.columns)} columns")
        return df

    except Exception as e:
        logger.error(f"Excel read error: {e}")
        raise FileReadError(f"Failed to read Excel: {str(e)}")


def read_txt_file(
    file_path: Path,
    encoding: Optional[str] = None,
    delimiter: str = '\t',
    **kwargs
) -> pd.DataFrame:
    """
    Read TXT file (tab-delimited by default).

    Args:
        file_path: Path to TXT file
        encoding: Explicit encoding (if None, will auto-detect)
        delimiter: Column delimiter
        **kwargs: Additional arguments for pd.read_csv

    Returns:
        DataFrame with loaded data

    Raises:
        FileReadError: If file cannot be read
    """
    try:
        if encoding is None:
            encoding = detect_encoding(file_path)

        df = pd.read_csv(file_path, encoding=encoding, delimiter=delimiter, **kwargs)
        logger.info(f"TXT loaded: {len(df)} rows, {len(df.columns)} columns")
        return df

    except Exception as e:
        logger.error(f"TXT read error: {e}")
        raise FileReadError(f"Failed to read TXT: {str(e)}")


def read_file(file_path: str | Path, **kwargs) -> pd.DataFrame:
    """
    Read file automatically based on extension.

    Args:
        file_path: Path to file
        **kwargs: Additional arguments for specific readers

    Returns:
        DataFrame with loaded data

    Raises:
        FileReadError: If file format is unsupported or read fails
    """
    file_path = Path(file_path)

    if not file_path.exists():
        raise FileReadError(f"File not found: {file_path}")

    suffix = file_path.suffix.lower()

    if suffix == '.csv':
        return read_csv_file(file_path, **kwargs)
    elif suffix in ['.xlsx', '.xls']:
        return read_excel_file(file_path, **kwargs)
    elif suffix == '.txt':
        return read_txt_file(file_path, **kwargs)
    else:
        raise FileReadError(
            f"Unsupported file format: {suffix}. "
            f"Supported formats: {', '.join(config.SUPPORTED_DATA_FORMATS)}"
        )


def get_column_info(df: pd.DataFrame) -> List[Tuple[str, str, int]]:
    """
    Get information about DataFrame columns.

    Args:
        df: DataFrame to analyze

    Returns:
        List of tuples (column_name, dtype, non_null_count)
    """
    info = []
    for col in df.columns:
        dtype = str(df[col].dtype)
        non_null = df[col].notna().sum()
        info.append((col, dtype, non_null))

    return info


def preview_dataframe(
    df: pd.DataFrame,
    max_rows: int = None,
    max_col_width: int = None
) -> pd.DataFrame:
    """
    Create a preview of DataFrame with limited rows and column width.

    Args:
        df: DataFrame to preview
        max_rows: Maximum number of rows (from config if None)
        max_col_width: Maximum column width (from config if None)

    Returns:
        Preview DataFrame
    """
    max_rows = max_rows or config.DATA_PREVIEW_ROWS
    max_col_width = max_col_width or config.DATA_PREVIEW_MAX_COLUMN_WIDTH

    # Get preview rows
    preview = df.head(max_rows).copy()

    # Truncate long strings in each column
    for col in preview.columns:
        if preview[col].dtype == 'object':
            preview[col] = preview[col].astype(str).apply(
                lambda x: x[:max_col_width] + '...' if len(x) > max_col_width else x
            )

    return preview


def save_dataframe(
    df: pd.DataFrame,
    file_path: str | Path,
    **kwargs
) -> None:
    """
    Save DataFrame to file based on extension.

    Args:
        df: DataFrame to save
        file_path: Output file path
        **kwargs: Additional arguments for specific writers

    Raises:
        FileReadError: If save fails
    """
    file_path = Path(file_path)
    suffix = file_path.suffix.lower()

    try:
        if suffix == '.csv':
            df.to_csv(file_path, index=False, encoding='utf-8-sig', **kwargs)
        elif suffix in ['.xlsx', '.xls']:
            df.to_excel(file_path, index=False, **kwargs)
        else:
            raise FileReadError(f"Unsupported output format: {suffix}")

        logger.info(f"Saved {len(df)} rows to {file_path}")

    except Exception as e:
        logger.error(f"Save error: {e}")
        raise FileReadError(f"Failed to save file: {str(e)}")
