# RAG++ Analytical Query Capabilities

## Overview

Your RAG++ system is designed to answer **5 main types of analytical questions** using evidence-based reasoning. It analyzes data from multiple sources and provides confidence-scored answers.

---

## 1. 📈 Trend Analysis

**What it does**: Analyzes how metrics change over time, identifies growth/decline patterns, and detects trends.

### Example Questions:
- "What is the trend in revenue over the last quarter?"
- "How has user engagement changed over the past month?"
- "Show me the sales growth pattern for the last 6 months"
- "Is customer retention increasing or decreasing?"
- "What's the trajectory of conversion rates this year?"

### What You Get:
- Current metric values
- Percentage changes over time
- Trend direction (increasing/decreasing)
- Average change rates
- Confidence in the trend analysis

### Sample Answer:
```
Based on the available data:

Key Findings:
• Average revenue: 7561.40
• Revenue is increasing with average change of +0.8%

Observed Patterns:
• Strong upward trend across most metrics
• High confidence in most evidence

This analysis is based on 2 evidence objects from multiple sources.
```

---

## 2. 🔄 Comparison Analysis

**What it does**: Compares metrics across different segments, time periods, or categories.

### Example Questions:
- "Compare customer retention between enterprise and consumer segments"
- "What's the difference in revenue between Q1 and Q2?"
- "Compare mobile vs desktop user engagement"
- "How do premium users differ from free users in terms of activity?"
- "Which segment has better conversion rates?"

### What You Get:
- Side-by-side metric comparisons
- Percentage differences
- Statistical significance
- Relative performance insights

### Sample Answer:
```
Based on the available data:

Comparisons:
• Revenue: enterprise vs consumer shows 45.2% difference
• Retention: premium vs free shows 28.5% difference

Key Findings:
• Enterprise segment outperforms consumer by significant margin
• Premium users show higher retention rates

This analysis is based on 4 evidence objects from multiple sources.
```

---

## 3. 📊 Segmentation Analysis

**What it does**: Breaks down metrics by different segments, cohorts, or categories.

### Example Questions:
- "Show me user engagement breakdown by segment"
- "What's the distribution of revenue across customer types?"
- "Break down conversion rates by user category"
- "How do different age groups perform in terms of retention?"
- "Segment analysis of sales by region"

### What You Get:
- Metric values for each segment
- Segment-wise distributions
- Relative performance of segments
- Patterns across segments

### Sample Answer:
```
Based on the available data:

Key Findings:
• Enterprise segment: 65.2% of total revenue
• Consumer segment: 34.8% of total revenue
• Premium users: 82% retention rate
• Free users: 54% retention rate

Observed Patterns:
• Clear segmentation in user behavior
• Enterprise and premium segments show stronger metrics

This analysis is based on 6 evidence objects from multiple sources.
```

---

## 4. ⚠️ Anomaly Explanation

**What it does**: Identifies unusual patterns and explains potential causes of spikes, drops, or anomalies.

### Example Questions:
- "Why did revenue spike in March 2024?"
- "Explain the drop in user engagement last week"
- "What caused the unusual increase in conversion rates?"
- "Why is there an anomaly in customer retention this month?"
- "What happened to cause the sales dip?"

### What You Get:
- Baseline vs anomalous values
- Statistical significance of the anomaly
- Potential contributing factors
- Context from related metrics

### Sample Answer:
```
Based on the available data:

Key Findings:
• Baseline revenue: 7200.00
• Anomalous value: 9500.00 (+31.9% deviation)
• Anomaly detected in March 2024

Observed Patterns:
• Significant deviation from historical average
• Concurrent increase in user acquisition
• Seasonal factors may have contributed

This analysis is based on 5 evidence objects from multiple sources.
```

---

## 5. 📋 Descriptive Summary

**What it does**: Provides statistical summaries and current state of metrics.

### Example Questions:
- "Summarize current customer retention metrics"
- "What are the key statistics for revenue?"
- "Give me an overview of user engagement"
- "What's the current state of conversion rates?"
- "Summarize sales performance"

### What You Get:
- Current metric values
- Statistical measures (mean, median, etc.)
- Overall health indicators
- Key performance indicators

### Sample Answer:
```
Based on the available data:

Key Findings:
• Average revenue: 7561.40
• User engagement: 0.72 (72%)
• Customer retention: 0.85 (85%)
• Conversion rate: 0.18 (18%)

Observed Patterns:
• Metrics are within normal ranges
• Strong performance across key indicators

This analysis is based on 8 evidence objects from multiple sources.
```

---

## How the System Works

### 1. Query Classification
Your query is automatically classified into one of the 5 types above.

### 2. Query Decomposition
The system breaks down your question into sub-questions:
- What metrics are needed?
- What segments to analyze?
- What time periods to consider?
- What factors might be relevant?

### 3. Evidence Retrieval
Three parallel retrieval methods:
- **Semantic**: Similar patterns from knowledge base
- **Structured**: Direct data queries and aggregations
- **Statistical**: Trend detection and anomaly analysis

### 4. Multi-Agent Analysis
Four specialized agents process the evidence:
- **Retriever**: Collects and deduplicates evidence
- **Analyst**: Identifies patterns and comparisons
- **Validator**: Checks logical consistency
- **Narrator**: Generates the final answer

### 5. Confidence Scoring
Every answer includes:
- **Coverage Score**: How well evidence covers the query
- **Completeness Score**: Quality of the evidence
- **Overall Confidence**: High/Partial/Insufficient

---

## Advanced Query Examples

### Multi-Metric Queries
"Compare revenue and retention between enterprise and consumer segments"

### Time-Series Analysis
"Show me the month-over-month growth in user engagement for Q1 2024"

### Conditional Queries
"What's the conversion rate for users who signed up in the last 30 days?"

### Cross-Segment Analysis
"How does mobile user engagement compare to desktop across different customer types?"

### Causal Analysis
"What factors contributed to the increase in revenue last quarter?"

---

## Query Best Practices

### ✅ Good Queries
- Specific metrics: "revenue", "retention", "engagement"
- Clear time frames: "last quarter", "Q1 2024", "past month"
- Defined segments: "enterprise", "consumer", "premium"
- Action-oriented: "compare", "show", "analyze", "explain"

### ❌ Avoid
- Too vague: "How are things?"
- No metrics: "What happened?"
- Unclear timeframes: "recently"
- Multiple unrelated questions in one query

---

## Confidence Levels Explained

### 🟢 High Confidence (80%+)
- Complete evidence coverage
- High data quality
- Strong statistical support
- **You can trust these answers**

### 🟡 Partial Evidence (50-80%)
- Some evidence gaps
- Moderate data quality
- Reasonable statistical support
- **Use with some caution**

### 🔴 Insufficient Data (<50%)
- Significant evidence gaps
- Low data quality
- Weak statistical support
- **System will refuse to speculate**

---

## Current Data Coverage

Your system currently has sample data for:
- **Metrics**: revenue, users, engagement, retention, conversion
- **Segments**: enterprise, consumer, premium, free
- **Time Range**: 90 days (Jan 1 - Mar 31, 2024)
- **Data Points**: 1,800 records

### To Add Your Own Data
1. Replace `backend/data/sample_data.csv` with your data
2. Ensure columns: `date`, `metric`, `segment`, `value`
3. Restart the backend
4. Start querying!

---

## Example Query Session

```
Query 1: "What is the trend in revenue over the last quarter?"
→ Trend Analysis
→ High Confidence (100% coverage)
→ Answer: Revenue increasing +0.8%

Query 2: "Compare retention between enterprise and consumer"
→ Comparison Analysis  
→ High Confidence (100% coverage)
→ Answer: Enterprise 15% higher retention

Query 3: "Show me engagement breakdown by segment"
→ Segmentation Analysis
→ High Confidence (100% coverage)
→ Answer: 4 segments analyzed with detailed breakdown

Query 4: "Why did revenue spike in March?"
→ Anomaly Explanation
→ Partial Evidence (65% coverage)
→ Answer: Potential seasonal factors identified

Query 5: "Summarize current metrics"
→ Descriptive Summary
→ High Confidence (95% coverage)
→ Answer: All key metrics within normal ranges
```

---

## Tips for Best Results

1. **Be Specific**: Include metric names, time periods, and segments
2. **One Question at a Time**: Better results than multiple questions
3. **Use Domain Terms**: "revenue", "retention", "conversion" work better than generic terms
4. **Enable Explainability**: See exactly how the system reached its conclusion
5. **Check Confidence**: Always review the confidence score

---

## What the System CANNOT Do

❌ **Predictions**: "What will revenue be next quarter?" (It analyzes past data, not future)
❌ **Causation**: "Did marketing cause the revenue increase?" (It shows correlations, not causation)
❌ **External Data**: "What's our competitor's revenue?" (Only analyzes your data)
❌ **Subjective Opinions**: "Is this good or bad?" (Provides facts, not judgments)
❌ **Real-time Data**: Works with the data you provide, not live streams

---

## Try It Now!

Open the frontend and try these queries:
1. "What is the trend in revenue over the last quarter?"
2. "Compare customer retention between enterprise and consumer segments"
3. "Show me user engagement breakdown by segment"

Watch the cosmic loading animation and see the multi-agent reasoning in action! 🌌✨
