"""
Retriever Agent: Collects and deduplicates evidence objects.
"""

from typing import Dict, Any, List
import time
from agents.base_agent import BaseAgent
from models.schemas import EvidenceObject, AgentResponse
from evidence.deduplicator import EvidenceDeduplicator
from utils.logger import get_logger

logger = get_logger(__name__)


class RetrieverAgent(BaseAgent):
    """Agent responsible for collecting and deduplicating evidence."""
    
    def __init__(self):
        super().__init__(
            name="RetrieverAgent",
            role="Collect and deduplicate evidence objects from retrieval layer"
        )
        self.deduplicator = EvidenceDeduplicator()
    
    def process(self, input_data: Dict[str, Any]) -> AgentResponse:
        """
        Process retrieval results and deduplicate evidence.
        
        Input: {
            "evidence_objects": List[EvidenceObject]
        }
        
        Output: {
            "deduplicated_evidence": List[EvidenceObject],
            "original_count": int,
            "deduplicated_count": int
        }
        """
        start_time = time.time()
        
        evidence_objects = input_data.get("evidence_objects", [])
        
        logger.info(f"{self.name}: Processing evidence", count=len(evidence_objects))
        
        # Deduplicate evidence
        deduplicated = self.deduplicator.deduplicate(evidence_objects)
        
        # Sort by confidence
        deduplicated.sort(key=lambda e: e.confidence, reverse=True)
        
        output = {
            "deduplicated_evidence": deduplicated,
            "original_count": len(evidence_objects),
            "deduplicated_count": len(deduplicated),
            "removed_count": len(evidence_objects) - len(deduplicated)
        }
        
        processing_time = (time.time() - start_time) * 1000
        
        logger.info(f"{self.name}: Processing complete",
                   original=len(evidence_objects),
                   deduplicated=len(deduplicated),
                   time_ms=processing_time)
        
        return AgentResponse(**self._create_response(output, processing_time))
