# RAG++ Analytical Reasoning Engine

A fully local, multi-agent analytical reasoning system with a stunning cosmic-themed frontend.

## 🌌 Project Structure

```
RAG Model/
├── backend/              # RAG++ Backend (Python/FastAPI)
│   ├── api/             # API server and endpoints
│   ├── agents/          # Multi-agent system
│   ├── evidence/        # Evidence construction
│   ├── input/           # Query processing
│   ├── models/          # Data schemas
│   ├── retrieval/       # Hybrid retrieval
│   ├── response/        # Response generation
│   ├── scoring/         # Confidence scoring
│   ├── utils/           # Utilities
│   ├── data/            # Sample data
│   ├── main.py          # Entry point
│   └── requirements.txt # Dependencies
│
├── frontend/            # Cosmic UI (HTML/CSS/JS)
│   ├── index.html      # Main page
│   ├── styles.css      # Cosmic theme
│   ├── script.js       # Backend integration
│   └── README.md       # Frontend docs
│
├── START.bat           # Quick start script
└── README.md           # This file
```

## 🚀 Quick Start

### Option 1: Use START.bat (Easiest)
```bash
# Double-click START.bat or run:
START.bat
```

This will:
1. Start the backend server on port 8000
2. Open the frontend in your browser
3. You're ready to go!

### Option 2: Manual Start

**Terminal 1 - Backend:**
```bash
cd backend
python main.py
```

**Terminal 2 - Frontend:**
```bash
cd frontend
start index.html
# Or use: python -m http.server 3000
```

## ✨ Features

### Backend (RAG++)
- ✅ **Fully Local Execution** - No external APIs
- ✅ **Multi-Agent System** - 4 specialized agents
- ✅ **Hybrid Retrieval** - Semantic + Structured + Statistical
- ✅ **Evidence-Based** - All answers backed by validated evidence
- ✅ **Confidence Scoring** - Coverage and completeness metrics
- ✅ **Explainability** - Complete reasoning transparency
- ✅ **REST API** - FastAPI with interactive docs

### Frontend (Cosmic UI)
- 🌌 **Animated Space Background** - Twinkling stars and nebula
- 🪐 **Solar System Animation** - Rotating planets and orbits
- ✨ **Particle Effects** - Interactive cosmic particles
- 📊 **Real-time Visualization** - Confidence meters and stats
- 🎨 **Premium Design** - Gradients, glows, and smooth animations
- 🔄 **Live Backend Connection** - Health status indicator
- 📱 **Responsive** - Works on all screen sizes

## 📖 Usage

### 1. Start the System
Run `START.bat` or start backend and frontend manually

### 2. Check Connection
Look for the green "Connected" status in the top-right corner

### 3. Enter a Query
Try these examples:
- "What is the trend in revenue over the last quarter?"
- "Compare customer retention between enterprise and consumer segments"
- "Show me user engagement breakdown by segment"

### 4. View Results
- See confidence level with animated meter
- Read the evidence-backed answer
- Enable explainability for full reasoning details

## 🔧 Configuration

### Backend Settings
Edit `backend/.env`:
```env
OLLAMA_MODEL=llama2
API_PORT=8000
HIGH_CONFIDENCE_THRESHOLD=0.8
```

### Frontend Settings
Edit `frontend/script.js`:
```javascript
const API_BASE_URL = 'http://localhost:8000';
```

## 📚 Documentation

- **Backend API Docs**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health
- **Frontend Guide**: `frontend/README.md`
- **Backend Guide**: `backend/README.md`

## 🎯 System Architecture

### Query Processing Flow
1. **Input** → Query Classifier → Decomposer
2. **Retrieval** → Semantic + Structured + Statistical
3. **Agents** → Retriever → Analyst → Validator → Narrator
4. **Scoring** → Coverage + Completeness → Confidence
5. **Output** → Evidence-backed answer + Explainability

### Technology Stack

**Backend:**
- Python 3.10+
- FastAPI (API server)
- Ollama (Local LLM)
- FAISS (Vector search)
- Pandas (Data processing)
- Sentence Transformers (Embeddings)

**Frontend:**
- HTML5
- CSS3 (Animations)
- Vanilla JavaScript
- Google Fonts (Orbitron, Space Grotesk)

## 🐛 Troubleshooting

**Backend won't start:**
```bash
cd backend
pip install -r requirements.txt
python main.py
```

**Frontend shows "Disconnected":**
- Ensure backend is running on port 8000
- Check `http://localhost:8000/health`

**Warnings on startup:**
- TensorFlow/PyTorch warnings are normal and harmless
- Use `python main_clean.py` for cleaner output

## 📊 Example Queries

### Trend Analysis
"What is the trend in revenue over the last quarter?"

### Comparison
"Compare customer retention between enterprise and consumer segments"

### Segmentation
"Show me user engagement breakdown by segment"

### Anomaly
"Why did revenue spike in March 2024?"

### Summary
"Summarize current customer retention metrics"

## 🌟 Key Highlights

- **100% Local** - No data leaves your machine
- **Deterministic** - Reproducible analytical results
- **Auditable** - Complete reasoning transparency
- **Beautiful UI** - Premium cosmic design
- **Fast** - Typical query: 1-3 seconds
- **Scalable** - Add your own data sources

## 📝 License

MIT License

## 🙏 Credits

- RAG++ Backend: Custom multi-agent analytical reasoning engine
- Cosmic Frontend: Custom universe-themed UI
- Fonts: Google Fonts
- Icons: Custom SVG

---

**Enjoy exploring the cosmos of analytical reasoning! 🌌✨**

For questions or issues, check the documentation in `backend/` and `frontend/` folders.
