"""
Evidence object builder for RAG++ system.
Converts retrieval outputs into standardized evidence objects.
"""

from typing import List, Dict, Any
from models.schemas import EvidenceObject
from utils.logger import get_logger

logger = get_logger(__name__)


class EvidenceBuilder:
    """Builds standardized evidence objects from various sources."""
    
    @staticmethod
    def from_dict(data: Dict[str, Any]) -> EvidenceObject:
        """Create evidence object from dictionary."""
        return EvidenceObject(**data)
    
    @staticmethod
    def from_dataframe_row(row: Dict[str, Any], metric: str, segment: str) -> EvidenceObject:
        """Create evidence object from a dataframe row."""
        return EvidenceObject(
            metric=metric,
            segment=segment,
            time_window=row.get('time_window', 'unknown'),
            value=float(row.get('value', 0)),
            change=row.get('change'),
            support=row.get('support', f"{metric} for {segment}"),
            source='structured',
            confidence=row.get('confidence', 0.9)
        )
    
    @staticmethod
    def merge_evidence(evidence_list: List[EvidenceObject]) -> List[EvidenceObject]:
        """
        Merge similar evidence objects to reduce redundancy.
        Groups by metric, segment, and time_window.
        """
        merged = {}
        
        for evidence in evidence_list:
            key = (evidence.metric, evidence.segment, evidence.time_window)
            
            if key not in merged:
                merged[key] = evidence
            else:
                # If duplicate, keep the one with higher confidence
                if evidence.confidence > merged[key].confidence:
                    merged[key] = evidence
        
        return list(merged.values())
    
    @staticmethod
    def enrich_evidence(evidence: EvidenceObject, additional_context: str) -> EvidenceObject:
        """Add additional context to evidence support text."""
        evidence.support = f"{evidence.support}. {additional_context}"
        return evidence
