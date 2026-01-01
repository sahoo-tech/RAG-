"""
Simple test script for RAG++ system.
Tests the main query processing pipeline.
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from input.query_classifier import QueryClassifier
from input.decomposer import QueryDecomposer
from retrieval.coordinator import RetrievalCoordinator
from agents.orchestrator import AgentOrchestrator
from scoring.confidence_classifier import ConfidenceClassifier
from response.builder import ResponseBuilder
from utils.logger import configure_logging, get_logger

# Configure logging
configure_logging()
logger = get_logger(__name__)


def test_query_pipeline(query: str):
    """Test the full query processing pipeline."""
    
    print(f"\n{'='*60}")
    print(f"Testing Query: {query}")
    print(f"{'='*60}\n")
    
    # Initialize components
    classifier = QueryClassifier()
    decomposer = QueryDecomposer()
    retrieval_coordinator = RetrievalCoordinator()
    agent_orchestrator = AgentOrchestrator()
    confidence_classifier = ConfidenceClassifier()
    response_builder = ResponseBuilder()
    
    # Step 1: Classify
    print("Step 1: Classifying query...")
    intent = classifier.classify(query)
    print(f"  Intent: {intent.value}")
    
    # Step 2: Decompose
    print("\nStep 2: Decomposing query...")
    decomposition = decomposer.decompose(query, intent)
    print(f"  Sub-questions: {len(decomposition.sub_questions)}")
    for i, sq in enumerate(decomposition.sub_questions, 1):
        print(f"    {i}. {sq.question}")
    
    # Step 3: Retrieve
    print("\nStep 3: Retrieving evidence...")
    retrieval_result = retrieval_coordinator.retrieve(decomposition.sub_questions)
    print(f"  Evidence objects: {len(retrieval_result.evidence_objects)}")
    print(f"  Sources: {', '.join(retrieval_result.sources_used)}")
    
    # Step 4: Agent orchestration
    print("\nStep 4: Running agent orchestration...")
    orchestration_result = agent_orchestrator.orchestrate(
        query=query,
        query_intent=intent.value,
        evidence_objects=retrieval_result.evidence_objects
    )
    print(f"  Validated evidence: {len(orchestration_result['validated_evidence'])}")
    print(f"  Insights: {len(orchestration_result['insights'])}")
    
    # Step 5: Confidence scoring
    print("\nStep 5: Computing confidence...")
    confidence = confidence_classifier.classify(
        orchestration_result["validated_evidence"],
        decomposition.sub_questions
    )
    print(f"  Confidence level: {confidence.confidence_level.value}")
    print(f"  Coverage: {confidence.coverage_score:.2%}")
    print(f"  Completeness: {confidence.completeness_score:.2%}")
    
    # Step 6: Build response
    print("\nStep 6: Building final response...")
    final_response = response_builder.build_response(
        query=query,
        answer=orchestration_result["final_answer"],
        confidence=confidence,
        evidence_objects=orchestration_result["validated_evidence"],
        processing_time_ms=100.0
    )
    
    print("\n" + "="*60)
    print("FINAL ANSWER:")
    print("="*60)
    print(final_response.answer)
    print("\n" + "="*60)
    print(f"Confidence: {confidence.confidence_level.value}")
    print(f"Evidence Count: {final_response.evidence_count}")
    print("="*60)
    
    return final_response


if __name__ == "__main__":
    # Test queries
    test_queries = [
        "What is the trend in revenue over the last quarter?",
        "Compare customer retention between enterprise and consumer segments",
        "Show me user engagement breakdown by segment"
    ]
    
    for query in test_queries:
        try:
            test_query_pipeline(query)
        except Exception as e:
            print(f"\nERROR: {e}")
            import traceback
            traceback.print_exc()
        
        print("\n" + "="*60 + "\n")
