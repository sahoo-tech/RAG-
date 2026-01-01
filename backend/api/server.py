"""
FastAPI server for RAG++ system.
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
import time

from models.schemas import QueryRequest, QueryResponse, HealthResponse, FinalResponse
from api.middleware import LoggingMiddleware, ErrorHandlingMiddleware
from input.query_classifier import QueryClassifier
from input.decomposer import QueryDecomposer
from retrieval.coordinator import RetrievalCoordinator
from agents.orchestrator import AgentOrchestrator
from scoring.confidence_classifier import ConfidenceClassifier
from response.builder import ResponseBuilder
from response.explainer import Explainer
from config import get_settings
from utils.logger import get_logger, configure_logging

# Configure logging
configure_logging()

logger = get_logger(__name__)
settings = get_settings()

# Create FastAPI app
app = FastAPI(
    title="RAG++ Analytical Reasoning Engine",
    description="Fully local analytical reasoning backend with evidence-based generation",
    version="1.0.0"
)

# Add middleware
app.add_middleware(LoggingMiddleware)
app.add_middleware(ErrorHandlingMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize components
classifier = QueryClassifier()
decomposer = QueryDecomposer()
retrieval_coordinator = RetrievalCoordinator()
agent_orchestrator = AgentOrchestrator()
confidence_classifier = ConfidenceClassifier()
response_builder = ResponseBuilder()
explainer = Explainer()

logger.info("RAG++ server initialized")


@app.get("/", tags=["Root"])
async def root():
    """Root endpoint."""
    return {
        "message": "RAG++ Analytical Reasoning Engine",
        "version": "1.0.0",
        "status": "running"
    }


@app.get("/health", response_model=HealthResponse, tags=["Health"])
async def health_check():
    """Health check endpoint."""
    components = {
        "classifier": True,
        "decomposer": True,
        "retrieval": True,
        "agents": True,
        "scoring": True
    }
    
    return HealthResponse(
        status="healthy",
        timestamp=datetime.now(),
        components=components,
        version="1.0.0"
    )


@app.post("/query", response_model=QueryResponse, tags=["Query"])
async def process_query(request: QueryRequest):
    """
    Main analytical query endpoint.
    
    Processes user queries through the full RAG++ pipeline:
    1. Query classification and decomposition
    2. Hybrid retrieval (semantic + structured + statistical)
    3. Multi-agent reasoning (Retriever → Analyst → Validator → Narrator)
    4. Confidence scoring and response generation
    """
    start_time = time.time()
    
    try:
        logger.info("Processing query", query=request.query[:100])
        
        # Step 1: Classify query intent
        intent = classifier.classify(request.query)
        
        # Step 2: Decompose query
        decomposition = decomposer.decompose(request.query, intent)
        
        # Step 3: Retrieve evidence
        retrieval_result = retrieval_coordinator.retrieve(decomposition.sub_questions)
        
        # Step 4: Agent orchestration
        orchestration_result = agent_orchestrator.orchestrate(
            query=request.query,
            query_intent=intent.value,
            evidence_objects=retrieval_result.evidence_objects
        )
        
        # Step 5: Compute confidence
        confidence = confidence_classifier.classify(
            orchestration_result["validated_evidence"],
            decomposition.sub_questions
        )
        
        # Step 6: Build final response
        total_time = (time.time() - start_time) * 1000
        
        final_response = response_builder.build_response(
            query=request.query,
            answer=orchestration_result["final_answer"],
            confidence=confidence,
            evidence_objects=orchestration_result["validated_evidence"],
            processing_time_ms=total_time
        )
        
        # Step 7: Generate explainability if requested
        explainability_output = None
        if request.include_explainability:
            reasoning_steps = [
                f"1. Classified query as {intent.value}",
                f"2. Decomposed into {len(decomposition.sub_questions)} sub-questions",
                f"3. Retrieved {len(retrieval_result.evidence_objects)} evidence objects",
                f"4. Validated {len(orchestration_result['validated_evidence'])} evidence objects",
                f"5. Generated final answer with {confidence.confidence_level.value} confidence"
            ]
            
            explainability_output = explainer.generate_explainability(
                query_decomposition=decomposition,
                evidence_objects=orchestration_result["validated_evidence"],
                agent_responses=orchestration_result["agent_responses"],
                validation_result=orchestration_result["agent_responses"][2].output["validation_result"],
                confidence=confidence,
                reasoning_steps=reasoning_steps
            )
        
        logger.info("Query processed successfully",
                   query=request.query[:50],
                   confidence=confidence.confidence_level.value,
                   time_ms=total_time)
        
        return QueryResponse(
            success=True,
            response=final_response,
            explainability=explainability_output,
            error=None
        )
    
    except Exception as e:
        logger.error("Query processing failed", error=str(e), exc_info=True)
        return QueryResponse(
            success=False,
            response=None,
            explainability=None,
            error=str(e)
        )


@app.post("/chat", tags=["Chat"])
async def chat(request: dict):
    """
    Conversational AI endpoint using Ollama with streaming support.
    
    Send messages and get AI responses with real-time token streaming.
    """
    try:
        from fastapi.responses import StreamingResponse
        from api.chat_handler import chat_with_ollama_stream, ChatRequest
        
        chat_request = ChatRequest(**request)
        
        # Return streaming response
        return StreamingResponse(
            chat_with_ollama_stream(chat_request),
            media_type="text/event-stream",
            headers={
                "Cache-Control": "no-cache",
                "Connection": "keep-alive",
                "X-Accel-Buffering": "no"  # Disable buffering for nginx
            }
        )
        
    except Exception as e:
        logger.error("Chat endpoint error", error=str(e), exc_info=True)
        return {
            "success": False,
            "message": "",
            "error": str(e)
        }


@app.post("/explain", tags=["Explainability"])
async def explain_query(request: QueryRequest):
    """
    Explainability endpoint - returns detailed reasoning steps.
    """
    # Set include_explainability to True
    request.include_explainability = True
    
    # Process query
    result = await process_query(request)
    
    if result.explainability:
        return {
            "success": True,
            "explainability_text": explainer.format_explainability_text(result.explainability),
            "explainability_data": result.explainability
        }
    else:
        return {
            "success": False,
            "error": result.error
        }


if __name__ == "__main__":
    import uvicorn
    
    logger.info("Starting RAG++ server",
               host=settings.api_host,
               port=settings.api_port)
    
    uvicorn.run(
        app,
        host=settings.api_host,
        port=settings.api_port,
        log_level=settings.log_level.lower()
    )
