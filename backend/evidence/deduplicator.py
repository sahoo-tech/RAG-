"""
Evidence deduplicator for RAG++ system.
Removes duplicate or highly similar evidence objects.
"""

from typing import List
import numpy as np
from sentence_transformers import SentenceTransformer
from models.schemas import EvidenceObject
from config import get_settings
from utils.logger import get_logger
from utils.helpers import generate_hash

logger = get_logger(__name__)
settings = get_settings()


class EvidenceDeduplicator:
    """Deduplicates evidence objects based on semantic similarity."""
    
    def __init__(self):
        self.model = SentenceTransformer(settings.embedding_model)
        self.dedup_threshold = settings.evidence_dedup_threshold
        logger.info("EvidenceDeduplicator initialized")
    
    def deduplicate(self, evidence_list: List[EvidenceObject]) -> List[EvidenceObject]:
        """
        Remove duplicate evidence objects.
        Uses both exact matching and semantic similarity.
        """
        if not evidence_list:
            return []
        
        # First pass: exact deduplication by hash
        unique_by_hash = self._deduplicate_by_hash(evidence_list)
        
        # Second pass: semantic deduplication
        unique_evidence = self._deduplicate_by_similarity(unique_by_hash)
        
        logger.info("Evidence deduplication complete",
                   original=len(evidence_list),
                   after_hash=len(unique_by_hash),
                   final=len(unique_evidence))
        
        return unique_evidence
    
    def _deduplicate_by_hash(self, evidence_list: List[EvidenceObject]) -> List[EvidenceObject]:
        """Remove exact duplicates using hash."""
        seen_hashes = set()
        unique = []
        
        for evidence in evidence_list:
            # Create hash from key fields
            hash_data = {
                "metric": evidence.metric,
                "segment": evidence.segment,
                "time_window": evidence.time_window,
                "value": round(evidence.value, 2)
            }
            evidence_hash = generate_hash(hash_data)
            
            if evidence_hash not in seen_hashes:
                seen_hashes.add(evidence_hash)
                unique.append(evidence)
        
        return unique
    
    def _deduplicate_by_similarity(self, evidence_list: List[EvidenceObject]) -> List[EvidenceObject]:
        """Remove semantically similar evidence."""
        if len(evidence_list) <= 1:
            return evidence_list
        
        # Create support text embeddings
        support_texts = [e.support for e in evidence_list]
        embeddings = self.model.encode(support_texts, convert_to_numpy=True)
        
        # Compute similarity matrix
        similarity_matrix = np.dot(embeddings, embeddings.T)
        
        # Normalize
        norms = np.linalg.norm(embeddings, axis=1)
        similarity_matrix = similarity_matrix / (norms[:, None] * norms[None, :])
        
        # Mark duplicates
        keep_indices = []
        removed_indices = set()
        
        for i in range(len(evidence_list)):
            if i in removed_indices:
                continue
            
            keep_indices.append(i)
            
            # Mark similar items as duplicates
            for j in range(i + 1, len(evidence_list)):
                if j not in removed_indices and similarity_matrix[i, j] >= self.dedup_threshold:
                    # Keep the one with higher confidence
                    if evidence_list[j].confidence > evidence_list[i].confidence:
                        keep_indices[-1] = j
                        removed_indices.add(i)
                    else:
                        removed_indices.add(j)
        
        unique_evidence = [evidence_list[i] for i in keep_indices]
        return unique_evidence
