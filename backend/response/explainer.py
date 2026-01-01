"""
Explainability layer for RAG++ system.
"""

from typing import List
from models.schemas import (
    ExplainabilityOutput, QueryDecomposition, EvidenceObject,
    AgentResponse, ValidationResult, ConfidenceScore
)
from utils.logger import get_logger

logger = get_logger(__name__)


class Explainer:
    """Generates explainability output for debugging and auditability."""
    
    def generate_explainability(
        self,
        query_decomposition: QueryDecomposition,
        evidence_objects: List[EvidenceObject],
        agent_responses: List[AgentResponse],
        validation_result: dict,
        confidence: ConfidenceScore,
        reasoning_steps: List[str]
    ) -> ExplainabilityOutput:
        """
        Generate comprehensive explainability output.
        """
        # Convert validation_result dict to ValidationResult if needed
        if isinstance(validation_result, dict):
            validation_result = ValidationResult(**validation_result)
        
        explainability = ExplainabilityOutput(
            query_decomposition=query_decomposition,
            evidence_objects=evidence_objects,
            agent_responses=agent_responses,
            validation_result=validation_result,
            confidence_details=confidence,
            reasoning_steps=reasoning_steps
        )
        
        logger.info("Explainability output generated",
                   evidence_count=len(evidence_objects),
                   agent_count=len(agent_responses),
                   reasoning_steps=len(reasoning_steps))
        
        return explainability
    
    def format_explainability_text(self, explainability: ExplainabilityOutput) -> str:
        """Format explainability output as human-readable text."""
        
        sections = []
        
        # Query Decomposition
        sections.append("## Query Decomposition")
        sections.append(f"Intent: {explainability.query_decomposition.intent.value}")
        sections.append(f"Sub-questions: {len(explainability.query_decomposition.sub_questions)}")
        
        # Evidence
        sections.append("\n## Evidence Collected")
        sections.append(f"Total evidence objects: {len(explainability.evidence_objects)}")
        sources = set(e.source for e in explainability.evidence_objects)
        sections.append(f"Sources: {', '.join(sources)}")
        
        # Agent Execution
        sections.append("\n## Agent Execution")
        for agent_resp in explainability.agent_responses:
            sections.append(f"- {agent_resp.agent_name}: {agent_resp.processing_time_ms:.2f}ms")
        
        # Validation
        sections.append("\n## Validation")
        sections.append(f"Valid: {explainability.validation_result.is_valid}")
        if explainability.validation_result.issues:
            sections.append(f"Issues: {len(explainability.validation_result.issues)}")
        
        # Confidence
        sections.append("\n## Confidence Assessment")
        sections.append(f"Level: {explainability.confidence_details.confidence_level.value}")
        sections.append(f"Coverage: {explainability.confidence_details.coverage_score:.2%}")
        sections.append(f"Completeness: {explainability.confidence_details.completeness_score:.2%}")
        
        # Reasoning Steps
        sections.append("\n## Reasoning Steps")
        for i, step in enumerate(explainability.reasoning_steps, 1):
            sections.append(f"{i}. {step}")
        
        return "\n".join(sections)
