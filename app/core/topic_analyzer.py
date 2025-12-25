"""
BERTopic Pro - Topic Analyzer
Wrapper for BERTopic with parameter management and persistence.
"""

import joblib
import hashlib
from pathlib import Path
from typing import Optional, List, Dict, Any, Callable, Tuple
import pandas as pd
import numpy as np
from bertopic import BERTopic
from sentence_transformers import SentenceTransformer
from sklearn.feature_extraction.text import CountVectorizer
from umap import UMAP
from hdbscan import HDBSCAN
from app.utils.logger import get_logger
from app.core.model_manager import ModelManager
import config


logger = get_logger(__name__)


class TopicModelParams:
    """Container for BERTopic parameters."""

    def __init__(
        self,
        # Embedding params
        embedding_model: str = config.DEFAULT_EMBEDDING_MODEL,

        # UMAP params
        umap_n_neighbors: int = config.DEFAULT_UMAP_N_NEIGHBORS,
        umap_n_components: int = config.DEFAULT_UMAP_N_COMPONENTS,
        umap_min_dist: float = config.DEFAULT_UMAP_MIN_DIST,
        umap_metric: str = 'cosine',

        # HDBSCAN params
        hdbscan_min_cluster_size: int = config.DEFAULT_HDBSCAN_MIN_CLUSTER_SIZE,
        hdbscan_min_samples: int = config.DEFAULT_HDBSCAN_MIN_SAMPLES,
        hdbscan_metric: str = 'euclidean',

        # c-TF-IDF params
        top_n_words: int = config.DEFAULT_TOP_N_WORDS,
        ngram_range: Tuple[int, int] = (1, 2),
        min_topic_size: int = config.DEFAULT_MIN_TOPIC_SIZE,

        # Other params
        nr_topics: Optional[int] = None,
        calculate_probabilities: bool = False,
        verbose: bool = True,
    ):
        # Embedding
        self.embedding_model = embedding_model

        # UMAP
        self.umap_n_neighbors = umap_n_neighbors
        self.umap_n_components = umap_n_components
        self.umap_min_dist = umap_min_dist
        self.umap_metric = umap_metric

        # HDBSCAN
        self.hdbscan_min_cluster_size = hdbscan_min_cluster_size
        self.hdbscan_min_samples = hdbscan_min_samples
        self.hdbscan_metric = hdbscan_metric

        # c-TF-IDF
        self.top_n_words = top_n_words
        self.ngram_range = ngram_range
        self.min_topic_size = min_topic_size

        # Other
        self.nr_topics = nr_topics
        self.calculate_probabilities = calculate_probabilities
        self.verbose = verbose

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            'embedding_model': self.embedding_model,
            'umap_n_neighbors': self.umap_n_neighbors,
            'umap_n_components': self.umap_n_components,
            'umap_min_dist': self.umap_min_dist,
            'umap_metric': self.umap_metric,
            'hdbscan_min_cluster_size': self.hdbscan_min_cluster_size,
            'hdbscan_min_samples': self.hdbscan_min_samples,
            'hdbscan_metric': self.hdbscan_metric,
            'top_n_words': self.top_n_words,
            'ngram_range': self.ngram_range,
            'min_topic_size': self.min_topic_size,
            'nr_topics': self.nr_topics,
            'calculate_probabilities': self.calculate_probabilities,
            'verbose': self.verbose,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'TopicModelParams':
        """Create from dictionary."""
        return cls(**data)


class TopicAnalyzer:
    """
    Wrapper for BERTopic with extended functionality.

    Features:
    - Parameter management
    - Model persistence
    - Embedding caching
    - Progress tracking
    - Result analysis
    """

    def __init__(
        self,
        model_manager: Optional[ModelManager] = None,
        cache_dir: Optional[Path] = None,
    ):
        """
        Initialize topic analyzer.

        Args:
            model_manager: ModelManager instance (creates new if None)
            cache_dir: Directory for caching (default: config.MODEL_DIR)
        """
        self.logger = get_logger(self.__class__.__name__)

        # Model manager
        self.model_manager = model_manager or ModelManager()

        # Cache directory
        self.cache_dir = cache_dir or config.MODEL_DIR / 'bertopic'
        self.cache_dir.mkdir(parents=True, exist_ok=True)

        # Embedding cache
        self.embedding_cache_dir = config.EMBEDDINGS_CACHE_DIR
        self.embedding_cache_dir.mkdir(parents=True, exist_ok=True)

        # BERTopic model
        self.model: Optional[BERTopic] = None
        self.params: Optional[TopicModelParams] = None

        # Training data references
        self.documents: Optional[List[str]] = None
        self.embeddings: Optional[np.ndarray] = None
        self.topics: Optional[List[int]] = None
        self.probabilities: Optional[np.ndarray] = None

        self.logger.info("TopicAnalyzer initialized")

    def _create_umap_model(self, params: TopicModelParams) -> UMAP:
        """Create UMAP model from parameters."""
        return UMAP(
            n_neighbors=params.umap_n_neighbors,
            n_components=params.umap_n_components,
            min_dist=params.umap_min_dist,
            metric=params.umap_metric,
            random_state=42,
            verbose=params.verbose,
        )

    def _create_hdbscan_model(self, params: TopicModelParams) -> HDBSCAN:
        """Create HDBSCAN model from parameters."""
        return HDBSCAN(
            min_cluster_size=params.hdbscan_min_cluster_size,
            min_samples=params.hdbscan_min_samples,
            metric=params.hdbscan_metric,
            prediction_data=True,
        )

    def _create_vectorizer_model(self, params: TopicModelParams) -> CountVectorizer:
        """Create CountVectorizer for c-TF-IDF."""
        return CountVectorizer(
            ngram_range=params.ngram_range,
            stop_words=None,  # Stopwords already removed in preprocessing
        )

    def _get_embedding_cache_path(self, documents: List[str]) -> Path:
        """
        Get cache path for embeddings based on document hash.

        Args:
            documents: List of documents

        Returns:
            Path to cache file
        """
        # Create hash from documents
        doc_string = ''.join(documents[:100])  # Use first 100 docs for hash
        doc_hash = hashlib.md5(doc_string.encode()).hexdigest()

        return self.embedding_cache_dir / f"embeddings_{doc_hash}.joblib"

    def _load_cached_embeddings(self, documents: List[str]) -> Optional[np.ndarray]:
        """
        Load cached embeddings if available.

        Args:
            documents: List of documents

        Returns:
            Embeddings array or None if not cached
        """
        cache_path = self._get_embedding_cache_path(documents)

        if cache_path.exists():
            try:
                embeddings = joblib.load(cache_path)
                self.logger.info(f"Loaded embeddings from cache: {cache_path.name}")
                return embeddings
            except Exception as e:
                self.logger.warning(f"Failed to load cached embeddings: {e}")
                return None

        return None

    def _save_embeddings_cache(self, documents: List[str], embeddings: np.ndarray) -> None:
        """
        Save embeddings to cache.

        Args:
            documents: List of documents
            embeddings: Embeddings array
        """
        cache_path = self._get_embedding_cache_path(documents)

        try:
            joblib.dump(embeddings, cache_path)
            self.logger.info(f"Saved embeddings to cache: {cache_path.name}")
        except Exception as e:
            self.logger.warning(f"Failed to save embeddings cache: {e}")

    def generate_embeddings(
        self,
        documents: List[str],
        embedding_model_name: str,
        use_cache: bool = True,
        progress_callback: Optional[Callable[[int, str], None]] = None,
    ) -> np.ndarray:
        """
        Generate embeddings for documents.

        Args:
            documents: List of documents
            embedding_model_name: Name of embedding model
            use_cache: Whether to use cached embeddings
            progress_callback: Callback(progress_pct, status_msg)

        Returns:
            Embeddings array
        """
        # Check cache
        if use_cache:
            cached_embeddings = self._load_cached_embeddings(documents)
            if cached_embeddings is not None:
                if progress_callback:
                    progress_callback(100, "Loaded embeddings from cache")
                return cached_embeddings

        # Load embedding model
        if progress_callback:
            progress_callback(10, "Loading embedding model...")

        embedding_model = self.model_manager.load_model(
            embedding_model_name,
            download_if_missing=True,
        )

        # Generate embeddings
        if progress_callback:
            progress_callback(30, f"Generating embeddings for {len(documents)} documents...")

        self.logger.info(f"Generating embeddings for {len(documents)} documents")

        embeddings = embedding_model.encode(
            documents,
            show_progress_bar=True,
            convert_to_numpy=True,
        )

        # Convert to float32 to save memory
        embeddings = embeddings.astype(np.float32)

        if progress_callback:
            progress_callback(90, "Embeddings generated")

        # Save to cache
        if use_cache:
            self._save_embeddings_cache(documents, embeddings)

        if progress_callback:
            progress_callback(100, f"Generated embeddings: {embeddings.shape}")

        self.logger.info(f"Embeddings generated: {embeddings.shape}")

        return embeddings

    def train(
        self,
        documents: List[str],
        embeddings: Optional[np.ndarray] = None,
        params: Optional[TopicModelParams] = None,
        progress_callback: Optional[Callable[[int, str], None]] = None,
    ) -> Tuple[List[int], Optional[np.ndarray]]:
        """
        Train BERTopic model.

        Args:
            documents: List of documents (preprocessed text)
            embeddings: Pre-computed embeddings (if None, will generate)
            params: Model parameters (uses defaults if None)
            progress_callback: Callback(progress_pct, status_msg)

        Returns:
            Tuple of (topics, probabilities)
        """
        if params is None:
            params = TopicModelParams()

        self.params = params

        try:
            # Generate embeddings if not provided
            if embeddings is None:
                if progress_callback:
                    progress_callback(0, "Generating embeddings...")

                embeddings = self.generate_embeddings(
                    documents,
                    params.embedding_model,
                    use_cache=True,
                    progress_callback=lambda pct, msg: progress_callback(int(pct * 0.3), msg) if progress_callback else None,
                )

            if progress_callback:
                progress_callback(30, "Creating BERTopic model...")

            # Create sub-models
            umap_model = self._create_umap_model(params)
            hdbscan_model = self._create_hdbscan_model(params)
            vectorizer_model = self._create_vectorizer_model(params)

            # Create BERTopic model
            self.model = BERTopic(
                umap_model=umap_model,
                hdbscan_model=hdbscan_model,
                vectorizer_model=vectorizer_model,
                top_n_words=params.top_n_words,
                nr_topics=params.nr_topics,
                min_topic_size=params.min_topic_size,
                calculate_probabilities=params.calculate_probabilities,
                verbose=params.verbose,
            )

            if progress_callback:
                progress_callback(40, "Fitting model...")

            self.logger.info("Training BERTopic model...")

            # Fit model
            topics, probabilities = self.model.fit_transform(documents, embeddings)

            # Store references
            self.documents = documents
            self.embeddings = embeddings
            self.topics = topics
            self.probabilities = probabilities

            if progress_callback:
                progress_callback(100, f"Training complete: {len(set(topics)) - 1} topics found")

            self.logger.info(f"Training complete: {len(set(topics)) - 1} topics (excluding outliers)")

            return topics, probabilities

        except Exception as e:
            error_msg = f"Training failed: {e}"
            self.logger.error(error_msg)
            raise

    def get_topic_info(self) -> Optional[pd.DataFrame]:
        """
        Get topic information DataFrame.

        Returns:
            DataFrame with topic info or None if model not trained
        """
        if self.model is None:
            return None

        return self.model.get_topic_info()

    def get_topic_words(self, topic_id: int, top_n: int = 10) -> List[Tuple[str, float]]:
        """
        Get top words for a topic.

        Args:
            topic_id: Topic ID
            top_n: Number of top words

        Returns:
            List of (word, score) tuples
        """
        if self.model is None:
            return []

        topic = self.model.get_topic(topic_id)
        return topic[:top_n] if topic else []

    def get_document_topics(self) -> Optional[List[int]]:
        """Get topic assignments for all documents."""
        return self.topics

    def save_model(self, save_path: Optional[Path] = None, name: str = "bertopic_model") -> Path:
        """
        Save BERTopic model and metadata.

        Args:
            save_path: Directory to save (default: cache_dir)
            name: Model name

        Returns:
            Path to saved model directory
        """
        if self.model is None:
            raise ValueError("No model to save")

        save_path = save_path or self.cache_dir
        model_dir = save_path / name
        model_dir.mkdir(parents=True, exist_ok=True)

        try:
            # Save BERTopic model
            model_file = model_dir / "model"
            self.model.save(str(model_file), serialization="pickle", save_ctfidf=True, save_embedding_model=False)

            # Save parameters
            params_file = model_dir / "params.json"
            import json
            with open(params_file, 'w', encoding='utf-8') as f:
                json.dump(self.params.to_dict(), f, indent=2)

            # Save topics
            if self.topics is not None:
                topics_file = model_dir / "topics.joblib"
                joblib.dump(self.topics, topics_file)

            # Save embeddings (optional)
            if self.embeddings is not None:
                embeddings_file = model_dir / "embeddings.joblib"
                joblib.dump(self.embeddings, embeddings_file)

            self.logger.info(f"Model saved to: {model_dir}")

            return model_dir

        except Exception as e:
            error_msg = f"Failed to save model: {e}"
            self.logger.error(error_msg)
            raise

    def load_model(self, model_path: Path) -> None:
        """
        Load BERTopic model and metadata.

        Args:
            model_path: Path to model directory
        """
        try:
            # Load BERTopic model
            model_file = model_path / "model"
            self.model = BERTopic.load(str(model_file))

            # Load parameters
            params_file = model_path / "params.json"
            if params_file.exists():
                import json
                with open(params_file, 'r', encoding='utf-8') as f:
                    params_dict = json.load(f)
                self.params = TopicModelParams.from_dict(params_dict)

            # Load topics
            topics_file = model_path / "topics.joblib"
            if topics_file.exists():
                self.topics = joblib.load(topics_file)

            # Load embeddings
            embeddings_file = model_path / "embeddings.joblib"
            if embeddings_file.exists():
                self.embeddings = joblib.load(embeddings_file)

            self.logger.info(f"Model loaded from: {model_path}")

        except Exception as e:
            error_msg = f"Failed to load model: {e}"
            self.logger.error(error_msg)
            raise
