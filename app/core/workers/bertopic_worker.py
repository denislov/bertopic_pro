"""
BERTopic Pro - BERTopic Worker
Background worker for BERTopic training.
"""

from typing import List, Optional
import numpy as np
from app.core.workers.base_worker import BaseWorker
from app.core.topic_analyzer import TopicAnalyzer, TopicModelParams


class BertopicWorker(BaseWorker):
    """
    Worker thread for BERTopic training.

    Trains BERTopic model in the background with progress tracking.
    """

    def __init__(
        self,
        documents: List[str],
        topic_analyzer: TopicAnalyzer,
        params: Optional[TopicModelParams] = None,
        embeddings: Optional[np.ndarray] = None,
    ):
        """
        Initialize BERTopic worker.

        Args:
            documents: List of documents (preprocessed)
            topic_analyzer: TopicAnalyzer instance
            params: Model parameters (uses defaults if None)
            embeddings: Pre-computed embeddings (generates if None)
        """
        super().__init__()

        self.documents = documents
        self.topic_analyzer = topic_analyzer
        self.params = params
        self.embeddings = embeddings

    def run(self):
        """Train BERTopic model."""
        try:
            self.emit_status("Starting BERTopic training...")
            self.emit_progress(0, "Initializing...")

            def progress_callback(pct, msg):
                if not self._is_cancelled:
                    self.emit_progress(pct, msg)
                    self.emit_status(msg)

            # Train model
            topics, probabilities = self.topic_analyzer.train(
                documents=self.documents,
                embeddings=self.embeddings,
                params=self.params,
                progress_callback=progress_callback,
            )

            if self._is_cancelled:
                self.emit_status("Training cancelled")
                return

            # Prepare result
            result = {
                'topics': topics,
                'probabilities': probabilities,
                'model': self.topic_analyzer.model,
                'topic_analyzer': self.topic_analyzer,
            }

            # Emit result
            self.emit_finished(result)

        except Exception as e:
            self.emit_error(e)
