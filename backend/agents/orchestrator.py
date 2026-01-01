"""
Agent orchestrator that manages the execution flow of all agents.
"""

from typing import Dict, Any, List
import time
from agents.retriever_agent import RetrieverAgent
from agents.analyst_agent import AnalystAgent
from agents.validator_agent import ValidatorAgent
from agents.narrator_agent import NarratorAgent
from models.schemas import EvidenceObject, AgentResponse
from utils.logger import get_logger

logger = get_logger(__name__)


class AgentOrchestrator:
    """Orchestrates the execution of all agents in the correct order."""
    
    def __init__(self):
        self.retriever = RetrieverAgent()
        self.analyst = AnalystAgent()
        self.validator = ValidatorAgent()
        self.narrator = NarratorAgent()
        logger.info("AgentOrchestrator initialized")
    
    def orchestrate(
        self,
        query: str,
        query_intent: str,
        evidence_objects: List[EvidenceObject]
    ) -> Dict[str, Any]:
        """
        Orchestrate the full agent pipeline.
        
        Returns: {
            "final_answer": str,
            "agent_responses": List[AgentResponse],
            "validated_evidence": List[EvidenceObject]
        }
        """
        start_time = time.time()
        agent_responses = []
        
        logger.info("Agent orchestration started", query=query[:50])
        
        # Step 1: Retriever Agent - Deduplicate evidence
        retriever_response = self.retriever.process({
            "evidence_objects": evidence_objects
        })
        agent_responses.append(retriever_response)
        
        deduplicated_evidence = retriever_response.output["deduplicated_evidence"]
        
        # Step 2: Analyst Agent - Analyze and generate insights
        analyst_response = self.analyst.process({
            "evidence_objects": deduplicated_evidence,
            "query_intent": query_intent
        })
        agent_responses.append(analyst_response)
        
        insights = analyst_response.output["insights"]
        comparisons = analyst_response.output["comparisons"]
        patterns = analyst_response.output["patterns"]
        
        # Step 3: Validator Agent - Validate evidence and insights
        validator_response = self.validator.process({
            "evidence_objects": deduplicated_evidence,
            "insights": insights
        })
        agent_responses.append(validator_response)
        
        validation_result = validator_response.output["validation_result"]
        validated_evidence = validation_result["validated_evidence"]
        
        # Convert validated evidence dicts back to EvidenceObject
        validated_evidence_objects = [
            EvidenceObject(**e) if isinstance(e, dict) else e
            for e in validated_evidence
        ]
        
        # Step 4: Narrator Agent - Generate final answer
        narrator_response = self.narrator.process({
            "query": query,
            "evidence_objects": validated_evidence_objects,
            "insights": insights,
            "comparisons": comparisons,
            "patterns": patterns
        })
        agent_responses.append(narrator_response)
        
        final_answer = narrator_response.output["answer"]
        
        elapsed = (time.time() - start_time) * 1000
        
        logger.info("Agent orchestration complete",
                   total_time_ms=elapsed,
                   agents_executed=len(agent_responses))
        
        return {
            "final_answer": final_answer,
            "agent_responses": agent_responses,
            "validated_evidence": validated_evidence_objects,
            "insights": insights,
            "comparisons": comparisons,
            "patterns": patterns,
            "orchestration_time_ms": elapsed
        }
