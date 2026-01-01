"""
Evidence coverage scorer for RAG++ system.
"""

from typing import List
from models.schemas import EvidenceObject, SubQuestion
from utils.logger import get_logger

logger = get_logger(__name__)


class CoverageScorer:
    """Computes evidence coverage score based on query requirements."""
    
    def compute_coverage(
        self,
        evidence_objects: List[EvidenceObject],
        sub_questions: List[SubQuestion]
    ) -> float:
        """
        Compute coverage score (0.0 to 1.0) based on how well evidence
        covers the requirements from sub-questions.
        """
        if not sub_questions:
            return 1.0
        
        total_requirements = 0
        covered_requirements = 0
        
        for sub_question in sub_questions:
            # Count required metrics
            for metric in sub_question.required_metrics:
                total_requirements += 1
                if self._metric_covered(metric, evidence_objects):
                    covered_requirements += 1
            
            # Count required segments
            for segment in sub_question.required_segments:
                if segment != "all":
                    total_requirements += 1
                    if self._segment_covered(segment, evidence_objects):
                        covered_requirements += 1
            
            # Count time windows
            for time_window in sub_question.time_windows:
                total_requirements += 1
                if self._time_window_covered(time_window, evidence_objects):
                    covered_requirements += 1
        
        if total_requirements == 0:
            return 1.0
        
        coverage = covered_requirements / total_requirements
        
        logger.info("Coverage score computed",
                   covered=covered_requirements,
                   total=total_requirements,
                   score=coverage)
        
        return coverage
    
    def _metric_covered(self, metric: str, evidence: List[EvidenceObject]) -> bool:
        """Check if a metric is covered by evidence."""
        return any(metric.lower() in e.metric.lower() for e in evidence)
    
    def _segment_covered(self, segment: str, evidence: List[EvidenceObject]) -> bool:
        """Check if a segment is covered by evidence."""
        return any(segment.lower() in e.segment.lower() for e in evidence)
    
    def _time_window_covered(self, time_window: str, evidence: List[EvidenceObject]) -> bool:
        """Check if a time window is covered by evidence."""
        return any(time_window.lower() in e.time_window.lower() for e in evidence)
