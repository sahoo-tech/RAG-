"""
Configuration management for RAG++ system.
All settings are loaded from environment variables with sensible defaults.
"""

from pydantic_settings import BaseSettings
from typing import Optional
import os


class Settings(BaseSettings):
    """System-wide configuration settings."""
    
    # Ollama Configuration
    ollama_base_url: str = "http://localhost:11434"
    ollama_model: str = "llama2"
    ollama_timeout: int = 120
    
    # Server Configuration
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    log_level: str = "INFO"
    
    # Retrieval Configuration
    faiss_index_path: str = "./data/faiss_index"
    embedding_model: str = "all-MiniLM-L6-v2"
    max_retrieval_results: int = 10
    semantic_similarity_threshold: float = 0.7
    
    # Confidence Thresholds
    high_confidence_threshold: float = 0.8
    partial_confidence_threshold: float = 0.5
    
    # Statistical Analysis
    significance_threshold: float = 0.05
    min_sample_size: int = 30
    trend_window_size: int = 5
    
    # Data Paths
    data_dir: str = "./data"
    vector_store_dir: str = "./data/vector_store"
    sample_data_path: str = "./data/sample_data.csv"
    
    # Agent Configuration
    max_agent_iterations: int = 3
    agent_temperature: float = 0.1  # Low temperature for deterministic responses
    
    # Evidence Configuration
    max_evidence_objects: int = 50
    evidence_dedup_threshold: float = 0.9
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False


# Global settings instance
settings = Settings()


def get_settings() -> Settings:
    """Get the global settings instance."""
    return settings
