"""
BERTopic Pro - Global Configuration
Defines all application-wide constants, paths, and default parameters.
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Base directory (project root)
BASE_DIR = Path(__file__).parent.resolve()

# Data directories
DATA_DIR = BASE_DIR / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
PROCESSED_DATA_DIR = DATA_DIR / "processed"
CACHE_DIR = DATA_DIR / "cache"

# Model directories
MODEL_DIR = BASE_DIR / "models"
BERTOPIC_MODEL_DIR = MODEL_DIR / "bertopic"
EMBEDDINGS_CACHE_DIR = MODEL_DIR / "embeddings"

# Resources directories
RESOURCES_DIR = BASE_DIR / "resources"
ICONS_DIR = RESOURCES_DIR / "icons"
FONTS_DIR = RESOURCES_DIR / "fonts"

# Logs directory
LOGS_DIR = BASE_DIR / "logs"

# Ensure all directories exist
for directory in [
    DATA_DIR,
    RAW_DATA_DIR,
    PROCESSED_DATA_DIR,
    CACHE_DIR,
    MODEL_DIR,
    BERTOPIC_MODEL_DIR,
    EMBEDDINGS_CACHE_DIR,
    RESOURCES_DIR,
    ICONS_DIR,
    FONTS_DIR,
    LOGS_DIR,
]:
    directory.mkdir(parents=True, exist_ok=True)

# ============================================================================
# Application Settings
# ============================================================================

APP_NAME = "BERTopic Pro"
APP_VERSION = "0.1.0"
APP_AUTHOR = "BERTopic Pro Team"
ORGANIZATION_NAME = "BertopicPro"

# ============================================================================
# UI Settings
# ============================================================================

# Window settings
WINDOW_TITLE = f"{APP_NAME} v{APP_VERSION}"
WINDOW_MIN_WIDTH = 1200
WINDOW_MIN_HEIGHT = 800
WINDOW_DEFAULT_WIDTH = 1400
WINDOW_DEFAULT_HEIGHT = 900

# Theme colors
PRIMARY_COLOR = "#1976d2"
SECONDARY_COLOR = "#42a5f5"
ACCENT_COLOR = "#1565c0"
ERROR_COLOR = "#d32f2f"
SUCCESS_COLOR = "#388e3c"
WARNING_COLOR = "#f57c00"

# ============================================================================
# BERTopic Model Defaults
# ============================================================================

# Default embedding model
# Using multilingual model for Chinese text support
DEFAULT_EMBEDDING_MODEL = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"

# UMAP parameters
DEFAULT_UMAP_N_NEIGHBORS = 15
DEFAULT_UMAP_N_COMPONENTS = 5
DEFAULT_UMAP_MIN_DIST = 0.0
DEFAULT_UMAP_METRIC = "cosine"

# HDBSCAN parameters
DEFAULT_HDBSCAN_MIN_CLUSTER_SIZE = 10
DEFAULT_HDBSCAN_MIN_SAMPLES = 10
DEFAULT_HDBSCAN_METRIC = "euclidean"
DEFAULT_HDBSCAN_CLUSTER_SELECTION_METHOD = "eom"
DEFAULT_HDBSCAN_CLUSTER_SELECTION_EPSILON = 0.0

# c-TF-IDF parameters
DEFAULT_TOP_N_WORDS = 10
DEFAULT_MIN_TOPIC_SIZE = 10

# ============================================================================
# Text Processing Defaults
# ============================================================================

# Stopwords file path
DEFAULT_STOPWORDS_PATH = DATA_DIR / "stopwords_zh.txt"

# Chinese text processing
JIEBA_PARALLEL_MODE = True
JIEBA_PARALLEL_PROCESSES = 4

# Text cleaning options
DEFAULT_REMOVE_URLS = True
DEFAULT_REMOVE_EMAILS = True
DEFAULT_REMOVE_PUNCTUATION = True
DEFAULT_LOWERCASE = True
DEFAULT_MIN_TEXT_LENGTH = 10

# ============================================================================
# Data Processing Settings
# ============================================================================

# Preview settings
DATA_PREVIEW_ROWS = 50
DATA_PREVIEW_MAX_COLUMN_WIDTH = 200

# Batch processing
EMBEDDING_BATCH_SIZE = 1000
PROCESSING_BATCH_SIZE = 100

# ============================================================================
# Hardware Settings
# ============================================================================

# Device selection (auto-detect by default)
import torch

DEFAULT_DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
DEFAULT_USE_GPU = torch.cuda.is_available()

# Memory settings
MAX_MEMORY_GB = 8
USE_FLOAT32 = True  # Use float32 instead of float64 to save memory

# ============================================================================
# LLM Settings
# ============================================================================

# OpenAI API
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
OPENAI_BASE_URL = os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1")
OPENAI_DEFAULT_MODEL = "gpt-3.5-turbo"

# Ollama
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
OLLAMA_DEFAULT_MODEL = "llama2"

# Zhipu AI
ZHIPU_API_KEY = os.getenv("ZHIPU_API_KEY", "")
ZHIPU_BASE_URL = os.getenv("ZHIPU_BASE_URL", "https://open.bigmodel.cn/api/paas/v4/")
ZHIPU_DEFAULT_MODEL = "glm-4"

# ============================================================================
# File Format Settings
# ============================================================================

# Supported file formats
SUPPORTED_DATA_FORMATS = [".csv", ".xlsx", ".xls", ".txt"]
SUPPORTED_IMAGE_FORMATS = [".png", ".jpg", ".jpeg", ".svg"]

# Export formats
EXPORT_HTML_FORMAT = "html"
EXPORT_PNG_FORMAT = "png"
EXPORT_JSON_FORMAT = "json"

# ============================================================================
# Logging Settings
# ============================================================================

# Log file path
LOG_FILE_PATH = LOGS_DIR / "bertopic_pro.log"

# Logging configuration
LOG_LEVEL = "INFO"
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
LOG_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"
LOG_MAX_BYTES = 10 * 1024 * 1024  # 10 MB
LOG_BACKUP_COUNT = 5

# Console logging
CONSOLE_LOG_MAX_LINES = 1000

# ============================================================================
# Visualization Settings
# ============================================================================

# Plotly configuration
PLOTLY_INCLUDE_PLOTLYJS = "cdn"  # Use CDN to reduce file size
PLOTLY_CONFIG = {
    "responsive": True,
    "displayModeBar": True,
    "displaylogo": False,
    "toImageButtonOptions": {
        "format": "png",
        "filename": "bertopic_visualization",
        "height": 800,
        "width": 1200,
        "scale": 2,
    },
}

# Chinese font for Plotly
PLOTLY_FONT_FAMILY = "Noto Sans CJK SC, Arial, sans-serif"
PLOTLY_FONT_SIZE = 12

# ============================================================================
# Model Download Settings
# ============================================================================

# HuggingFace Hub cache directory
HF_CACHE_DIR = Path.home() / ".cache" / "huggingface" / "hub"

# Download timeout
DOWNLOAD_TIMEOUT = 600  # 10 minutes
DOWNLOAD_RETRY_ATTEMPTS = 3

# ============================================================================
# Performance Settings
# ============================================================================

# Threading
MAX_WORKER_THREADS = 4

# Progress update frequency (seconds)
PROGRESS_UPDATE_INTERVAL = 0.1  # Update UI max 10 times per second

# ============================================================================
# Testing & Development
# ============================================================================

DEBUG_MODE = os.getenv("DEBUG", "False").lower() == "true"
ENABLE_PROFILING = os.getenv("ENABLE_PROFILING", "False").lower() == "true"

# ============================================================================
# User Configuration File
# ============================================================================

USER_CONFIG_FILE = BASE_DIR / "user_config.json"
