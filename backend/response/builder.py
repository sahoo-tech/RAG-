"""
Response builder for RAG++ system.
"""

from datetime import datetime
from models.schemas import (
    FinalResponse, ConfidenceScore, EvidenceObject,
    QueryDecomposition
)
from typing import List
from utils.logger import get_logger

logger = get_logger(__name__)


class ResponseBuilder:
    """Builds final responses with evidence references and confidence labels."""
    
    def build_response(
        self,
        query: str,
        answer: str,
        confidence: ConfidenceScore,
        evidence_objects: List[EvidenceObject],
        processing_time_ms: float
    ) -> FinalResponse:
        """
        Build the final response object.
        """
        response = FinalResponse(
            query=query,
            answer=answer,
            confidence=confidence,
            evidence_count=len(evidence_objects),
            processing_time_ms=processing_time_ms,
            timestamp=datetime.now()
        )
        
        logger.info("Response built",
                   query=query[:50],
                   evidence_count=len(evidence_objects),
                   confidence_level=confidence.confidence_level.value)
        
        return response
    
    def format_answer_with_confidence(
        self,
        answer: str,
        confidence: ConfidenceScore
    ) -> str:
        """
        Format answer with confidence label and reasoning.
        """
        formatted = f"{answer}\n\n"
        formatted += f"**Confidence Level**: {confidence.confidence_level.value.replace('_', ' ').title()}\n"
        formatted += f"**Reasoning**: {confidence.reasoning}\n"
        formatted += f"**Coverage Score**: {confidence.coverage_score:.2%}\n"
        formatted += f"**Completeness Score**: {confidence.completeness_score:.2%}"
        
        return formatted
