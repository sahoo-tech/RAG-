"""
Structured data retrieval using Pandas for filtering and aggregation.
"""

from typing import List, Optional
import pandas as pd
import time
from models.schemas import EvidenceObject, SubQuestion
from config import get_settings
from utils.logger import get_logger
from utils.helpers import calculate_percentage_change, format_metric_value

logger = get_logger(__name__)
settings = get_settings()


class StructuredRetriever:
    """Retrieves data from structured sources using Pandas."""
    
    def __init__(self, data_path: Optional[str] = None):
        self.data_path = data_path or settings.sample_data_path
        self.df: Optional[pd.DataFrame] = None
        logger.info("StructuredRetriever initialized", data_path=self.data_path)
    
    def load_data(self):
        """Load data from CSV file."""
        try:
            self.df = pd.read_csv(self.data_path)
            logger.info("Data loaded", rows=len(self.df), columns=list(self.df.columns))
        except FileNotFoundError:
            logger.warning("Data file not found, using sample data")
            self._create_sample_data()
    
    def _create_sample_data(self):
        """Create sample analytical data."""
        data = {
            'date': pd.date_range('2024-01-01', periods=90, freq='D'),
            'metric': ['revenue'] * 30 + ['users'] * 30 + ['engagement'] * 30,
            'segment': (['enterprise'] * 15 + ['consumer'] * 15) * 3,
            'value': [
                # Revenue data
                *range(10000, 10000 + 15 * 100, 100),  # enterprise revenue
                *range(5000, 5000 + 15 * 50, 50),      # consumer revenue
                # Users data
                *range(1000, 1000 + 15 * 10, 10),      # enterprise users
                *range(5000, 5000 + 15 * 50, 50),      # consumer users
                # Engagement data
                *[0.75 + i * 0.01 for i in range(15)], # enterprise engagement
                *[0.65 + i * 0.005 for i in range(15)] # consumer engagement
            ]
        }
        self.df = pd.DataFrame(data)
        logger.info("Sample data created", rows=len(self.df))
    
    def retrieve(self, sub_question: SubQuestion) -> List[EvidenceObject]:
        """
        Retrieve evidence from structured data based on sub-question requirements.
        """
        start_time = time.time()
        
        if self.df is None:
            self.load_data()
        
        evidence_objects = []
        
        # Filter by metrics
        for metric in sub_question.required_metrics:
            for segment in sub_question.required_segments:
                evidence = self._retrieve_metric_segment(
                    metric, segment, sub_question.time_windows
                )
                if evidence:
                    evidence_objects.extend(evidence)
        
        elapsed = (time.time() - start_time) * 1000
        logger.info("Structured retrieval complete",
                   query=sub_question.question[:50],
                   retrieved=len(evidence_objects),
                   time_ms=elapsed)
        
        return evidence_objects
    
    def _retrieve_metric_segment(
        self,
        metric: str,
        segment: str,
        time_windows: List[str]
    ) -> List[EvidenceObject]:
        """Retrieve data for a specific metric and segment."""
        
        if self.df is None:
            return []
        
        # Filter data
        mask = pd.Series([True] * len(self.df))
        
        if 'metric' in self.df.columns:
            mask &= self.df['metric'].str.contains(metric, case=False, na=False)
        
        if segment != "all" and 'segment' in self.df.columns:
            mask &= self.df['segment'].str.contains(segment, case=False, na=False)
        
        filtered_df = self.df[mask]
        
        if filtered_df.empty:
            return []
        
        evidence_objects = []
        
        # Compute aggregates for each time window
        for time_window in time_windows:
            evidence = self._compute_aggregate(filtered_df, metric, segment, time_window)
            if evidence:
                evidence_objects.append(evidence)
        
        return evidence_objects
    
    def _compute_aggregate(
        self,
        df: pd.DataFrame,
        metric: str,
        segment: str,
        time_window: str
    ) -> Optional[EvidenceObject]:
        """Compute aggregate statistics for a time window."""
        
        if 'value' not in df.columns:
            return None
        
        # For simplicity, use all available data
        # In production, would filter by actual time window
        current_value = df['value'].mean()
        
        # Calculate change (compare to previous period)
        if len(df) > 1:
            mid_point = len(df) // 2
            previous_value = df.iloc[:mid_point]['value'].mean()
            current_period_value = df.iloc[mid_point:]['value'].mean()
            change = calculate_percentage_change(previous_value, current_period_value)
        else:
            change = None
        
        # Create support text
        support = f"{metric.capitalize()} for {segment} segment: "
        support += f"current value {format_metric_value(current_value)}"
        if change is not None:
            support += f", {change:+.1f}% change from previous period"
        
        return EvidenceObject(
            metric=metric,
            segment=segment,
            time_window=time_window,
            value=current_value,
            change=change,
            support=support,
            source="structured",
            confidence=0.9
        )
    
    def get_cohort_breakdown(self, metric: str) -> List[EvidenceObject]:
        """Get breakdown of a metric across all cohorts."""
        
        if self.df is None or 'segment' not in self.df.columns:
            return []
        
        evidence_objects = []
        segments = self.df['segment'].unique()
        
        for segment in segments:
            segment_df = self.df[self.df['segment'] == segment]
            if 'value' in segment_df.columns:
                value = segment_df['value'].mean()
                evidence = EvidenceObject(
                    metric=metric,
                    segment=str(segment),
                    time_window="all",
                    value=value,
                    change=None,
                    support=f"{metric} for {segment}: {format_metric_value(value)}",
                    source="structured",
                    confidence=0.9
                )
                evidence_objects.append(evidence)
        
        return evidence_objects
