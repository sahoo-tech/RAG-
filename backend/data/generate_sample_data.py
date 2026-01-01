"""
Sample data initialization for RAG++ system.
Creates a CSV file with sample analytical data.
"""

import pandas as pd
from datetime import datetime, timedelta
import numpy as np


def create_sample_data():
    """Create sample analytical dataset."""
    
    # Set random seed for reproducibility
    np.random.seed(42)
    
    # Generate date range
    start_date = datetime(2024, 1, 1)
    dates = [start_date + timedelta(days=i) for i in range(90)]
    
    # Metrics
    metrics = ['revenue', 'users', 'engagement', 'retention', 'conversion']
    segments = ['enterprise', 'consumer', 'premium', 'free']
    
    data = []
    
    for date in dates:
        for metric in metrics:
            for segment in segments:
                # Generate realistic values based on metric type
                if metric == 'revenue':
                    base = 10000 if segment in ['enterprise', 'premium'] else 5000
                    value = base + np.random.normal(0, base * 0.1)
                elif metric == 'users':
                    base = 1000 if segment in ['enterprise', 'premium'] else 5000
                    value = base + np.random.normal(0, base * 0.05)
                elif metric in ['engagement', 'retention', 'conversion']:
                    base = 0.75 if segment in ['enterprise', 'premium'] else 0.65
                    value = max(0, min(1, base + np.random.normal(0, 0.05)))
                else:
                    value = np.random.uniform(0, 100)
                
                data.append({
                    'date': date.strftime('%Y-%m-%d'),
                    'metric': metric,
                    'segment': segment,
                    'value': round(value, 2)
                })
    
    # Create DataFrame
    df = pd.DataFrame(data)
    
    # Save to CSV
    output_path = './data/sample_data.csv'
    df.to_csv(output_path, index=False)
    
    print(f"Sample data created: {output_path}")
    print(f"Total rows: {len(df)}")
    print(f"Date range: {df['date'].min()} to {df['date'].max()}")
    print(f"Metrics: {df['metric'].unique()}")
    print(f"Segments: {df['segment'].unique()}")


if __name__ == "__main__":
    import os
    os.makedirs('./data', exist_ok=True)
    create_sample_data()
