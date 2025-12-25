"""
BERTopic Pro - Visualization Generator
Generates interactive Plotly visualizations for BERTopic models.
"""

from pathlib import Path
from typing import Optional, List, Dict, Any
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from app.utils.logger import get_logger
from app.core.topic_analyzer import TopicAnalyzer
import config


logger = get_logger(__name__)


class VisualizationGenerator:
    """
    Generates interactive visualizations for BERTopic models.

    Features:
    - Intertopic distance map
    - Hierarchical clustering dendrogram
    - Topic word scores bar charts
    - Document projections
    - Topics over time (if timestamps available)
    - Chinese font support
    - HTML export
    """

    def __init__(
        self,
        topic_analyzer: TopicAnalyzer,
        font_family: str = "Noto Sans CJK SC, Microsoft YaHei, SimHei, sans-serif",
    ):
        """
        Initialize visualization generator.

        Args:
            topic_analyzer: Trained TopicAnalyzer instance
            font_family: Font family for Chinese text support
        """
        self.logger = get_logger(self.__class__.__name__)

        if topic_analyzer.model is None:
            raise ValueError("TopicAnalyzer must have a trained model")

        self.topic_analyzer = topic_analyzer
        self.model = topic_analyzer.model
        self.font_family = font_family

        # Default layout settings
        self.default_layout = {
            'font': {'family': font_family, 'size': 12},
            'template': 'plotly_white',
            'hovermode': 'closest',
        }

        self.logger.info("VisualizationGenerator initialized")

    def _apply_layout(self, fig: go.Figure, title: str, **kwargs) -> go.Figure:
        """
        Apply default layout to figure.

        Args:
            fig: Plotly figure
            title: Chart title
            **kwargs: Additional layout options

        Returns:
            Updated figure
        """
        layout_updates = {
            'title': {'text': title, 'font': {'size': 16, 'family': self.font_family}},
            **self.default_layout,
            **kwargs,
        }

        fig.update_layout(**layout_updates)

        return fig

    def visualize_topics(
        self,
        top_n_topics: Optional[int] = None,
        width: int = 800,
        height: int = 800,
    ) -> go.Figure:
        """
        Generate intertopic distance map.

        Args:
            top_n_topics: Number of topics to show (None for all)
            width: Figure width
            height: Figure height

        Returns:
            Plotly figure
        """
        try:
            self.logger.info("Generating intertopic distance map...")

            # Use BERTopic's built-in visualization
            fig = self.model.visualize_topics(
                top_n_topics=top_n_topics,
                width=width,
                height=height,
            )

            # Apply custom layout
            fig = self._apply_layout(
                fig,
                title="主题间距离图 (Intertopic Distance Map)",
                width=width,
                height=height,
            )

            self.logger.info("Intertopic distance map generated")

            return fig

        except Exception as e:
            self.logger.error(f"Failed to generate intertopic distance map: {e}")
            raise

    def visualize_hierarchy(
        self,
        orientation: str = "left",
        width: int = 1000,
        height: int = 600,
    ) -> go.Figure:
        """
        Generate hierarchical clustering dendrogram.

        Args:
            orientation: Tree orientation ('left', 'top', 'right', 'bottom')
            width: Figure width
            height: Figure height

        Returns:
            Plotly figure
        """
        try:
            self.logger.info("Generating hierarchical clustering...")

            # Use BERTopic's built-in visualization
            fig = self.model.visualize_hierarchy(
                orientation=orientation,
                width=width,
                height=height,
            )

            # Apply custom layout
            fig = self._apply_layout(
                fig,
                title="主题层次聚类 (Hierarchical Clustering)",
                width=width,
                height=height,
            )

            self.logger.info("Hierarchical clustering generated")

            return fig

        except Exception as e:
            self.logger.error(f"Failed to generate hierarchical clustering: {e}")
            raise

    def visualize_barchart(
        self,
        topics: Optional[List[int]] = None,
        top_n_topics: int = 8,
        n_words: int = 10,
        width: int = 800,
        height: int = 600,
    ) -> go.Figure:
        """
        Generate topic word scores bar chart.

        Args:
            topics: List of topic IDs to show (None for top topics)
            top_n_topics: Number of topics to show if topics is None
            n_words: Number of words per topic
            width: Figure width
            height: Figure height

        Returns:
            Plotly figure
        """
        try:
            self.logger.info("Generating topic word scores bar chart...")

            # Use BERTopic's built-in visualization
            fig = self.model.visualize_barchart(
                topics=topics,
                top_n_topics=top_n_topics,
                n_words=n_words,
                width=width,
                height=height,
            )

            # Apply custom layout
            fig = self._apply_layout(
                fig,
                title="主题关键词得分 (Topic Word Scores)",
                width=width,
                height=height,
            )

            self.logger.info("Topic word scores bar chart generated")

            return fig

        except Exception as e:
            self.logger.error(f"Failed to generate topic word scores: {e}")
            raise

    def visualize_documents(
        self,
        docs: Optional[List[str]] = None,
        topics: Optional[List[int]] = None,
        embeddings: Optional[np.ndarray] = None,
        reduced_embeddings: Optional[np.ndarray] = None,
        sample: Optional[float] = None,
        hide_annotations: bool = False,
        width: int = 1000,
        height: int = 800,
    ) -> go.Figure:
        """
        Generate document projection visualization.

        Args:
            docs: List of documents (uses stored if None)
            topics: Topic assignments (uses stored if None)
            embeddings: Document embeddings (uses stored if None)
            reduced_embeddings: Reduced embeddings for visualization
            sample: Sample fraction of documents (e.g., 0.1 for 10%)
            hide_annotations: Whether to hide topic annotations
            width: Figure width
            height: Figure height

        Returns:
            Plotly figure
        """
        try:
            self.logger.info("Generating document projection...")

            # Use stored data if not provided
            if docs is None:
                docs = self.topic_analyzer.documents

            if topics is None:
                topics = self.topic_analyzer.topics

            if embeddings is None:
                embeddings = self.topic_analyzer.embeddings

            if docs is None or topics is None:
                raise ValueError("No documents or topics available for visualization")

            # Use BERTopic's built-in visualization
            fig = self.model.visualize_documents(
                docs=docs,
                topics=topics,
                embeddings=embeddings,
                reduced_embeddings=reduced_embeddings,
                sample=sample,
                hide_annotations=hide_annotations,
                width=width,
                height=height,
            )

            # Apply custom layout
            fig = self._apply_layout(
                fig,
                title="文档投影图 (Documents Projection)",
                width=width,
                height=height,
            )

            self.logger.info("Document projection generated")

            return fig

        except Exception as e:
            self.logger.error(f"Failed to generate document projection: {e}")
            raise

    def visualize_topics_over_time(
        self,
        topics_over_time: pd.DataFrame,
        top_n_topics: Optional[int] = None,
        normalize_frequency: bool = False,
        width: int = 1000,
        height: int = 600,
    ) -> go.Figure:
        """
        Generate topics over time visualization.

        Args:
            topics_over_time: DataFrame from topics_over_time()
            top_n_topics: Number of topics to show
            normalize_frequency: Whether to normalize frequencies
            width: Figure width
            height: Figure height

        Returns:
            Plotly figure
        """
        try:
            self.logger.info("Generating topics over time...")

            # Use BERTopic's built-in visualization
            fig = self.model.visualize_topics_over_time(
                topics_over_time=topics_over_time,
                top_n_topics=top_n_topics,
                normalize_frequency=normalize_frequency,
                width=width,
                height=height,
            )

            # Apply custom layout
            fig = self._apply_layout(
                fig,
                title="主题时间演化 (Topics Over Time)",
                width=width,
                height=height,
            )

            self.logger.info("Topics over time generated")

            return fig

        except Exception as e:
            self.logger.error(f"Failed to generate topics over time: {e}")
            raise

    def visualize_heatmap(
        self,
        topics: Optional[List[int]] = None,
        top_n_topics: int = 20,
        n_clusters: int = 10,
        width: int = 800,
        height: int = 800,
    ) -> go.Figure:
        """
        Generate topic similarity heatmap.

        Args:
            topics: List of topic IDs to show
            top_n_topics: Number of topics to show if topics is None
            n_clusters: Number of clusters for grouping
            width: Figure width
            height: Figure height

        Returns:
            Plotly figure
        """
        try:
            self.logger.info("Generating topic similarity heatmap...")

            # Use BERTopic's built-in visualization
            fig = self.model.visualize_heatmap(
                topics=topics,
                top_n_topics=top_n_topics,
                n_clusters=n_clusters,
                width=width,
                height=height,
            )

            # Apply custom layout
            fig = self._apply_layout(
                fig,
                title="主题相似度热力图 (Topic Similarity Heatmap)",
                width=width,
                height=height,
            )

            self.logger.info("Topic similarity heatmap generated")

            return fig

        except Exception as e:
            self.logger.error(f"Failed to generate topic similarity heatmap: {e}")
            raise

    def visualize_term_rank(
        self,
        topics: Optional[List[int]] = None,
        log_scale: bool = False,
        width: int = 800,
        height: int = 500,
    ) -> go.Figure:
        """
        Generate term rank visualization.

        Args:
            topics: List of topic IDs to show
            log_scale: Whether to use log scale
            width: Figure width
            height: Figure height

        Returns:
            Plotly figure
        """
        try:
            self.logger.info("Generating term rank visualization...")

            # Use BERTopic's built-in visualization
            fig = self.model.visualize_term_rank(
                topics=topics,
                log_scale=log_scale,
                width=width,
                height=height,
            )

            # Apply custom layout
            fig = self._apply_layout(
                fig,
                title="主题词排序 (Term Rank)",
                width=width,
                height=height,
            )

            self.logger.info("Term rank visualization generated")

            return fig

        except Exception as e:
            self.logger.error(f"Failed to generate term rank: {e}")
            raise

    def save_figure(
        self,
        fig: go.Figure,
        filepath: Path,
        format: str = "html",
        include_plotlyjs: str = "cdn",
    ) -> None:
        """
        Save figure to file.

        Args:
            fig: Plotly figure
            filepath: Output file path
            format: Output format ('html', 'png', 'jpeg', 'svg', 'pdf')
            include_plotlyjs: How to include plotly.js ('cdn', True, False)
        """
        try:
            filepath = Path(filepath)

            if format == "html":
                fig.write_html(
                    str(filepath),
                    include_plotlyjs=include_plotlyjs,
                    config={'displayModeBar': True, 'responsive': True},
                )

                self.logger.info(f"Figure saved to HTML: {filepath}")

            elif format in ["png", "jpeg", "svg", "pdf"]:
                # Requires kaleido
                fig.write_image(str(filepath), format=format)

                self.logger.info(f"Figure saved to {format.upper()}: {filepath}")

            else:
                raise ValueError(f"Unsupported format: {format}")

        except Exception as e:
            self.logger.error(f"Failed to save figure: {e}")
            raise

    def get_available_visualizations(self) -> List[Dict[str, Any]]:
        """
        Get list of available visualizations.

        Returns:
            List of visualization metadata
        """
        visualizations = [
            {
                'id': 'topics',
                'name': '主题间距离图',
                'description': '显示主题在二维空间中的分布和相似度',
                'method': self.visualize_topics,
            },
            {
                'id': 'hierarchy',
                'name': '主题层次聚类',
                'description': '显示主题的层次结构和关系',
                'method': self.visualize_hierarchy,
            },
            {
                'id': 'barchart',
                'name': '主题关键词得分',
                'description': '显示每个主题的关键词及其重要性得分',
                'method': self.visualize_barchart,
            },
            {
                'id': 'documents',
                'name': '文档投影图',
                'description': '显示文档在降维空间中的分布',
                'method': self.visualize_documents,
            },
            {
                'id': 'heatmap',
                'name': '主题相似度热力图',
                'description': '显示主题之间的相似度矩阵',
                'method': self.visualize_heatmap,
            },
            {
                'id': 'term_rank',
                'name': '主题词排序',
                'description': '显示主题词的排序和分布',
                'method': self.visualize_term_rank,
            },
        ]

        # Add topics over time if timestamps are available
        if self.topic_analyzer.documents is not None:
            visualizations.append({
                'id': 'topics_over_time',
                'name': '主题时间演化',
                'description': '显示主题随时间的变化趋势',
                'method': self.visualize_topics_over_time,
            })

        return visualizations
