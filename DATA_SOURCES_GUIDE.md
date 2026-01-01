# RAG++ Data Sources Guide

## 📊 Where Does RAG++ Get Its Data?

The RAG++ system retrieves data from **3 main sources** for comprehensive analytical reasoning:

---

## 1. 📁 Structured Data (CSV Files)

### Current Location
```
backend/data/sample_data.csv
```

### What It Contains
Currently has **1,800 sample records** with:
- **Date**: Daily data from Jan 1 - Mar 31, 2024
- **Metric**: revenue, users, engagement, retention, conversion
- **Segment**: enterprise, consumer, premium, free
- **Value**: Numerical metric values

### Sample Data Format
```csv
date,metric,segment,value
2024-01-01,revenue,enterprise,10000.00
2024-01-01,revenue,consumer,5000.00
2024-01-01,users,enterprise,1000
2024-01-01,users,consumer,5000
2024-01-01,engagement,enterprise,0.75
2024-01-01,engagement,consumer,0.65
```

### How It's Used
- **Structured Retriever** (`backend/retrieval/structured_retriever.py`) reads this CSV
- Performs filtering, aggregation, and time-slicing
- Computes metrics like averages, trends, and comparisons
- Used for: Trend analysis, comparisons, segmentation

---

## 2. 🧠 Semantic Knowledge Base (In-Memory)

### Current Location
```
backend/retrieval/semantic_retriever.py
```

### What It Contains
Pre-loaded analytical insights stored in memory:
```python
sample_knowledge = [
    {
        "text": "Revenue increased by 15.5% in Q1 2024 compared to Q4 2023 for enterprise customers",
        "metadata": {
            "metric": "revenue",
            "segment": "enterprise",
            "time_window": "Q1_2024",
            "value": 125000.0,
            "change": 15.5
        }
    },
    # ... more insights
]
```

### How It's Used
- **Semantic Retriever** uses sentence transformers to create embeddings
- Searches for similar patterns using FAISS vector similarity
- Retrieves relevant insights based on query meaning
- Used for: Context, historical patterns, domain knowledge

---

## 3. 📈 Statistical Analysis (Computed)

### Current Location
```
backend/retrieval/statistical_analyzer.py
```

### What It Does
Computes statistics **on-the-fly** from the structured data:
- Trend detection (moving averages, growth rates)
- Anomaly detection (z-scores, outliers)
- Correlation analysis
- Variance and distribution analysis

### How It's Used
- Analyzes evidence from other sources
- Detects patterns and anomalies
- Provides statistical significance
- Used for: Anomaly explanation, trend validation

---

## 🔄 How Data Flows Through the System

```
User Query
    ↓
Query Decomposition
    ↓
┌─────────────────────────────────────────┐
│  Parallel Retrieval (3 Sources)        │
├─────────────────────────────────────────┤
│ 1. Structured Data (CSV)                │
│    → Pandas filtering & aggregation     │
│                                         │
│ 2. Semantic Knowledge (Embeddings)      │
│    → FAISS similarity search            │
│                                         │
│ 3. Statistical Analysis (Computed)      │
│    → Trend/anomaly detection            │
└─────────────────────────────────────────┘
    ↓
Evidence Objects Created
    ↓
Multi-Agent Processing
    ↓
Final Answer with Confidence
```

---

## 📝 How to Add Your Own Data

### Option 1: Replace Sample CSV (Easiest)

1. **Create your CSV file** with these columns:
   ```csv
   date,metric,segment,value
   ```

2. **Save it as**:
   ```
   backend/data/sample_data.csv
   ```

3. **Restart the backend**:
   ```bash
   cd backend
   python main.py
   ```

4. **Start querying!**

### Example Custom Data
```csv
date,metric,segment,value
2024-01-01,sales,north_region,50000
2024-01-01,sales,south_region,45000
2024-01-01,customer_satisfaction,north_region,4.5
2024-01-01,customer_satisfaction,south_region,4.2
2024-01-02,sales,north_region,52000
2024-01-02,sales,south_region,46000
```

Then query: "Compare sales between north and south regions"

---

### Option 2: Add to Semantic Knowledge Base

Edit `backend/retrieval/semantic_retriever.py`:

```python
def initialize_sample_knowledge(self):
    sample_knowledge = [
        {
            "text": "Your analytical insight here",
            "metadata": {
                "metric": "your_metric",
                "segment": "your_segment",
                "time_window": "Q1_2024",
                "value": 12345.0,
                "change": 5.5
            }
        },
        # Add more insights...
    ]
```

---

### Option 3: Connect to Database (Advanced)

Modify `backend/retrieval/structured_retriever.py`:

```python
def load_data(self):
    # Instead of CSV, connect to your database
    import sqlalchemy
    engine = sqlalchemy.create_engine('your_database_url')
    self.df = pd.read_sql_query("SELECT * FROM analytics", engine)
```

Supported databases:
- PostgreSQL
- MySQL
- SQLite
- MongoDB (with pandas)
- Snowflake
- BigQuery

---

### Option 4: Connect to APIs (Advanced)

Create a custom retriever:

```python
# backend/retrieval/api_retriever.py
import requests
import pandas as pd

class APIRetriever:
    def fetch_data(self):
        response = requests.get('https://your-api.com/analytics')
        data = response.json()
        return pd.DataFrame(data)
```

---

## 🎯 Data Requirements

### Minimum Requirements
- **Date column**: For time-based analysis
- **Metric column**: What you're measuring
- **Value column**: Numerical values
- **Segment column** (optional): For comparisons

### Recommended Format
```csv
date,metric,segment,value
YYYY-MM-DD,metric_name,segment_name,numeric_value
```

### Data Quality Tips
✅ **Good:**
- Consistent date formats
- Clean metric names (no spaces)
- Numerical values only in value column
- Regular time intervals

❌ **Avoid:**
- Missing dates
- Mixed data types in value column
- Inconsistent segment names
- Too many null values

---

## 📊 Current Data Location Summary

| Source | Location | Type | Used For |
|--------|----------|------|----------|
| **Structured Data** | `backend/data/sample_data.csv` | CSV File | Aggregations, trends, comparisons |
| **Semantic Knowledge** | `backend/retrieval/semantic_retriever.py` | In-Memory | Pattern matching, insights |
| **Statistical** | Computed on-the-fly | Calculated | Anomalies, significance |

---

## 🔍 Verify Your Data

After adding your data, test it:

```bash
# 1. Check if CSV loads
cd backend
python -c "import pandas as pd; print(pd.read_csv('data/sample_data.csv').head())"

# 2. Restart backend
python main.py

# 3. Test query
curl -X POST "http://localhost:8000/query" \
  -H "Content-Type: application/json" \
  -d '{"query": "What is the trend in [your_metric]?"}'
```

---

## 📈 Scaling Your Data

### Small Dataset (< 10K rows)
✅ Use CSV files (current setup)
- Fast loading
- Easy to manage
- Perfect for demos

### Medium Dataset (10K - 1M rows)
✅ Use SQLite or PostgreSQL
- Better performance
- Query optimization
- Still local

### Large Dataset (> 1M rows)
✅ Use data warehouse
- Snowflake, BigQuery, Redshift
- Distributed processing
- Production-ready

---

## 🎨 Example: E-commerce Data

```csv
date,metric,segment,value
2024-01-01,orders,mobile,150
2024-01-01,orders,desktop,200
2024-01-01,revenue,mobile,7500
2024-01-01,revenue,desktop,12000
2024-01-01,cart_abandonment,mobile,0.35
2024-01-01,cart_abandonment,desktop,0.28
```

**Queries you can run:**
- "What is the trend in orders over the last month?"
- "Compare revenue between mobile and desktop"
- "Show me cart abandonment breakdown by segment"
- "Why did orders spike on January 15th?"

---

## 🚀 Quick Start with Your Data

1. **Prepare your CSV** (date, metric, segment, value)
2. **Save to** `backend/data/sample_data.csv`
3. **Restart backend** (`python main.py`)
4. **Open frontend** and start querying!

---

## 💡 Pro Tips

1. **Start Small**: Test with 100 rows first
2. **Clean Data**: Remove nulls and duplicates
3. **Consistent Names**: Use same metric/segment names
4. **Date Format**: Use YYYY-MM-DD
5. **Test Queries**: Try simple queries first

---

## ❓ Common Questions

**Q: Can I use multiple CSV files?**
A: Yes! Modify `structured_retriever.py` to load and concatenate multiple files.

**Q: Can I update data without restarting?**
A: Currently no, but you can add a reload endpoint to refresh data.

**Q: What if my data is in Excel?**
A: Convert to CSV or use `pd.read_excel()` in the retriever.

**Q: Can I use real-time data?**
A: Yes! Connect to your API or database that updates in real-time.

**Q: How much data can it handle?**
A: CSV: ~100K rows comfortably. For more, use a database.

---

## 📚 Next Steps

1. ✅ Review current sample data: `backend/data/sample_data.csv`
2. ✅ Prepare your own data in the same format
3. ✅ Replace the sample file
4. ✅ Restart and test!

**Your data + RAG++ = Powerful analytical insights! 🚀**
