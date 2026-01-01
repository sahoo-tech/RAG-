"""
Pydantic schemas for RAG++ system.
Defines all data structures used throughout the application.
"""

from pydantic import BaseModel, Field, validator
from typing import List, Optional, Dict, Any, Literal
from datetime import datetime
from enum import Enum


class AnalyticalIntent(str, Enum):
    """Types of analytical queries the system can handle."""
    TREND_ANALYSIS = "trend_analysis"
    SEGMENTATION = "segmentation"
    COMPARISON = "comparison"
    ANOMALY_EXPLANATION = "anomaly_explanation"
    DESCRIPTIVE_SUMMARY = "descriptive_summary"


class ConfidenceLevel(str, Enum):
    """Confidence levels for responses."""
    HIGH = "high_confidence"
    PARTIAL = "partial_evidence"
    INSUFFICIENT = "insufficient_data"


class EvidenceObject(BaseModel):
    """Standardized evidence object from retrieval."""
    metric: str = Field(..., description="Name of the metric")
    segment: str = Field(..., description="Segment or cohort definition")
    time_window: str = Field(..., description="Time range for this evidence")
    value: float = Field(..., description="Observed value")
    change: Optional[float] = Field(None, description="Delta or trend value")
    support: str = Field(..., description="Supporting observation or context")
    source: str = Field(..., description="Source of evidence (semantic/structured/statistical)")
    confidence: float = Field(default=1.0, ge=0.0, le=1.0, description="Confidence in this evidence")
    
    class Config:
        json_schema_extra = {
            "example": {
                "metric": "revenue",
                "segment": "enterprise_customers",
                "time_window": "Q1_2024",
                "value": 125000.0,
                "change": 15.5,
                "support": "15.5% increase compared to Q4_2023",
                "source": "structured",
                "confidence": 0.95
            }
        }


class SubQuestion(BaseModel):
    """A decomposed sub-question from the main query."""
    question: str = Field(..., description="The sub-question text")
    required_metrics: List[str] = Field(default_factory=list, description="Metrics needed")
    required_segments: List[str] = Field(default_factory=list, description="Segments needed")
    time_windows: List[str] = Field(default_factory=list, description="Time periods needed")
    contributing_factors: List[str] = Field(default_factory=list, description="Potential factors to analyze")


class QueryDecomposition(BaseModel):
    """Structured decomposition of a user query."""
    original_query: str = Field(..., description="Original user query")
    intent: AnalyticalIntent = Field(..., description="Classified analytical intent")
    sub_questions: List[SubQuestion] = Field(..., description="Decomposed sub-questions")
    priority_order: List[int] = Field(..., description="Order to process sub-questions")
    
    @validator('priority_order')
    def validate_priority_order(cls, v, values):
        """Ensure priority order matches number of sub-questions."""
        if 'sub_questions' in values and len(v) != len(values['sub_questions']):
            raise ValueError("Priority order must match number of sub-questions")
        return v


class RetrievalResult(BaseModel):
    """Results from a retrieval operation."""
    evidence_objects: List[EvidenceObject] = Field(default_factory=list)
    retrieval_time_ms: float = Field(..., description="Time taken for retrieval")
    sources_used: List[str] = Field(default_factory=list, description="Retrieval sources used")


class AgentResponse(BaseModel):
    """Response from an agent."""
    agent_name: str = Field(..., description="Name of the agent")
    output: Dict[str, Any] = Field(..., description="Agent output")
    processing_time_ms: float = Field(..., description="Processing time")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional metadata")


class ValidationResult(BaseModel):
    """Result from evidence validation."""
    is_valid: bool = Field(..., description="Whether evidence is valid")
    issues: List[str] = Field(default_factory=list, description="List of validation issues")
    validated_evidence: List[EvidenceObject] = Field(default_factory=list)


class ConfidenceScore(BaseModel):
    """Confidence scoring for a response."""
    coverage_score: float = Field(..., ge=0.0, le=1.0, description="Evidence coverage score")
    completeness_score: float = Field(..., ge=0.0, le=1.0, description="Data completeness score")
    overall_confidence: float = Field(..., ge=0.0, le=1.0, description="Overall confidence")
    confidence_level: ConfidenceLevel = Field(..., description="Classified confidence level")
    reasoning: str = Field(..., description="Explanation of confidence score")


class FinalResponse(BaseModel):
    """Final response to user query."""
    query: str = Field(..., description="Original query")
    answer: str = Field(..., description="Generated answer")
    confidence: ConfidenceScore = Field(..., description="Confidence scoring")
    evidence_count: int = Field(..., description="Number of evidence objects used")
    processing_time_ms: float = Field(..., description="Total processing time")
    timestamp: datetime = Field(default_factory=datetime.now)


class ExplainabilityOutput(BaseModel):
    """Explainability information for debugging and auditability."""
    query_decomposition: QueryDecomposition = Field(..., description="How query was decomposed")
    evidence_objects: List[EvidenceObject] = Field(..., description="All evidence collected")
    agent_responses: List[AgentResponse] = Field(..., description="Responses from each agent")
    validation_result: ValidationResult = Field(..., description="Validation results")
    confidence_details: ConfidenceScore = Field(..., description="Detailed confidence scoring")
    reasoning_steps: List[str] = Field(..., description="Step-by-step reasoning")


# API Request/Response Models

class QueryRequest(BaseModel):
    """Request model for query endpoint."""
    query: str = Field(..., min_length=5, description="User's analytical query")
    include_explainability: bool = Field(default=False, description="Include explainability output")
    max_evidence: Optional[int] = Field(default=None, description="Maximum evidence objects to return")


class QueryResponse(BaseModel):
    """Response model for query endpoint."""
    success: bool = Field(..., description="Whether query was successful")
    response: Optional[FinalResponse] = Field(None, description="Final response")
    explainability: Optional[ExplainabilityOutput] = Field(None, description="Explainability output if requested")
    error: Optional[str] = Field(None, description="Error message if failed")


class HealthResponse(BaseModel):
    """Health check response."""
    status: Literal["healthy", "unhealthy"] = Field(..., description="System health status")
    timestamp: datetime = Field(default_factory=datetime.now)
    components: Dict[str, bool] = Field(..., description="Status of individual components")
    version: str = Field(default="1.0.0", description="System version")
