"""
Retrieval coordinator that orchestrates parallel retrieval paths.
"""

from typing import List
import asyncio
from concurrent.futures import ThreadPoolExecutor
import time
from models.schemas import EvidenceObject, SubQuestion, RetrievalResult
from retrieval.semantic_retriever import SemanticRetriever
from retrieval.structured_retriever import StructuredRetriever
from retrieval.statistical_analyzer import StatisticalAnalyzer
from config import get_settings
from utils.logger import get_logger

logger = get_logger(__name__)
settings = get_settings()


class RetrievalCoordinator:
    """Coordinates parallel retrieval from multiple sources."""
    
    def __init__(self):
        self.semantic_retriever = SemanticRetriever()
        self.structured_retriever = StructuredRetriever()
        self.statistical_analyzer = StatisticalAnalyzer()
        
        # Initialize retrievers
        self.semantic_retriever.initialize_sample_knowledge()
        self.structured_retriever.load_data()
        
        logger.info("RetrievalCoordinator initialized")
    
    def retrieve(self, sub_questions: List[SubQuestion]) -> RetrievalResult:
        """
        Coordinate retrieval across all sources for multiple sub-questions.
        Runs retrieval paths in parallel.
        """
        start_time = time.time()
        
        all_evidence = []
        sources_used = set()
        
        # Process each sub-question
        for sub_question in sub_questions:
            evidence = self._retrieve_for_subquestion(sub_question)
            all_evidence.extend(evidence)
        
        # Perform statistical analysis on collected evidence
        statistical_evidence = self.statistical_analyzer.analyze(all_evidence)
        all_evidence.extend(statistical_evidence)
        
        # Determine sources used
        for evidence in all_evidence:
            sources_used.add(evidence.source)
        
        # Limit to max evidence objects
        if len(all_evidence) > settings.max_evidence_objects:
            # Sort by confidence and take top N
            all_evidence.sort(key=lambda e: e.confidence, reverse=True)
            all_evidence = all_evidence[:settings.max_evidence_objects]
        
        elapsed = (time.time() - start_time) * 1000
        
        logger.info("Retrieval coordination complete",
                   sub_questions=len(sub_questions),
                   total_evidence=len(all_evidence),
                   sources=list(sources_used),
                   time_ms=elapsed)
        
        return RetrievalResult(
            evidence_objects=all_evidence,
            retrieval_time_ms=elapsed,
            sources_used=list(sources_used)
        )
    
    def _retrieve_for_subquestion(self, sub_question: SubQuestion) -> List[EvidenceObject]:
        """Retrieve evidence for a single sub-question from all sources."""
        
        evidence = []
        
        # Semantic retrieval
        try:
            semantic_evidence = self.semantic_retriever.retrieve(sub_question)
            evidence.extend(semantic_evidence)
        except Exception as e:
            logger.error("Semantic retrieval failed", error=str(e))
        
        # Structured retrieval
        try:
            structured_evidence = self.structured_retriever.retrieve(sub_question)
            evidence.extend(structured_evidence)
        except Exception as e:
            logger.error("Structured retrieval failed", error=str(e))
        
        return evidence
    
    def retrieve_parallel(self, sub_questions: List[SubQuestion]) -> RetrievalResult:
        """
        Retrieve evidence using parallel execution.
        This is an optimized version using ThreadPoolExecutor.
        """
        start_time = time.time()
        
        with ThreadPoolExecutor(max_workers=3) as executor:
            futures = [
                executor.submit(self._retrieve_for_subquestion, sq)
                for sq in sub_questions
            ]
            
            all_evidence = []
            for future in futures:
                try:
                    evidence = future.result()
                    all_evidence.extend(evidence)
                except Exception as e:
                    logger.error("Parallel retrieval failed", error=str(e))
        
        # Statistical analysis
        statistical_evidence = self.statistical_analyzer.analyze(all_evidence)
        all_evidence.extend(statistical_evidence)
        
        # Limit evidence
        if len(all_evidence) > settings.max_evidence_objects:
            all_evidence.sort(key=lambda e: e.confidence, reverse=True)
            all_evidence = all_evidence[:settings.max_evidence_objects]
        
        sources_used = list(set(e.source for e in all_evidence))
        elapsed = (time.time() - start_time) * 1000
        
        logger.info("Parallel retrieval complete",
                   total_evidence=len(all_evidence),
                   time_ms=elapsed)
        
        return RetrievalResult(
            evidence_objects=all_evidence,
            retrieval_time_ms=elapsed,
            sources_used=sources_used
        )
