"""
Data validation utilities for RAG++ system.
Ensures evidence objects and analytical data meet quality standards.
"""

from typing import List, Optional, Tuple
from models.schemas import EvidenceObject, ConfidenceLevel
from utils.logger import get_logger

logger = get_logger(__name__)


class EvidenceValidator:
    """Validates evidence objects for quality and consistency."""
    
    def __init__(self, min_confidence: float = 0.3):
        self.min_confidence = min_confidence
    
    def validate_evidence(self, evidence: EvidenceObject) -> Tuple[bool, List[str]]:
        """
        Validate a single evidence object.
        Returns (is_valid, list_of_issues).
        """
        issues = []
        
        # Check required fields are not empty
        if not evidence.metric or evidence.metric.strip() == "":
            issues.append("Metric name is empty")
        
        if not evidence.segment or evidence.segment.strip() == "":
            issues.append("Segment is empty")
        
        if not evidence.time_window or evidence.time_window.strip() == "":
            issues.append("Time window is empty")
        
        # Check value is reasonable
        if evidence.value is None:
            issues.append("Value is None")
        
        # Check confidence threshold
        if evidence.confidence < self.min_confidence:
            issues.append(f"Confidence {evidence.confidence} below minimum {self.min_confidence}")
        
        # Check support is meaningful
        if not evidence.support or len(evidence.support) < 10:
            issues.append("Support text is too short or empty")
        
        is_valid = len(issues) == 0
        
        if not is_valid:
            logger.warning("Evidence validation failed", 
                          metric=evidence.metric, 
                          issues=issues)
        
        return is_valid, issues
    
    def validate_evidence_list(self, evidence_list: List[EvidenceObject]) -> Tuple[List[EvidenceObject], List[str]]:
        """
        Validate a list of evidence objects.
        Returns (valid_evidence, all_issues).
        """
        valid_evidence = []
        all_issues = []
        
        for idx, evidence in enumerate(evidence_list):
            is_valid, issues = self.validate_evidence(evidence)
            if is_valid:
                valid_evidence.append(evidence)
            else:
                all_issues.extend([f"Evidence {idx}: {issue}" for issue in issues])
        
        logger.info("Evidence validation complete",
                   total=len(evidence_list),
                   valid=len(valid_evidence),
                   invalid=len(evidence_list) - len(valid_evidence))
        
        return valid_evidence, all_issues
    
    def check_logical_consistency(self, evidence_list: List[EvidenceObject]) -> List[str]:
        """
        Check for logical inconsistencies across evidence objects.
        Returns list of inconsistency warnings.
        """
        warnings = []
        
        # Group evidence by metric and segment
        metric_segment_map = {}
        for evidence in evidence_list:
            key = (evidence.metric, evidence.segment)
            if key not in metric_segment_map:
                metric_segment_map[key] = []
            metric_segment_map[key].append(evidence)
        
        # Check for conflicting values in same metric/segment
        for key, evidence_group in metric_segment_map.items():
            if len(evidence_group) > 1:
                values = [e.value for e in evidence_group]
                if len(set(values)) > 1:
                    warnings.append(
                        f"Conflicting values for {key[0]} in {key[1]}: {values}"
                    )
        
        return warnings


class DataQualityChecker:
    """Checks data quality for analytical operations."""
    
    @staticmethod
    def check_sample_size(sample_size: int, min_size: int = 30) -> Tuple[bool, Optional[str]]:
        """Check if sample size is sufficient for statistical analysis."""
        if sample_size < min_size:
            return False, f"Sample size {sample_size} below minimum {min_size}"
        return True, None
    
    @staticmethod
    def check_missing_data_ratio(total: int, missing: int, max_ratio: float = 0.3) -> Tuple[bool, Optional[str]]:
        """Check if missing data ratio is acceptable."""
        if total == 0:
            return False, "No data available"
        
        ratio = missing / total
        if ratio > max_ratio:
            return False, f"Missing data ratio {ratio:.2%} exceeds maximum {max_ratio:.2%}"
        return True, None
    
    @staticmethod
    def check_time_coverage(start_date, end_date, required_days: int = 7) -> Tuple[bool, Optional[str]]:
        """Check if time coverage is sufficient."""
        if start_date is None or end_date is None:
            return False, "Missing date information"
        
        delta = (end_date - start_date).days
        if delta < required_days:
            return False, f"Time coverage {delta} days below required {required_days} days"
        return True, None


def validate_analytical_constraints(
    metric: str,
    value: float,
    allowed_metrics: Optional[List[str]] = None
) -> Tuple[bool, Optional[str]]:
    """
    Validate analytical constraints.
    Ensures metrics and values are within expected ranges.
    """
    # Check if metric is in allowed list
    if allowed_metrics and metric not in allowed_metrics:
        return False, f"Metric '{metric}' not in allowed metrics"
    
    # Check for invalid numeric values
    if value is None or (isinstance(value, float) and (value != value)):  # NaN check
        return False, "Invalid numeric value (None or NaN)"
    
    return True, None
