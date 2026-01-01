"""
Statistical analysis module for computing trends, deltas, and significance.
"""

from typing import List, Optional, Tuple
import numpy as np
from scipy import stats
import time
from models.schemas import EvidenceObject, SubQuestion
from config import get_settings
from utils.logger import get_logger
from utils.helpers import calculate_percentage_change, is_significant_change

logger = get_logger(__name__)
settings = get_settings()


class StatisticalAnalyzer:
    """Performs statistical analysis on data to detect patterns and significance."""
    
    def __init__(self):
        self.significance_threshold = settings.significance_threshold
        self.min_sample_size = settings.min_sample_size
        logger.info("StatisticalAnalyzer initialized")
    
    def analyze(self, evidence_list: List[EvidenceObject]) -> List[EvidenceObject]:
        """
        Perform statistical analysis on evidence objects.
        Returns additional evidence objects with statistical insights.
        """
        start_time = time.time()
        
        statistical_evidence = []
        
        # Group evidence by metric and segment
        grouped = self._group_evidence(evidence_list)
        
        for key, group in grouped.items():
            metric, segment = key
            
            # Compute trend analysis
            trend_evidence = self._compute_trend(group, metric, segment)
            if trend_evidence:
                statistical_evidence.append(trend_evidence)
            
            # Detect anomalies
            anomaly_evidence = self._detect_anomalies(group, metric, segment)
            statistical_evidence.extend(anomaly_evidence)
        
        elapsed = (time.time() - start_time) * 1000
        logger.info("Statistical analysis complete",
                   input_evidence=len(evidence_list),
                   output_evidence=len(statistical_evidence),
                   time_ms=elapsed)
        
        return statistical_evidence
    
    def _group_evidence(self, evidence_list: List[EvidenceObject]) -> dict:
        """Group evidence by metric and segment."""
        grouped = {}
        for evidence in evidence_list:
            key = (evidence.metric, evidence.segment)
            if key not in grouped:
                grouped[key] = []
            grouped[key].append(evidence)
        return grouped
    
    def _compute_trend(
        self,
        evidence_group: List[EvidenceObject],
        metric: str,
        segment: str
    ) -> Optional[EvidenceObject]:
        """Compute trend analysis for a group of evidence."""
        
        if len(evidence_group) < 2:
            return None
        
        # Extract values and changes
        values = [e.value for e in evidence_group]
        changes = [e.change for e in evidence_group if e.change is not None]
        
        # Compute statistics
        mean_value = np.mean(values)
        std_value = np.std(values)
        
        if changes:
            mean_change = np.mean(changes)
            trend_direction = "increasing" if mean_change > 0 else "decreasing"
            
            support = f"Trend analysis for {metric} in {segment}: "
            support += f"average value {mean_value:.2f} (±{std_value:.2f}), "
            support += f"{trend_direction} trend with average change of {mean_change:+.1f}%"
            
            return EvidenceObject(
                metric=metric,
                segment=segment,
                time_window="aggregated",
                value=mean_value,
                change=mean_change,
                support=support,
                source="statistical",
                confidence=0.85
            )
        
        return None
    
    def _detect_anomalies(
        self,
        evidence_group: List[EvidenceObject],
        metric: str,
        segment: str
    ) -> List[EvidenceObject]:
        """Detect anomalies in evidence values."""
        
        if len(evidence_group) < self.min_sample_size:
            return []
        
        values = np.array([e.value for e in evidence_group])
        
        # Compute z-scores
        mean = np.mean(values)
        std = np.std(values)
        
        if std == 0:
            return []
        
        z_scores = np.abs((values - mean) / std)
        
        # Detect outliers (z-score > 2)
        anomaly_evidence = []
        for idx, z_score in enumerate(z_scores):
            if z_score > 2.0:
                evidence = evidence_group[idx]
                support = f"Anomaly detected in {metric} for {segment}: "
                support += f"value {evidence.value:.2f} is {z_score:.1f} standard deviations from mean {mean:.2f}"
                
                anomaly = EvidenceObject(
                    metric=metric,
                    segment=segment,
                    time_window=evidence.time_window,
                    value=evidence.value,
                    change=evidence.change,
                    support=support,
                    source="statistical",
                    confidence=0.8
                )
                anomaly_evidence.append(anomaly)
        
        return anomaly_evidence
    
    def compute_correlation(
        self,
        evidence_list1: List[EvidenceObject],
        evidence_list2: List[EvidenceObject]
    ) -> Optional[Tuple[float, float]]:
        """
        Compute correlation between two sets of evidence.
        Returns (correlation_coefficient, p_value) or None.
        """
        
        if len(evidence_list1) < 3 or len(evidence_list2) < 3:
            return None
        
        values1 = [e.value for e in evidence_list1]
        values2 = [e.value for e in evidence_list2]
        
        # Ensure same length
        min_len = min(len(values1), len(values2))
        values1 = values1[:min_len]
        values2 = values2[:min_len]
        
        try:
            correlation, p_value = stats.pearsonr(values1, values2)
            return correlation, p_value
        except:
            return None
    
    def test_significance(
        self,
        group1_values: List[float],
        group2_values: List[float]
    ) -> Tuple[bool, float]:
        """
        Test if difference between two groups is statistically significant.
        Returns (is_significant, p_value).
        """
        
        if len(group1_values) < 2 or len(group2_values) < 2:
            return False, 1.0
        
        try:
            t_stat, p_value = stats.ttest_ind(group1_values, group2_values)
            is_significant = p_value < self.significance_threshold
            return is_significant, p_value
        except:
            return False, 1.0
    
    def compute_variance_analysis(self, evidence_list: List[EvidenceObject]) -> dict:
        """Compute variance analysis for evidence values."""
        
        values = [e.value for e in evidence_list]
        
        if len(values) < 2:
            return {}
        
        return {
            "mean": float(np.mean(values)),
            "median": float(np.median(values)),
            "std": float(np.std(values)),
            "variance": float(np.var(values)),
            "min": float(np.min(values)),
            "max": float(np.max(values)),
            "range": float(np.max(values) - np.min(values)),
            "coefficient_of_variation": float(np.std(values) / np.mean(values)) if np.mean(values) != 0 else 0
        }
