"""
Analyst Agent: Performs comparisons and identifies patterns.
"""

from typing import Dict, Any, List
import time
from agents.base_agent import BaseAgent
from models.schemas import EvidenceObject, AgentResponse
from utils.logger import get_logger
from utils.helpers import calculate_percentage_change

logger = get_logger(__name__)


class AnalystAgent(BaseAgent):
    """Agent responsible for analyzing evidence and identifying patterns."""
    
    def __init__(self):
        super().__init__(
            name="AnalystAgent",
            role="Perform comparisons and identify analytical patterns"
        )
    
    def process(self, input_data: Dict[str, Any]) -> AgentResponse:
        """
        Analyze evidence and generate insights.
        
        Input: {
            "evidence_objects": List[EvidenceObject],
            "query_intent": str
        }
        
        Output: {
            "insights": List[str],
            "comparisons": List[Dict],
            "patterns": List[str]
        }
        """
        start_time = time.time()
        
        evidence_objects = input_data.get("evidence_objects", [])
        query_intent = input_data.get("query_intent", "descriptive_summary")
        
        logger.info(f"{self.name}: Analyzing evidence",
                   count=len(evidence_objects),
                   intent=query_intent)
        
        # Generate insights
        insights = self._generate_insights(evidence_objects)
        
        # Perform comparisons
        comparisons = self._perform_comparisons(evidence_objects)
        
        # Identify patterns
        patterns = self._identify_patterns(evidence_objects)
        
        output = {
            "insights": insights,
            "comparisons": comparisons,
            "patterns": patterns
        }
        
        processing_time = (time.time() - start_time) * 1000
        
        logger.info(f"{self.name}: Analysis complete",
                   insights=len(insights),
                   comparisons=len(comparisons),
                   patterns=len(patterns),
                   time_ms=processing_time)
        
        return AgentResponse(**self._create_response(output, processing_time))
    
    def _generate_insights(self, evidence_objects: List[EvidenceObject]) -> List[str]:
        """Generate analytical insights from evidence."""
        insights = []
        
        # Group by metric
        metrics = {}
        for evidence in evidence_objects:
            if evidence.metric not in metrics:
                metrics[evidence.metric] = []
            metrics[evidence.metric].append(evidence)
        
        # Generate insights for each metric
        for metric, evidence_list in metrics.items():
            if evidence_list:
                # Average value insight
                avg_value = sum(e.value for e in evidence_list) / len(evidence_list)
                insights.append(f"Average {metric}: {avg_value:.2f}")
                
                # Change insights
                changes = [e.change for e in evidence_list if e.change is not None]
                if changes:
                    avg_change = sum(changes) / len(changes)
                    direction = "increasing" if avg_change > 0 else "decreasing"
                    insights.append(f"{metric.capitalize()} is {direction} with average change of {avg_change:+.1f}%")
        
        return insights
    
    def _perform_comparisons(self, evidence_objects: List[EvidenceObject]) -> List[Dict]:
        """Perform comparisons between segments."""
        comparisons = []
        
        # Group by metric and segment
        metric_segments = {}
        for evidence in evidence_objects:
            key = evidence.metric
            if key not in metric_segments:
                metric_segments[key] = {}
            if evidence.segment not in metric_segments[key]:
                metric_segments[key][evidence.segment] = []
            metric_segments[key][evidence.segment].append(evidence)
        
        # Compare segments within each metric
        for metric, segments in metric_segments.items():
            segment_names = list(segments.keys())
            if len(segment_names) >= 2:
                for i in range(len(segment_names)):
                    for j in range(i + 1, len(segment_names)):
                        seg1 = segment_names[i]
                        seg2 = segment_names[j]
                        
                        val1 = sum(e.value for e in segments[seg1]) / len(segments[seg1])
                        val2 = sum(e.value for e in segments[seg2]) / len(segments[seg2])
                        
                        diff = calculate_percentage_change(val1, val2)
                        
                        comparisons.append({
                            "metric": metric,
                            "segment1": seg1,
                            "segment2": seg2,
                            "value1": val1,
                            "value2": val2,
                            "difference_pct": diff
                        })
        
        return comparisons
    
    def _identify_patterns(self, evidence_objects: List[EvidenceObject]) -> List[str]:
        """Identify patterns in the evidence."""
        patterns = []
        
        # Check for consistent trends
        changes = [e.change for e in evidence_objects if e.change is not None]
        if changes:
            positive_changes = sum(1 for c in changes if c > 0)
            negative_changes = sum(1 for c in changes if c < 0)
            
            if positive_changes > len(changes) * 0.7:
                patterns.append("Strong upward trend across most metrics")
            elif negative_changes > len(changes) * 0.7:
                patterns.append("Strong downward trend across most metrics")
            else:
                patterns.append("Mixed trends across metrics")
        
        # Check for high confidence evidence
        high_conf = sum(1 for e in evidence_objects if e.confidence > 0.8)
        if high_conf > len(evidence_objects) * 0.7:
            patterns.append("High confidence in most evidence")
        
        return patterns
