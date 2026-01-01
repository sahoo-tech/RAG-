"""
Request logging and error handling middleware.
"""

from fastapi import Request, status
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
import time
from utils.logger import get_logger

logger = get_logger(__name__)


class LoggingMiddleware(BaseHTTPMiddleware):
    """Logs all incoming requests and responses."""
    
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()
        
        # Log request
        logger.info("Request received",
                   method=request.method,
                   path=request.url.path,
                   client=request.client.host if request.client else "unknown")
        
        try:
            response = await call_next(request)
            
            # Log response
            duration = (time.time() - start_time) * 1000
            logger.info("Request completed",
                       method=request.method,
                       path=request.url.path,
                       status_code=response.status_code,
                       duration_ms=duration)
            
            return response
        
        except Exception as e:
            logger.error("Request failed",
                        method=request.method,
                        path=request.url.path,
                        error=str(e))
            
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content={"error": "Internal server error", "detail": str(e)}
            )


class ErrorHandlingMiddleware(BaseHTTPMiddleware):
    """Handles errors and returns appropriate responses."""
    
    async def dispatch(self, request: Request, call_next):
        try:
            return await call_next(request)
        except ValueError as e:
            logger.warning("Validation error", error=str(e))
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={"error": "Validation error", "detail": str(e)}
            )
        except Exception as e:
            logger.error("Unexpected error", error=str(e), exc_info=True)
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content={"error": "Internal server error"}
            )
