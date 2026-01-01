# RAG++ Local Multi-Agent Analytical Reasoning Engine

A fully local analytical reasoning backend that extends standard RAG into a deterministic, auditable insight engine for analytics-focused question answering.

## Features

- **Fully Local Execution**: No external APIs or cloud services
- **Deterministic Reasoning**: Explicit validation and confidence scoring
- **Evidence-First Generation**: All answers backed by validated evidence
- **Multi-Agent System**: Specialized agents for retrieval, analysis, validation, and narration
- **Hybrid Retrieval**: Semantic, structured, and statistical analysis
- **Explainability**: Complete transparency into reasoning steps

## Architecture

The system consists of several key components:

1. **Input Processing**: Query classification and decomposition
2. **Hybrid Retrieval**: Semantic (FAISS), structured (Pandas), and statistical analysis
3. **Evidence Construction**: Standardized evidence objects with deduplication
4. **Multi-Agent System**: Retriever → Analyst → Validator → Narrator
5. **Confidence Scoring**: Coverage and completeness-based confidence classification
6. **Response Generation**: Evidence-backed answers with explainability

## Installation

### Prerequisites

- Python 3.10 or higher
- Ollama (optional, for LLM-based agents)

### Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Copy environment template:
```bash
copy .env.example .env
```

3. (Optional) Install and start Ollama:
```bash
# Download from https://ollama.ai
ollama pull llama2
```

## Usage

### Starting the Server

```bash
python main.py
```

The server will start on `http://localhost:8000`

### API Endpoints

#### POST /query
Process an analytical query:

```bash
curl -X POST "http://localhost:8000/query" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "What is the trend in revenue over the last quarter?",
    "include_explainability": false
  }'
```

#### POST /explain
Get detailed explainability for a query:

```bash
curl -X POST "http://localhost:8000/explain" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "Compare customer retention between enterprise and consumer segments"
  }'
```

#### GET /health
Check system health:

```bash
curl "http://localhost:8000/health"
```

### Example Queries

- **Trend Analysis**: "What is the trend in sales over the last quarter?"
- **Segmentation**: "Show me user engagement breakdown by segment"
- **Comparison**: "Compare revenue between enterprise and consumer customers"
- **Anomaly Explanation**: "Why did revenue spike in March 2024?"
- **Descriptive Summary**: "Summarize current customer retention metrics"

## Configuration

Edit `.env` to configure:

- `OLLAMA_MODEL`: LLM model to use (default: llama2)
- `API_PORT`: Server port (default: 8000)
- `HIGH_CONFIDENCE_THRESHOLD`: Threshold for high confidence (default: 0.8)
- `EMBEDDING_MODEL`: Sentence transformer model (default: all-MiniLM-L6-v2)

## System Components

### Input Processing
- `input/query_classifier.py`: Classifies queries into analytical intents
- `input/decomposer.py`: Decomposes queries into sub-questions

### Retrieval Layer
- `retrieval/semantic_retriever.py`: Semantic similarity search
- `retrieval/structured_retriever.py`: Pandas-based data retrieval
- `retrieval/statistical_analyzer.py`: Statistical analysis and trend detection
- `retrieval/coordinator.py`: Parallel retrieval coordination

### Evidence System
- `evidence/builder.py`: Evidence object construction
- `evidence/deduplicator.py`: Semantic deduplication

### Multi-Agent System
- `agents/retriever_agent.py`: Evidence collection and deduplication
- `agents/analyst_agent.py`: Pattern identification and comparisons
- `agents/validator_agent.py`: Logical consistency checking
- `agents/narrator_agent.py`: Final answer generation
- `agents/orchestrator.py`: Agent execution orchestration

### Scoring & Response
- `scoring/coverage_scorer.py`: Evidence coverage scoring
- `scoring/completeness_scorer.py`: Data completeness scoring
- `scoring/confidence_classifier.py`: Confidence level classification
- `response/builder.py`: Final response construction
- `response/explainer.py`: Explainability output generation

## Development

### Project Structure
```
RAG Model/
├── api/                 # FastAPI server and middleware
├── agents/              # Multi-agent system
├── evidence/            # Evidence construction
├── input/               # Query processing
├── models/              # Pydantic schemas
├── retrieval/           # Hybrid retrieval system
├── response/            # Response generation
├── scoring/             # Confidence scoring
├── utils/               # Utilities and logging
├── config.py            # Configuration management
├── main.py              # Entry point
└── requirements.txt     # Dependencies
```

### Running Tests

```bash
pytest
```

## Constraints

- **No External APIs**: All processing is local
- **No Speculative Reasoning**: Only evidence-backed claims
- **Deterministic Analytics**: Reproducible results
- **Auditable**: Complete reasoning transparency

## License

MIT License

## Contributing

Contributions welcome! Please ensure:
- All code is fully local (no external API calls)
- Evidence-based reasoning is maintained
- Explainability is preserved
