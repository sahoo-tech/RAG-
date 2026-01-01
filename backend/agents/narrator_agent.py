"""
Narrator Agent: Generates final answer using only validated evidence.
"""

from typing import Dict, Any, List
import time
from agents.base_agent import BaseAgent
from models.schemas import EvidenceObject, AgentResponse
from utils.logger import get_logger

logger = get_logger(__name__)


class NarratorAgent(BaseAgent):
    """Agent responsible for generating the final narrative answer."""
    
    def __init__(self):
        super().__init__(
            name="NarratorAgent",
            role="Generate final answer using only validated evidence"
        )
    
    def process(self, input_data: Dict[str, Any]) -> AgentResponse:
        """
        Generate final narrative answer from validated evidence and insights.
        
        Input: {
            "query": str,
            "evidence_objects": List[EvidenceObject],
            "insights": List[str],
            "comparisons": List[Dict],
            "patterns": List[str]
        }
        
        Output: {
            "answer": str,
            "evidence_references": List[str]
        }
        """
        start_time = time.time()
        
        query = input_data.get("query", "")
        evidence_objects = input_data.get("evidence_objects", [])
        insights = input_data.get("insights", [])
        comparisons = input_data.get("comparisons", [])
        patterns = input_data.get("patterns", [])
        
        logger.info(f"{self.name}: Generating narrative",
                   evidence_count=len(evidence_objects),
                   insights_count=len(insights))
        
        # Generate answer
        answer = self._generate_answer(
            query, evidence_objects, insights, comparisons, patterns
        )
        
        # Create evidence references
        evidence_refs = [
            f"{e.metric} ({e.segment}): {e.value:.2f}"
            for e in evidence_objects[:5]  # Top 5 evidence
        ]
        
        output = {
            "answer": answer,
            "evidence_references": evidence_refs
        }
        
        processing_time = (time.time() - start_time) * 1000
        
        logger.info(f"{self.name}: Narrative generation complete",
                   answer_length=len(answer),
                   time_ms=processing_time)
        
        return AgentResponse(**self._create_response(output, processing_time))
    
    def _generate_answer(
        self,
        query: str,
        evidence: List[EvidenceObject],
        insights: List[str],
        comparisons: List[Dict],
        patterns: List[str]
    ) -> str:
        """Generate the final answer narrative."""
        
        if not evidence:
            return "Insufficient data available to answer this query."
        
        # Build answer sections
        sections = []
        
        # Opening statement
        sections.append(f"Based on the available data:")
        
        # Key insights
        if insights:
            sections.append("\nKey Findings:")
            for insight in insights[:3]:  # Top 3 insights
                sections.append(f"• {insight}")
        
        # Comparisons
        if comparisons:
            sections.append("\nComparisons:")
            for comp in comparisons[:2]:  # Top 2 comparisons
                metric = comp['metric']
                seg1 = comp['segment1']
                seg2 = comp['segment2']
                diff = comp.get('difference_pct', 0)
                sections.append(
                    f"• {metric.capitalize()}: {seg1} vs {seg2} shows {abs(diff):.1f}% difference"
                )
        
        # Patterns
        if patterns:
            sections.append("\nObserved Patterns:")
            for pattern in patterns:
                sections.append(f"• {pattern}")
        
        # Evidence summary
        sections.append(f"\nThis analysis is based on {len(evidence)} evidence objects from multiple sources.")
        
        return "\n".join(sections)
