"""
Main entry point for RAG++ system.
"""

import sys
from api.server import app
from utils.logger import configure_logging, get_logger
from config import get_settings

# Configure logging
configure_logging()

logger = get_logger(__name__)
settings = get_settings()


def main():
    """Main entry point."""
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
            log_level=settings.log_level.lower(),
            reload=False
        )
    except KeyboardInterrupt:
        logger.info("Server stopped by user")
    except Exception as e:
        logger.error("Server error", error=str(e), exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
