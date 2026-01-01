"""
Data completeness scorer for RAG++ system.
"""

from typing import List
from models.schemas import EvidenceObject
from utils.logger import get_logger

logger = get_logger(__name__)


class CompletenessScorer:
    """Computes data completeness score based on evidence quality."""
    
    def compute_completeness(self, evidence_objects: List[EvidenceObject]) -> float:
        """
        Compute completeness score (0.0 to 1.0) based on:
        - Presence of change values
        - Evidence confidence levels
        - Support text quality
        """
        if not evidence_objects:
            return 0.0
        
        scores = []
        
        for evidence in evidence_objects:
            evidence_score = 0.0
            
            # Has change value (0.3 weight)
            if evidence.change is not None:
                evidence_score += 0.3
            
            # High confidence (0.4 weight)
            evidence_score += evidence.confidence * 0.4
            
            # Quality support text (0.3 weight)
            if evidence.support and len(evidence.support) > 20:
                evidence_score += 0.3
            
            scores.append(evidence_score)
        
        completeness = sum(scores) / len(scores)
        
        logger.info("Completeness score computed",
                   evidence_count=len(evidence_objects),
                   score=completeness)
        
        return completeness
