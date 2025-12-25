"""
BERTopic Pro - Model Manager
Manages embedding models, downloading, caching, and metadata.
"""

import json
import shutil
from pathlib import Path
from typing import Optional, Dict, Any, Callable, List, Tuple
import torch
from sentence_transformers import SentenceTransformer
from huggingface_hub import snapshot_download, hf_hub_download
from huggingface_hub.utils import RepositoryNotFoundError, HfHubHTTPError
from app.utils.logger import get_logger
import config


logger = get_logger(__name__)


class ModelMetadata:
    """Model metadata container."""

    def __init__(
        self,
        model_name: str,
        model_path: Path,
        model_type: str = "sentence-transformer",
        size_mb: float = 0.0,
        download_date: Optional[str] = None,
        description: str = "",
        language: str = "multilingual",
        max_seq_length: int = 512,
    ):
        self.model_name = model_name
        self.model_path = model_path
        self.model_type = model_type
        self.size_mb = size_mb
        self.download_date = download_date
        self.description = description
        self.language = language
        self.max_seq_length = max_seq_length

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            'model_name': self.model_name,
            'model_path': str(self.model_path),
            'model_type': self.model_type,
            'size_mb': self.size_mb,
            'download_date': self.download_date,
            'description': self.description,
            'language': self.language,
            'max_seq_length': self.max_seq_length,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'ModelMetadata':
        """Create from dictionary."""
        return cls(
            model_name=data['model_name'],
            model_path=Path(data['model_path']),
            model_type=data.get('model_type', 'sentence-transformer'),
            size_mb=data.get('size_mb', 0.0),
            download_date=data.get('download_date'),
            description=data.get('description', ''),
            language=data.get('language', 'multilingual'),
            max_seq_length=data.get('max_seq_length', 512),
        )


class ModelManager:
    """
    Manages embedding models for BERTopic.

    Features:
    - Download models from HuggingFace Hub
    - Cache models locally
    - Track model metadata
    - Device management (CPU/CUDA)
    - Model validation
    """

    def __init__(
        self,
        cache_dir: Optional[Path] = None,
        device: Optional[str] = None,
    ):
        """
        Initialize model manager.

        Args:
            cache_dir: Directory for caching models (default: config.EMBEDDING_CACHE_DIR)
            device: Device to use ('cuda', 'cpu', or None for auto-detect)
        """
        self.logger = get_logger(self.__class__.__name__)

        # Cache directory
        self.cache_dir = cache_dir or config.EMBEDDINGS_CACHE_DIR
        self.cache_dir.mkdir(parents=True, exist_ok=True)

        # Metadata file
        self.metadata_file = self.cache_dir / 'models_metadata.json'
        self.metadata: Dict[str, ModelMetadata] = {}
        self._load_metadata()

        # Device detection
        if device is None:
            self.device = config.DEFAULT_DEVICE
        else:
            self.device = device

        self.logger.info(f"ModelManager initialized (device: {self.device})")

    def _load_metadata(self) -> None:
        """Load model metadata from file."""
        if self.metadata_file.exists():
            try:
                with open(self.metadata_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)

                self.metadata = {
                    name: ModelMetadata.from_dict(info)
                    for name, info in data.items()
                }

                self.logger.info(f"Loaded metadata for {len(self.metadata)} models")

            except Exception as e:
                self.logger.error(f"Failed to load metadata: {e}")
                self.metadata = {}

    def _save_metadata(self) -> None:
        """Save model metadata to file."""
        try:
            data = {
                name: meta.to_dict()
                for name, meta in self.metadata.items()
            }

            with open(self.metadata_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)

            self.logger.info("Metadata saved successfully")

        except Exception as e:
            self.logger.error(f"Failed to save metadata: {e}")

    def list_models(self) -> List[ModelMetadata]:
        """
        List all cached models.

        Returns:
            List of ModelMetadata objects
        """
        return list(self.metadata.values())

    def get_model_info(self, model_name: str) -> Optional[ModelMetadata]:
        """
        Get metadata for a specific model.

        Args:
            model_name: Name of the model

        Returns:
            ModelMetadata or None if not found
        """
        return self.metadata.get(model_name)

    def is_model_cached(self, model_name: str) -> bool:
        """
        Check if model is cached locally.

        Args:
            model_name: Name of the model

        Returns:
            True if cached
        """
        if model_name not in self.metadata:
            return False

        model_path = self.metadata[model_name].model_path
        return model_path.exists()

    def get_model_path(self, model_name: str) -> Optional[Path]:
        """
        Get local path for a model.

        Args:
            model_name: Name of the model

        Returns:
            Path to model or None if not cached
        """
        if not self.is_model_cached(model_name):
            return None

        return self.metadata[model_name].model_path

    def download_model(
        self,
        model_name: str,
        progress_callback: Optional[Callable[[int, str], None]] = None,
        force: bool = False,
    ) -> Path:
        """
        Download model from HuggingFace Hub.

        Args:
            model_name: HuggingFace model identifier
            progress_callback: Callback(progress_pct, status_msg)
            force: Force re-download even if cached

        Returns:
            Path to downloaded model

        Raises:
            Exception if download fails
        """
        # Check if already cached
        if not force and self.is_model_cached(model_name):
            self.logger.info(f"Model '{model_name}' already cached")
            if progress_callback:
                progress_callback(100, "Model already cached")
            return self.get_model_path(model_name)

        try:
            # Progress update
            if progress_callback:
                progress_callback(5, f"Downloading {model_name}...")

            # Download model
            self.logger.info(f"Downloading model: {model_name}")

            # Use snapshot_download for complete model
            model_path = self.cache_dir / model_name.replace('/', '--')

            snapshot_download(
                repo_id=model_name,
                local_dir=str(model_path),
                local_dir_use_symlinks=False,
            )

            if progress_callback:
                progress_callback(80, "Download complete, validating...")

            # Calculate model size
            size_mb = self._calculate_dir_size(model_path)

            # Get model info (try to load to get max_seq_length)
            max_seq_length = 512
            try:
                temp_model = SentenceTransformer(str(model_path))
                max_seq_length = temp_model.max_seq_length
                del temp_model
            except Exception as e:
                self.logger.warning(f"Could not load model for info: {e}")

            # Create metadata
            from datetime import datetime
            metadata = ModelMetadata(
                model_name=model_name,
                model_path=model_path,
                size_mb=size_mb,
                download_date=datetime.now().isoformat(),
                max_seq_length=max_seq_length,
            )

            # Save metadata
            self.metadata[model_name] = metadata
            self._save_metadata()

            if progress_callback:
                progress_callback(100, "Download complete")

            self.logger.info(f"Model downloaded successfully: {model_name} ({size_mb:.1f} MB)")

            return model_path

        except RepositoryNotFoundError:
            error_msg = f"Model '{model_name}' not found on HuggingFace Hub"
            self.logger.error(error_msg)
            raise ValueError(error_msg)

        except HfHubHTTPError as e:
            error_msg = f"HTTP error downloading model: {e}"
            self.logger.error(error_msg)
            raise Exception(error_msg)

        except Exception as e:
            error_msg = f"Failed to download model: {e}"
            self.logger.error(error_msg)
            raise

    def load_model(
        self,
        model_name: str,
        download_if_missing: bool = True,
        progress_callback: Optional[Callable[[int, str], None]] = None,
    ) -> SentenceTransformer:
        """
        Load a SentenceTransformer model.

        Args:
            model_name: HuggingFace model identifier or local path
            download_if_missing: Download if not cached
            progress_callback: Callback for progress updates

        Returns:
            Loaded SentenceTransformer model

        Raises:
            Exception if model cannot be loaded
        """
        try:
            # Check if it's a local path
            if Path(model_name).exists():
                self.logger.info(f"Loading model from local path: {model_name}")
                if progress_callback:
                    progress_callback(50, "Loading model...")

                model = SentenceTransformer(model_name, device=self.device)

                if progress_callback:
                    progress_callback(100, "Model loaded")

                return model

            # Check if cached
            if not self.is_model_cached(model_name):
                if download_if_missing:
                    self.logger.info(f"Model not cached, downloading: {model_name}")
                    self.download_model(model_name, progress_callback)
                else:
                    raise ValueError(f"Model '{model_name}' not cached and download_if_missing=False")

            # Load from cache
            model_path = self.get_model_path(model_name)

            if progress_callback:
                progress_callback(50, "Loading model from cache...")

            self.logger.info(f"Loading model from cache: {model_path}")
            model = SentenceTransformer(str(model_path), device=self.device)

            if progress_callback:
                progress_callback(100, "Model loaded")

            self.logger.info(f"Model loaded successfully: {model_name}")

            return model

        except Exception as e:
            error_msg = f"Failed to load model '{model_name}': {e}"
            self.logger.error(error_msg)
            raise

    def delete_model(self, model_name: str) -> bool:
        """
        Delete a cached model.

        Args:
            model_name: Name of the model

        Returns:
            True if successfully deleted
        """
        if model_name not in self.metadata:
            self.logger.warning(f"Model '{model_name}' not found in metadata")
            return False

        try:
            model_path = self.metadata[model_name].model_path

            if model_path.exists():
                shutil.rmtree(model_path)
                self.logger.info(f"Deleted model directory: {model_path}")

            # Remove from metadata
            del self.metadata[model_name]
            self._save_metadata()

            self.logger.info(f"Model '{model_name}' deleted successfully")
            return True

        except Exception as e:
            self.logger.error(f"Failed to delete model: {e}")
            return False

    def _calculate_dir_size(self, path: Path) -> float:
        """
        Calculate directory size in MB.

        Args:
            path: Directory path

        Returns:
            Size in MB
        """
        total_size = 0
        for file in path.rglob('*'):
            if file.is_file():
                total_size += file.stat().st_size

        return total_size / (1024 * 1024)  # Convert to MB

    def get_device_info(self) -> Dict[str, Any]:
        """
        Get device information.

        Returns:
            Dictionary with device info
        """
        info = {
            'device': self.device,
            'cuda_available': torch.cuda.is_available(),
        }

        if torch.cuda.is_available():
            info['cuda_device_name'] = torch.cuda.get_device_name(0)
            info['cuda_device_count'] = torch.cuda.device_count()
            info['cuda_memory_total'] = torch.cuda.get_device_properties(0).total_memory / (1024**3)  # GB

        return info

    def clear_cache(self) -> bool:
        """
        Clear all cached models.

        Returns:
            True if successful
        """
        try:
            for model_name in list(self.metadata.keys()):
                self.delete_model(model_name)

            self.logger.info("Cache cleared successfully")
            return True

        except Exception as e:
            self.logger.error(f"Failed to clear cache: {e}")
            return False
