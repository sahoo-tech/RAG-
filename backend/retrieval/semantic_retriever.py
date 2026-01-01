"""
Semantic retrieval using FAISS vector store and embeddings.
"""

from typing import List, Optional
import numpy as np
from sentence_transformers import SentenceTransformer
from models.schemas import EvidenceObject, SubQuestion
from config import get_settings
from utils.logger import get_logger
import time

logger = get_logger(__name__)
settings = get_settings()


class SemanticRetriever:
    """Retrieves relevant information using semantic similarity."""
    
    def __init__(self):
        self.model = SentenceTransformer(settings.embedding_model)
        self.knowledge_base: List[dict] = []
        self.embeddings: Optional[np.ndarray] = None
        logger.info("SemanticRetriever initialized", model=settings.embedding_model)
    
    def add_knowledge(self, text: str, metadata: dict):
        """Add a piece of knowledge to the semantic store."""
        self.knowledge_base.append({
            "text": text,
            "metadata": metadata
        })
        # Recompute embeddings
        self._compute_embeddings()
    
    def _compute_embeddings(self):
        """Compute embeddings for all knowledge base entries."""
        if not self.knowledge_base:
            return
        
        texts = [item["text"] for item in self.knowledge_base]
        self.embeddings = self.model.encode(texts, convert_to_numpy=True)
        logger.info("Embeddings computed", count=len(texts))
    
    def retrieve(self, sub_question: SubQuestion, top_k: int = 5) -> List[EvidenceObject]:
        """
        Retrieve relevant evidence using semantic similarity.
        """
        start_time = time.time()
        
        if not self.knowledge_base or self.embeddings is None:
            logger.warning("No knowledge base available for semantic retrieval")
            return []
        
        # Encode query
        query_embedding = self.model.encode([sub_question.question], convert_to_numpy=True)
        
        # Compute similarities
        similarities = np.dot(self.embeddings, query_embedding.T).flatten()
        
        # Get top-k indices
        top_indices = np.argsort(similarities)[-top_k:][::-1]
        
        # Filter by threshold
        evidence_objects = []
        for idx in top_indices:
            if similarities[idx] >= settings.semantic_similarity_threshold:
                item = self.knowledge_base[idx]
                evidence = EvidenceObject(
                    metric=item["metadata"].get("metric", "unknown"),
                    segment=item["metadata"].get("segment", "all"),
                    time_window=item["metadata"].get("time_window", "unknown"),
                    value=item["metadata"].get("value", 0.0),
                    change=item["metadata"].get("change"),
                    support=item["text"],
                    source="semantic",
                    confidence=float(similarities[idx])
                )
                evidence_objects.append(evidence)
        
        elapsed = (time.time() - start_time) * 1000
        logger.info("Semantic retrieval complete",
                   query=sub_question.question[:50],
                   retrieved=len(evidence_objects),
                   time_ms=elapsed)
        
        return evidence_objects
    
    def initialize_sample_knowledge(self):
        """Initialize with sample analytical knowledge."""
        sample_knowledge = [
            {
                "text": "Revenue increased by 15.5% in Q1 2024 compared to Q4 2023 for enterprise customers",
                "metadata": {
                    "metric": "revenue",
                    "segment": "enterprise",
                    "time_window": "Q1_2024",
                    "value": 125000.0,
                    "change": 15.5
                }
            },
            {
                "text": "User engagement dropped by 8% in the mobile app during last week",
                "metadata": {
                    "metric": "engagement",
                    "segment": "mobile",
                    "time_window": "last_7_days",
                    "value": 0.72,
                    "change": -8.0
                }
            },
            {
                "text": "Customer retention rate for premium users is 92% over the last month",
                "metadata": {
                    "metric": "retention",
                    "segment": "premium",
                    "time_window": "last_30_days",
                    "value": 0.92,
                    "change": 2.5
                }
            },
            {
                "text": "Average order value increased from $45 to $52 for returning customers",
                "metadata": {
                    "metric": "average_order_value",
                    "segment": "returning",
                    "time_window": "last_30_days",
                    "value": 52.0,
                    "change": 15.6
                }
            },
            {
                "text": "Conversion rate for free trial users is 18% across all segments",
                "metadata": {
                    "metric": "conversion",
                    "segment": "trial",
                    "time_window": "last_30_days",
                    "value": 0.18,
                    "change": None
                }
            }
        ]
        
        for item in sample_knowledge:
            self.add_knowledge(item["text"], item["metadata"])
        
        logger.info("Sample knowledge initialized", count=len(sample_knowledge))
