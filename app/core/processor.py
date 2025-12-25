"""
BERTopic Pro - Text Processor
Core text processing module with Jieba integration and cleaning pipeline.
"""

import re
from typing import List, Set, Optional, Callable
from pathlib import Path
import pandas as pd
import jieba
import jieba.posseg as pseg
from app.utils.logger import get_logger
import config


logger = get_logger(__name__)


class TextProcessor:
    """
    Text processing pipeline with Chinese support.

    Features:
    - Jieba segmentation
    - Stopwords filtering
    - URL/email removal
    - Punctuation removal
    - Custom cleaning rules
    """

    def __init__(
        self,
        stopwords_path: Optional[Path] = None,
        custom_dict_path: Optional[Path] = None,
        enable_parallel: bool = True,
    ):
        """
        Initialize text processor.

        Args:
            stopwords_path: Path to stopwords file
            custom_dict_path: Path to custom Jieba dictionary
            enable_parallel: Whether to enable Jieba parallel mode
        """
        self.logger = get_logger(self.__class__.__name__)

        # Load stopwords
        self.stopwords: Set[str] = set()
        if stopwords_path and stopwords_path.exists():
            self.load_stopwords(stopwords_path)
        elif config.DEFAULT_STOPWORDS_PATH.exists():
            self.load_stopwords(config.DEFAULT_STOPWORDS_PATH)

        # Load custom dictionary
        if custom_dict_path and custom_dict_path.exists():
            jieba.load_userdict(str(custom_dict_path))
            self.logger.info(f"Loaded custom dictionary: {custom_dict_path}")

        # Enable parallel mode
        if enable_parallel and config.JIEBA_PARALLEL_MODE:
            jieba.enable_parallel(config.JIEBA_PARALLEL_PROCESSES)
            self.logger.info(f"Jieba parallel mode enabled ({config.JIEBA_PARALLEL_PROCESSES} processes)")

        # Regex patterns
        self.url_pattern = re.compile(
            r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
        )
        self.email_pattern = re.compile(r'[\w\.-]+@[\w\.-]+\.\w+')
        self.punctuation_pattern = re.compile(r'[^\w\s]')
        self.whitespace_pattern = re.compile(r'\s+')
        self.number_pattern = re.compile(r'\d+')

        self.logger.info("TextProcessor initialized")

    def load_stopwords(self, stopwords_path: Path) -> None:
        """
        Load stopwords from file.

        Args:
            stopwords_path: Path to stopwords file (one word per line)
        """
        try:
            with open(stopwords_path, 'r', encoding='utf-8') as f:
                self.stopwords = set(line.strip() for line in f if line.strip())

            self.logger.info(f"Loaded {len(self.stopwords)} stopwords from {stopwords_path}")

        except Exception as e:
            self.logger.error(f"Failed to load stopwords: {e}")

    def add_stopwords(self, words: List[str]) -> None:
        """
        Add stopwords to the set.

        Args:
            words: List of stopwords to add
        """
        self.stopwords.update(words)
        self.logger.info(f"Added {len(words)} stopwords, total: {len(self.stopwords)}")

    def segment(
        self,
        text: str,
        cut_all: bool = False,
        use_pos: bool = False,
        allowed_pos: Optional[Set[str]] = None
    ) -> List[str]:
        """
        Segment text using Jieba.

        Args:
            text: Input text
            cut_all: Whether to use full mode (default: precise mode)
            use_pos: Whether to use POS tagging
            allowed_pos: Set of allowed POS tags (e.g., {'n', 'v', 'a'})

        Returns:
            List of segmented words
        """
        if not text or not isinstance(text, str):
            return []

        if use_pos and allowed_pos:
            # POS tagging mode
            words = pseg.cut(text)
            return [word for word, pos in words if pos in allowed_pos]
        else:
            # Regular segmentation
            return list(jieba.cut(text, cut_all=cut_all))

    def remove_stopwords(self, words: List[str]) -> List[str]:
        """
        Remove stopwords from word list.

        Args:
            words: List of words

        Returns:
            List of words without stopwords
        """
        return [word for word in words if word not in self.stopwords]

    def clean_text(
        self,
        text: str,
        remove_urls: bool = True,
        remove_emails: bool = True,
        remove_punctuation: bool = True,
        remove_numbers: bool = False,
        lowercase: bool = False,
        strip_whitespace: bool = True,
    ) -> str:
        """
        Clean text with various options.

        Args:
            text: Input text
            remove_urls: Remove URLs
            remove_emails: Remove email addresses
            remove_punctuation: Remove punctuation
            remove_numbers: Remove numbers
            lowercase: Convert to lowercase
            strip_whitespace: Normalize whitespace

        Returns:
            Cleaned text
        """
        if not text or not isinstance(text, str):
            return ""

        # Remove URLs
        if remove_urls:
            text = self.url_pattern.sub(' ', text)

        # Remove emails
        if remove_emails:
            text = self.email_pattern.sub(' ', text)

        # Remove numbers
        if remove_numbers:
            text = self.number_pattern.sub(' ', text)

        # Remove punctuation
        if remove_punctuation:
            text = self.punctuation_pattern.sub(' ', text)

        # Lowercase
        if lowercase:
            text = text.lower()

        # Normalize whitespace
        if strip_whitespace:
            text = self.whitespace_pattern.sub(' ', text).strip()

        return text

    def process_text(
        self,
        text: str,
        segment: bool = True,
        remove_stopwords: bool = True,
        clean_options: Optional[dict] = None,
        min_word_length: int = 1,
    ) -> str:
        """
        Complete text processing pipeline.

        Args:
            text: Input text
            segment: Whether to segment text
            remove_stopwords: Whether to remove stopwords
            clean_options: Cleaning options dict (if None, uses defaults)
            min_word_length: Minimum word length to keep

        Returns:
            Processed text (space-separated words if segmented)
        """
        if not text or not isinstance(text, str):
            return ""

        # Default cleaning options
        if clean_options is None:
            clean_options = {
                'remove_urls': config.DEFAULT_REMOVE_URLS,
                'remove_emails': config.DEFAULT_REMOVE_EMAILS,
                'remove_punctuation': config.DEFAULT_REMOVE_PUNCTUATION,
                'lowercase': config.DEFAULT_LOWERCASE,
            }

        # Clean text first
        cleaned = self.clean_text(text, **clean_options)

        # Segment if requested
        if segment:
            words = self.segment(cleaned)

            # Remove stopwords
            if remove_stopwords:
                words = self.remove_stopwords(words)

            # Filter by word length
            if min_word_length > 1:
                words = [w for w in words if len(w) >= min_word_length]

            # Join back to string
            return ' '.join(words)

        return cleaned

    def process_dataframe(
        self,
        df: pd.DataFrame,
        text_column: str,
        output_column: Optional[str] = None,
        progress_callback: Optional[Callable[[int, str], None]] = None,
        **processing_options
    ) -> pd.DataFrame:
        """
        Process text column in DataFrame with progress tracking.

        Args:
            df: Input DataFrame
            text_column: Name of column containing text
            output_column: Name of output column (if None, overwrites input)
            progress_callback: Callback function(progress_pct, status_msg)
            **processing_options: Options for process_text()

        Returns:
            DataFrame with processed text column
        """
        if text_column not in df.columns:
            raise ValueError(f"Column '{text_column}' not found in DataFrame")

        output_column = output_column or f"{text_column}_processed"

        total_rows = len(df)
        processed_texts = []

        self.logger.info(f"Processing {total_rows} texts...")

        for idx, text in enumerate(df[text_column]):
            # Process text
            processed = self.process_text(text, **processing_options)
            processed_texts.append(processed)

            # Progress callback
            if progress_callback and (idx + 1) % 100 == 0:
                progress = int((idx + 1) / total_rows * 100)
                progress_callback(progress, f"Processing: {idx + 1}/{total_rows}")

        # Create output column
        df = df.copy()
        df[output_column] = processed_texts

        if progress_callback:
            progress_callback(100, f"Completed: {total_rows} texts processed")

        self.logger.info(f"Processing completed: {total_rows} texts")

        return df

    def get_word_frequencies(
        self,
        texts: List[str],
        top_n: int = 100
    ) -> List[tuple[str, int]]:
        """
        Get top N most frequent words from texts.

        Args:
            texts: List of texts
            top_n: Number of top words to return

        Returns:
            List of (word, frequency) tuples
        """
        from collections import Counter

        word_counter = Counter()

        for text in texts:
            words = self.segment(text)
            words = self.remove_stopwords(words)
            word_counter.update(words)

        return word_counter.most_common(top_n)

    def estimate_processing_time(self, num_texts: int) -> float:
        """
        Estimate processing time in seconds.

        Args:
            num_texts: Number of texts to process

        Returns:
            Estimated time in seconds
        """
        # Rough estimate: 1000 texts per second with Jieba
        estimated_time = num_texts / 1000.0
        return estimated_time
