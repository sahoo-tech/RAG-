"""
Query decomposer for RAG++ system.
Decomposes analytical queries into structured sub-questions.
"""

from typing import List, Dict, Any
import re
from models.schemas import QueryDecomposition, SubQuestion, AnalyticalIntent
from utils.logger import get_logger
from utils.helpers import parse_time_window

logger = get_logger(__name__)


class QueryDecomposer:
    """Decomposes analytical queries into structured sub-questions."""
    
    def __init__(self):
        self.metric_patterns = [
            r'\b(revenue|sales|profit|cost|price|margin)\b',
            r'\b(users?|customers?|accounts?|subscribers?)\b',
            r'\b(engagement|retention|churn|conversion)\b',
            r'\b(traffic|visits?|sessions?|pageviews?)\b',
            r'\b(orders?|transactions?|purchases?)\b',
            r'\b(growth|rate|percentage|ratio)\b'
        ]
        
        self.segment_patterns = [
            r'\b(segment|cohort|group|category)\s+([A-Z]|\w+)',
            r'\b(enterprise|small business|consumer|individual)\b',
            r'\b(mobile|desktop|web|app)\b',
            r'\b(new|existing|returning|churned)\b',
            r'\b(premium|free|trial|paid)\b'
        ]
    
    def decompose(self, query: str, intent: AnalyticalIntent) -> QueryDecomposition:
        """
        Decompose a query into structured sub-questions based on intent.
        """
        # Extract components
        metrics = self._extract_metrics(query)
        segments = self._extract_segments(query)
        time_windows = self._extract_time_windows(query)
        
        # Generate sub-questions based on intent
        sub_questions = self._generate_sub_questions(
            query, intent, metrics, segments, time_windows
        )
        
        # Determine priority order
        priority_order = list(range(len(sub_questions)))
        
        decomposition = QueryDecomposition(
            original_query=query,
            intent=intent,
            sub_questions=sub_questions,
            priority_order=priority_order
        )
        
        logger.info("Query decomposed",
                   query=query[:100],
                   intent=intent.value,
                   num_sub_questions=len(sub_questions),
                   metrics=metrics,
                   segments=segments)
        
        return decomposition
    
    def _extract_metrics(self, query: str) -> List[str]:
        """Extract metric names from query."""
        metrics = set()
        query_lower = query.lower()
        
        for pattern in self.metric_patterns:
            matches = re.findall(pattern, query_lower)
            metrics.update(matches)
        
        # If no metrics found, use generic "value"
        if not metrics:
            metrics.add("value")
        
        return list(metrics)
    
    def _extract_segments(self, query: str) -> List[str]:
        """Extract segment names from query."""
        segments = set()
        query_lower = query.lower()
        
        for pattern in self.segment_patterns:
            matches = re.findall(pattern, query_lower)
            if isinstance(matches, list) and matches:
                if isinstance(matches[0], tuple):
                    segments.update([m[0] if m[0] else m[1] for m in matches])
                else:
                    segments.update(matches)
        
        # If no segments found, use "all"
        if not segments:
            segments.add("all")
        
        return list(segments)
    
    def _extract_time_windows(self, query: str) -> List[str]:
        """Extract time window references from query."""
        time_windows = []
        query_lower = query.lower()
        
        # Pattern: "last X days/weeks/months"
        last_pattern = r'last\s+(\d+)\s+(day|week|month|quarter|year)s?'
        matches = re.findall(last_pattern, query_lower)
        for match in matches:
            time_windows.append(f"last_{match[0]}_{match[1]}s")
        
        # Pattern: "Q1 2024", "2024"
        quarter_pattern = r'q([1-4])\s+(\d{4})'
        matches = re.findall(quarter_pattern, query_lower)
        for match in matches:
            time_windows.append(f"Q{match[0]}_{match[1]}")
        
        year_pattern = r'\b(20\d{2})\b'
        matches = re.findall(year_pattern, query_lower)
        time_windows.extend(matches)
        
        # Default if no time window found
        if not time_windows:
            time_windows.append("last_7_days")
        
        return time_windows
    
    def _generate_sub_questions(
        self,
        query: str,
        intent: AnalyticalIntent,
        metrics: List[str],
        segments: List[str],
        time_windows: List[str]
    ) -> List[SubQuestion]:
        """Generate sub-questions based on intent and extracted components."""
        
        sub_questions = []
        
        if intent == AnalyticalIntent.TREND_ANALYSIS:
            sub_questions = self._generate_trend_questions(metrics, segments, time_windows)
        
        elif intent == AnalyticalIntent.SEGMENTATION:
            sub_questions = self._generate_segmentation_questions(metrics, segments, time_windows)
        
        elif intent == AnalyticalIntent.COMPARISON:
            sub_questions = self._generate_comparison_questions(metrics, segments, time_windows)
        
        elif intent == AnalyticalIntent.ANOMALY_EXPLANATION:
            sub_questions = self._generate_anomaly_questions(metrics, segments, time_windows)
        
        elif intent == AnalyticalIntent.DESCRIPTIVE_SUMMARY:
            sub_questions = self._generate_summary_questions(metrics, segments, time_windows)
        
        return sub_questions
    
    def _generate_trend_questions(self, metrics: List[str], segments: List[str], time_windows: List[str]) -> List[SubQuestion]:
        """Generate sub-questions for trend analysis."""
        questions = []
        
        for metric in metrics:
            questions.append(SubQuestion(
                question=f"What is the current value of {metric}?",
                required_metrics=[metric],
                required_segments=segments,
                time_windows=[time_windows[0]],
                contributing_factors=[]
            ))
            
            questions.append(SubQuestion(
                question=f"How has {metric} changed over {time_windows[0]}?",
                required_metrics=[metric],
                required_segments=segments,
                time_windows=time_windows,
                contributing_factors=["time", "seasonality"]
            ))
        
        return questions
    
    def _generate_segmentation_questions(self, metrics: List[str], segments: List[str], time_windows: List[str]) -> List[SubQuestion]:
        """Generate sub-questions for segmentation analysis."""
        questions = []
        
        for metric in metrics:
            questions.append(SubQuestion(
                question=f"What is the distribution of {metric} across segments?",
                required_metrics=[metric],
                required_segments=segments,
                time_windows=[time_windows[0]],
                contributing_factors=["segment_characteristics"]
            ))
        
        return questions
    
    def _generate_comparison_questions(self, metrics: List[str], segments: List[str], time_windows: List[str]) -> List[SubQuestion]:
        """Generate sub-questions for comparison analysis."""
        questions = []
        
        for metric in metrics:
            questions.append(SubQuestion(
                question=f"What are the values of {metric} for each segment?",
                required_metrics=[metric],
                required_segments=segments,
                time_windows=[time_windows[0]],
                contributing_factors=[]
            ))
            
            if len(segments) >= 2:
                questions.append(SubQuestion(
                    question=f"What is the difference in {metric} between segments?",
                    required_metrics=[metric],
                    required_segments=segments,
                    time_windows=[time_windows[0]],
                    contributing_factors=["segment_differences"]
                ))
        
        return questions
    
    def _generate_anomaly_questions(self, metrics: List[str], segments: List[str], time_windows: List[str]) -> List[SubQuestion]:
        """Generate sub-questions for anomaly explanation."""
        questions = []
        
        for metric in metrics:
            questions.append(SubQuestion(
                question=f"What is the baseline value of {metric}?",
                required_metrics=[metric],
                required_segments=segments,
                time_windows=time_windows,
                contributing_factors=[]
            ))
            
            questions.append(SubQuestion(
                question=f"What factors might have influenced {metric}?",
                required_metrics=[metric],
                required_segments=segments,
                time_windows=time_windows,
                contributing_factors=["external_events", "seasonality", "segment_changes"]
            ))
        
        return questions
    
    def _generate_summary_questions(self, metrics: List[str], segments: List[str], time_windows: List[str]) -> List[SubQuestion]:
        """Generate sub-questions for descriptive summary."""
        questions = []
        
        for metric in metrics:
            questions.append(SubQuestion(
                question=f"What are the key statistics for {metric}?",
                required_metrics=[metric],
                required_segments=segments,
                time_windows=[time_windows[0]],
                contributing_factors=[]
            ))
        
        return questions
