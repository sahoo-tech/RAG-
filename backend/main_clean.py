"""
Suppress unnecessary warnings when starting the RAG++ server.
"""

import os
import warnings

# Suppress TensorFlow warnings
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'

# Suppress protobuf warnings
os.environ['PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION'] = 'python'

# Suppress other warnings
warnings.filterwarnings('ignore', category=UserWarning)
warnings.filterwarnings('ignore', category=FutureWarning)
warnings.filterwarnings('ignore', category=DeprecationWarning)

# Now import and run the main application
from api.server import app
from utils.logger import configure_logging, get_logger
from config import get_settings

# Configure logging
configure_logging()

logger = get_logger(__name__)
settings = get_settings()


def main():
    """Main entry point with suppressed warnings."""
    import uvicorn
    
    logger.info("=" * 60)
    logger.info("RAG++ Analytical Reasoning Engine")
    logger.info("=" * 60)
    logger.info("Starting server",
               host=settings.api_host,
               port=settings.api_port,
               model=settings.ollama_model)
    
    try:
        uvicorn.run(
            "api.server:app",
            host=settings.api_host,
            port=settings.api_port,
            log_level="warning",  # Reduce uvicorn verbosity
            reload=False
        )
    except KeyboardInterrupt:
        logger.info("Server stopped by user")
    except Exception as e:
        logger.error("Server error", error=str(e), exc_info=True)
        import sys
        sys.exit(1)


if __name__ == "__main__":
    main()
