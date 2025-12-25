"""
BERTopic Pro - Configuration Manager
Manages application configuration using QSettings (user preferences) and JSON (model configs).
"""

import json
from typing import Any, Optional, Dict
from pathlib import Path
from PySide6.QtCore import QSettings
from app.utils.logger import get_logger
import config


class ConfigManager:
    """
    Manages application configuration with multiple layers:
    1. QSettings for user preferences (UI state, recent files, etc.)
    2. JSON file for model configurations and parameters
    """

    def __init__(self):
        """Initialize the configuration manager."""
        self.logger = get_logger(self.__class__.__name__)

        # Qt Settings for user preferences
        self.settings = QSettings(config.ORGANIZATION_NAME, config.APP_NAME)

        # JSON config file path
        self.model_config_path = config.USER_CONFIG_FILE

        # Cache for model configurations
        self._model_config_cache: Optional[Dict] = None

        self.logger.info("Configuration manager initialized")

    # ========================================================================
    # QSettings Methods (User Preferences)
    # ========================================================================

    def get(self, key: str, default: Any = None) -> Any:
        """
        Get a value from QSettings.

        Args:
            key: Setting key
            default: Default value if key doesn't exist

        Returns:
            Setting value or default
        """
        value = self.settings.value(key, default)
        self.logger.debug(f"Get setting: {key} = {value}")
        return value

    def set(self, key: str, value: Any):
        """
        Set a value in QSettings.

        Args:
            key: Setting key
            value: Setting value
        """
        self.settings.setValue(key, value)
        self.settings.sync()  # Force write to disk
        self.logger.debug(f"Set setting: {key} = {value}")

    def remove(self, key: str):
        """
        Remove a setting.

        Args:
            key: Setting key
        """
        self.settings.remove(key)
        self.logger.debug(f"Removed setting: {key}")

    def clear_all_settings(self):
        """Clear all QSettings."""
        self.settings.clear()
        self.logger.warning("All QSettings cleared")

    def save(self):
        """
        Explicitly save all settings to disk.

        Note: QSettings auto-saves on each setValue(), but this method
        can be called to ensure all pending writes are flushed.
        """
        self.settings.sync()
        self.logger.debug("Settings synced to disk")

    # ========================================================================
    # Window Geometry & State
    # ========================================================================

    def save_window_geometry(self, geometry: bytes):
        """
        Save window geometry.

        Args:
            geometry: Window geometry from saveGeometry()
        """
        self.set("window/geometry", geometry)

    def load_window_geometry(self) -> Optional[bytes]:
        """
        Load window geometry.

        Returns:
            Window geometry bytes or None
        """
        return self.get("window/geometry", None)

    def save_window_state(self, state: bytes):
        """
        Save window state (splitters, etc.).

        Args:
            state: Window state from saveState()
        """
        self.set("window/state", state)

    def load_window_state(self) -> Optional[bytes]:
        """
        Load window state.

        Returns:
            Window state bytes or None
        """
        return self.get("window/state", None)

    # ========================================================================
    # Recent Files
    # ========================================================================

    def add_recent_file(self, file_path: str):
        """
        Add a file to recent files list.

        Args:
            file_path: Path to the file
        """
        recent_files = self.get_recent_files()

        # Remove if already exists (to move to top)
        if file_path in recent_files:
            recent_files.remove(file_path)

        # Add to beginning
        recent_files.insert(0, file_path)

        # Keep only last 10
        recent_files = recent_files[:10]

        self.set("recent_files", recent_files)
        self.logger.info(f"Added recent file: {file_path}")

    def get_recent_files(self) -> list[str]:
        """
        Get list of recent files.

        Returns:
            List of recent file paths
        """
        recent_files = self.get("recent_files", [])
        # Filter out non-existent files
        return [f for f in recent_files if Path(f).exists()]

    def clear_recent_files(self):
        """Clear recent files list."""
        self.set("recent_files", [])
        self.logger.info("Recent files cleared")

    # ========================================================================
    # JSON Model Configuration
    # ========================================================================

    def load_model_config(self) -> Dict[str, Any]:
        """
        Load model configuration from JSON file.

        Returns:
            Model configuration dictionary
        """
        if self._model_config_cache is not None:
            return self._model_config_cache

        if self.model_config_path.exists():
            try:
                with open(self.model_config_path, "r", encoding="utf-8") as f:
                    self._model_config_cache = json.load(f)
                self.logger.info(f"Model config loaded from {self.model_config_path}")
                return self._model_config_cache
            except Exception as e:
                self.logger.error(f"Failed to load model config: {e}")
                self._model_config_cache = {}
                return {}
        else:
            self.logger.info("No model config file found, using defaults")
            self._model_config_cache = {}
            return {}

    def save_model_config(self, config_dict: Dict[str, Any]):
        """
        Save model configuration to JSON file.

        Args:
            config_dict: Configuration dictionary to save
        """
        try:
            with open(self.model_config_path, "w", encoding="utf-8") as f:
                json.dump(config_dict, f, indent=2, ensure_ascii=False)
            self._model_config_cache = config_dict
            self.logger.info(f"Model config saved to {self.model_config_path}")
        except Exception as e:
            self.logger.error(f"Failed to save model config: {e}")
            raise

    def get_model_param(self, param_name: str, default: Any = None) -> Any:
        """
        Get a model parameter from JSON config.

        Args:
            param_name: Parameter name (supports dot notation, e.g., "umap.n_neighbors")
            default: Default value if parameter doesn't exist

        Returns:
            Parameter value or default
        """
        config_dict = self.load_model_config()

        # Support dot notation for nested keys
        keys = param_name.split(".")
        value = config_dict

        for key in keys:
            if isinstance(value, dict) and key in value:
                value = value[key]
            else:
                return default

        return value

    def set_model_param(self, param_name: str, value: Any):
        """
        Set a model parameter in JSON config.

        Args:
            param_name: Parameter name (supports dot notation)
            value: Parameter value
        """
        config_dict = self.load_model_config()

        # Support dot notation for nested keys
        keys = param_name.split(".")
        current = config_dict

        for key in keys[:-1]:
            if key not in current:
                current[key] = {}
            current = current[key]

        current[keys[-1]] = value
        self.save_model_config(config_dict)

    # ========================================================================
    # LLM Configuration
    # ========================================================================

    def get_llm_provider(self) -> str:
        """
        Get selected LLM provider.

        Returns:
            Provider name ("openai", "ollama", "zhipu", or "none")
        """
        return self.get("llm/provider", "none")

    def set_llm_provider(self, provider: str):
        """
        Set LLM provider.

        Args:
            provider: Provider name
        """
        self.set("llm/provider", provider)

    def get_llm_api_key(self, provider: str) -> str:
        """
        Get API key for LLM provider.

        Args:
            provider: Provider name

        Returns:
            API key (empty string if not set)
        """
        return self.get(f"llm/{provider}/api_key", "")

    def set_llm_api_key(self, provider: str, api_key: str):
        """
        Set API key for LLM provider.

        Args:
            provider: Provider name
            api_key: API key
        """
        self.set(f"llm/{provider}/api_key", api_key)

    def get_llm_model(self, provider: str) -> str:
        """
        Get model name for LLM provider.

        Args:
            provider: Provider name

        Returns:
            Model name
        """
        defaults = {
            "openai": config.OPENAI_DEFAULT_MODEL,
            "ollama": config.OLLAMA_DEFAULT_MODEL,
            "zhipu": config.ZHIPU_DEFAULT_MODEL,
        }
        return self.get(f"llm/{provider}/model", defaults.get(provider, ""))

    def set_llm_model(self, provider: str, model: str):
        """
        Set model name for LLM provider.

        Args:
            provider: Provider name
            model: Model name
        """
        self.set(f"llm/{provider}/model", model)

    # ========================================================================
    # Hardware Configuration
    # ========================================================================

    def get_device(self) -> str:
        """
        Get compute device (cpu/cuda).

        Returns:
            Device string
        """
        return self.get("hardware/device", config.DEFAULT_DEVICE)

    def set_device(self, device: str):
        """
        Set compute device.

        Args:
            device: Device string ("cpu" or "cuda")
        """
        self.set("hardware/device", device)

    def get_use_gpu(self) -> bool:
        """
        Get whether to use GPU.

        Returns:
            True if GPU should be used
        """
        return self.get("hardware/use_gpu", config.DEFAULT_USE_GPU)

    def set_use_gpu(self, use_gpu: bool):
        """
        Set whether to use GPU.

        Args:
            use_gpu: True to use GPU
        """
        self.set("hardware/use_gpu", use_gpu)


# Singleton instance
_config_manager_instance: Optional[ConfigManager] = None


def get_config_manager() -> ConfigManager:
    """
    Get the singleton ConfigManager instance.

    Returns:
        ConfigManager instance
    """
    global _config_manager_instance
    if _config_manager_instance is None:
        _config_manager_instance = ConfigManager()
    return _config_manager_instance
