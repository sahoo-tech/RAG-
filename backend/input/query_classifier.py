"""
Query classifier for RAG++ system.
Classifies user queries into analytical intent categories.
"""

from typing import Dict, List
import re
from models.schemas import AnalyticalIntent
from utils.logger import get_logger

logger = get_logger(__name__)


class QueryClassifier:
    """Classifies analytical queries into intent categories."""
    
    def __init__(self):
        # Keywords for each intent type
        self.intent_keywords = {
            AnalyticalIntent.TREND_ANALYSIS: [
                "trend", "over time", "growth", "decline", "increase", "decrease",
                "change", "evolution", "progression", "trajectory", "pattern",
                "last", "past", "historical", "time series"
            ],
            AnalyticalIntent.SEGMENTATION: [
                "segment", "group", "cohort", "category", "breakdown", "split",
                "by", "across", "distribution", "demographics", "types"
            ],
            AnalyticalIntent.COMPARISON: [
                "compare", "comparison", "versus", "vs", "difference", "between",
                "against", "relative to", "better", "worse", "higher", "lower",
                "than", "contrast"
            ],
            AnalyticalIntent.ANOMALY_EXPLANATION: [
                "why", "explain", "reason", "cause", "anomaly", "spike", "drop",
                "unusual", "unexpected", "outlier", "abnormal", "strange",
                "sudden", "what happened", "what caused"
            ],
            AnalyticalIntent.DESCRIPTIVE_SUMMARY: [
                "what", "summary", "overview", "describe", "show", "tell",
                "current", "status", "state", "snapshot", "report", "total",
                "average", "mean", "median"
            ]
        }
    
    def classify(self, query: str) -> AnalyticalIntent:
        """
        Classify a query into an analytical intent category.
        Uses keyword matching with scoring.
        """
        query_lower = query.lower()
        scores: Dict[AnalyticalIntent, int] = {intent: 0 for intent in AnalyticalIntent}
        
        # Score each intent based on keyword matches
        for intent, keywords in self.intent_keywords.items():
            for keyword in keywords:
                if keyword in query_lower:
                    scores[intent] += 1
        
        # Additional pattern-based scoring
        scores = self._apply_pattern_rules(query_lower, scores)
        
        # Get intent with highest score
        best_intent = max(scores.items(), key=lambda x: x[1])[0]
        
        # Default to descriptive summary if no clear intent
        if scores[best_intent] == 0:
            best_intent = AnalyticalIntent.DESCRIPTIVE_SUMMARY
        
        logger.info("Query classified",
                   query=query[:100],
                   intent=best_intent.value,
                   scores={k.value: v for k, v in scores.items()})
        
        return best_intent
    
    def _apply_pattern_rules(self, query: str, scores: Dict[AnalyticalIntent, int]) -> Dict[AnalyticalIntent, int]:
        """Apply additional pattern-based rules for classification."""
        
        # Time-based patterns suggest trend analysis
        time_patterns = [
            r'\blast\s+\d+\s+(day|week|month|year|quarter)',
            r'\bq[1-4]\s+\d{4}',
            r'\b\d{4}',
            r'\bmonthly\b',
            r'\bweekly\b',
            r'\bdaily\b'
        ]
        for pattern in time_patterns:
            if re.search(pattern, query):
                scores[AnalyticalIntent.TREND_ANALYSIS] += 2
        
        # Question words
        if query.startswith("why") or query.startswith("what caused"):
            scores[AnalyticalIntent.ANOMALY_EXPLANATION] += 3
        
        if query.startswith("compare") or " vs " in query or " versus " in query:
            scores[AnalyticalIntent.COMPARISON] += 3
        
        # Segmentation indicators
        if " by " in query or " across " in query:
            scores[AnalyticalIntent.SEGMENTATION] += 2
        
        return scores
    
    def get_intent_description(self, intent: AnalyticalIntent) -> str:
        """Get a human-readable description of an intent."""
        descriptions = {
            AnalyticalIntent.TREND_ANALYSIS: "Analyzing trends and changes over time",
            AnalyticalIntent.SEGMENTATION: "Breaking down data by segments or groups",
            AnalyticalIntent.COMPARISON: "Comparing metrics across different entities",
            AnalyticalIntent.ANOMALY_EXPLANATION: "Explaining unusual patterns or anomalies",
            AnalyticalIntent.DESCRIPTIVE_SUMMARY: "Providing descriptive statistics and summaries"
        }
        return descriptions.get(intent, "Unknown intent")
