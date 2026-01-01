# Quick Start Guide - RAG++ Backend

## Installation Steps

### 1. Install Python Dependencies

```bash
cd "c:\Users\ss983\OneDrive\Desktop\RAG Model"
pip install -r requirements.txt
```

This will install all required packages including:
- FastAPI and Uvicorn (API server)
- Pydantic (data validation)
- Pandas and NumPy (data processing)
- Sentence Transformers and FAISS (semantic search)
- SciPy and Statsmodels (statistical analysis)
- Structlog (logging)

### 2. Generate Sample Data

```bash
python data/generate_sample_data.py
```

This creates `data/sample_data.csv` with 1800 rows of sample analytical data.

### 3. (Optional) Install Ollama for LLM Agents

The system works without Ollama using deterministic fallbacks, but for full LLM-powered agents:

1. Download Ollama from https://ollama.ai
2. Install and start Ollama
3. Pull a model:
```bash
ollama pull llama2
```

### 4. Start the Server

```bash
python main.py
```

The server will start on `http://localhost:8000`

### 5. Test the System

**Option A: Use the test script**
```bash
python test_pipeline.py
```

**Option B: Use curl**
```bash
curl -X POST "http://localhost:8000/query" \
  -H "Content-Type: application/json" \
  -d "{\"query\": \"What is the trend in revenue over the last quarter?\"}"
```

**Option C: Visit the API docs**
Open `http://localhost:8000/docs` in your browser for interactive API documentation.

## Example Queries

Try these analytical queries:

1. **Trend Analysis**: "What is the trend in revenue over the last quarter?"
2. **Comparison**: "Compare customer retention between enterprise and consumer segments"
3. **Segmentation**: "Show me user engagement breakdown by segment"
4. **Anomaly**: "Why did revenue spike in March 2024?"
5. **Summary**: "Summarize current customer retention metrics"

## Configuration

Create a `.env` file (copy from `.env.example`) to customize:

```bash
# Ollama Configuration
OLLAMA_MODEL=llama2

# Server Configuration
API_PORT=8000

# Confidence Thresholds
HIGH_CONFIDENCE_THRESHOLD=0.8
PARTIAL_CONFIDENCE_THRESHOLD=0.5
```

## Troubleshooting

**Issue**: Module not found errors  
**Solution**: Run `pip install -r requirements.txt`

**Issue**: Ollama connection error  
**Solution**: The system will use deterministic fallbacks. Install Ollama for full LLM features.

**Issue**: Sample data not found  
**Solution**: Run `python data/generate_sample_data.py`

## Next Steps

1. Replace sample data with your real analytical data
2. Customize confidence thresholds in `.env`
3. Add your own metrics and segments
4. Extend the knowledge base in `semantic_retriever.py`
