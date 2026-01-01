"""
Confidence classifier for RAG++ system.
"""

from models.schemas import ConfidenceScore, ConfidenceLevel, SubQuestion, EvidenceObject
from typing import List
from scoring.coverage_scorer import CoverageScorer
from scoring.completeness_scorer import CompletenessScorer
from config import get_settings
from utils.logger import get_logger

logger = get_logger(__name__)
settings = get_settings()


class ConfidenceClassifier:
    """Classifies response confidence based on coverage and completeness."""
    
    def __init__(self):
        self.coverage_scorer = CoverageScorer()
        self.completeness_scorer = CompletenessScorer()
    
    def classify(
        self,
        evidence_objects: List[EvidenceObject],
        sub_questions: List[SubQuestion]
    ) -> ConfidenceScore:
        """
        Classify confidence level based on evidence coverage and completeness.
        """
        # Compute scores
        coverage_score = self.coverage_scorer.compute_coverage(
            evidence_objects, sub_questions
        )
        
        completeness_score = self.completeness_scorer.compute_completeness(
            evidence_objects
        )
        
        # Overall confidence (weighted average)
        overall_confidence = (coverage_score * 0.6) + (completeness_score * 0.4)
        
        # Classify confidence level
        if overall_confidence >= settings.high_confidence_threshold:
            confidence_level = ConfidenceLevel.HIGH
            reasoning = "Strong evidence coverage and high data completeness"
        elif overall_confidence >= settings.partial_confidence_threshold:
            confidence_level = ConfidenceLevel.PARTIAL
            reasoning = "Partial evidence coverage or moderate data completeness"
        else:
            confidence_level = ConfidenceLevel.INSUFFICIENT
            reasoning = "Insufficient evidence coverage or low data completeness"
        
        logger.info("Confidence classified",
                   coverage=coverage_score,
                   completeness=completeness_score,
                   overall=overall_confidence,
                   level=confidence_level.value)
        
        return ConfidenceScore(
            coverage_score=coverage_score,
            completeness_score=completeness_score,
            overall_confidence=overall_confidence,
            confidence_level=confidence_level,
            reasoning=reasoning
        )
