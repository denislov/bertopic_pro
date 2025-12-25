"""
BERTopic Pro - Embedding Worker
Background worker for generating embeddings.
"""

from typing import List, Optional
import numpy as np
from app.core.workers.base_worker import BaseWorker
from app.core.topic_analyzer import TopicAnalyzer


class EmbeddingWorker(BaseWorker):
    """
    Worker thread for generating embeddings.

    Generates document embeddings in the background with progress tracking.
    """

    def __init__(
        self,
        documents: List[str],
        embedding_model_name: str,
        topic_analyzer: TopicAnalyzer,
        use_cache: bool = True,
    ):
        """
        Initialize embedding worker.

        Args:
            documents: List of documents to embed
            embedding_model_name: Name of embedding model
            topic_analyzer: TopicAnalyzer instance
            use_cache: Whether to use embedding cache
        """
        super().__init__()

        self.documents = documents
        self.embedding_model_name = embedding_model_name
        self.topic_analyzer = topic_analyzer
        self.use_cache = use_cache

    def run(self):
        """Generate embeddings."""
        try:
            self.emit_status("Starting embedding generation...")

            def progress_callback(pct, msg):
                if not self._is_cancelled:
                    self.emit_progress(pct, msg)

            # Generate embeddings
            embeddings = self.topic_analyzer.generate_embeddings(
                documents=self.documents,
                embedding_model_name=self.embedding_model_name,
                use_cache=self.use_cache,
                progress_callback=progress_callback,
            )

            if self._is_cancelled:
                self.emit_status("Embedding generation cancelled")
                return

            # Emit result
            self.emit_finished(embeddings)

        except Exception as e:
            self.emit_error(e)
