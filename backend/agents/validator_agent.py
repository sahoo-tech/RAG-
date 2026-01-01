"""
Validator Agent: Checks logical consistency and flags unsupported claims.
"""

from typing import Dict, Any, List
import time
from agents.base_agent import BaseAgent
from models.schemas import EvidenceObject, AgentResponse, ValidationResult
from models.validators import EvidenceValidator
from utils.logger import get_logger

logger = get_logger(__name__)


class ValidatorAgent(BaseAgent):
    """Agent responsible for validating evidence and checking consistency."""
    
    def __init__(self):
        super().__init__(
            name="ValidatorAgent",
            role="Check logical consistency and flag unsupported claims"
        )
        self.validator = EvidenceValidator()
    
    def process(self, input_data: Dict[str, Any]) -> AgentResponse:
        """
        Validate evidence objects and check for inconsistencies.
        
        Input: {
            "evidence_objects": List[EvidenceObject],
            "insights": List[str]
        }
        
        Output: {
            "validation_result": ValidationResult,
            "warnings": List[str]
        }
        """
        start_time = time.time()
        
        evidence_objects = input_data.get("evidence_objects", [])
        insights = input_data.get("insights", [])
        
        logger.info(f"{self.name}: Validating evidence", count=len(evidence_objects))
        
        # Validate individual evidence objects
        validated_evidence, issues = self.validator.validate_evidence_list(evidence_objects)
        
        # Check logical consistency
        consistency_warnings = self.validator.check_logical_consistency(validated_evidence)
        
        # Validate insights against evidence
        insight_warnings = self._validate_insights(insights, validated_evidence)
        
        all_warnings = consistency_warnings + insight_warnings
        
        validation_result = ValidationResult(
            is_valid=len(issues) == 0,
            issues=issues,
            validated_evidence=validated_evidence
        )
        
        output = {
            "validation_result": validation_result.dict(),
            "warnings": all_warnings,
            "valid_evidence_count": len(validated_evidence),
            "invalid_evidence_count": len(evidence_objects) - len(validated_evidence)
        }
        
        processing_time = (time.time() - start_time) * 1000
        
        logger.info(f"{self.name}: Validation complete",
                   valid=len(validated_evidence),
                   invalid=len(evidence_objects) - len(validated_evidence),
                   warnings=len(all_warnings),
                   time_ms=processing_time)
        
        return AgentResponse(**self._create_response(output, processing_time))
    
    def _validate_insights(self, insights: List[str], evidence: List[EvidenceObject]) -> List[str]:
        """Validate that insights are supported by evidence."""
        warnings = []
        
        # Check if insights reference metrics that exist in evidence
        evidence_metrics = set(e.metric for e in evidence)
        
        for insight in insights:
            # Simple check: does insight mention any evidence metric?
            mentions_metric = any(metric in insight.lower() for metric in evidence_metrics)
            if not mentions_metric and len(evidence) > 0:
                warnings.append(f"Insight may not be supported by evidence: '{insight[:50]}...'")
        
        return warnings
