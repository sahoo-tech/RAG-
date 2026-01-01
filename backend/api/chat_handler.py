"""
Chat endpoint for conversational AI using Ollama with streaming support.
"""

from typing import List, Dict, Any, AsyncGenerator
from pydantic import BaseModel
import ollama
import json
from utils.logger import get_logger
from config import get_settings

logger = get_logger(__name__)
settings = get_settings()


class ChatMessage(BaseModel):
    """Single chat message."""
    role: str
    content: str


class ChatRequest(BaseModel):
    """Chat request with conversation history."""
    messages: List[ChatMessage]
    model: str = None


class ChatResponse(BaseModel):
    """Chat response."""
    success: bool
    message: str
    error: str = None


async def chat_with_ollama_stream(request: ChatRequest) -> AsyncGenerator[str, None]:
    """
    Chat with Ollama model using streaming for real-time token generation.
    
    Args:
        request: ChatRequest with conversation history
        
    Yields:
        JSON strings with streaming tokens or error messages
    """
    try:
        model = request.model or settings.ollama_model
        
        messages = [{"role": msg.role, "content": msg.content} for msg in request.messages]
        
        logger.info("Processing streaming chat request", 
                   model=model,
                   message_count=len(messages))
        
        stream = ollama.chat(
            model=model,
            messages=messages,
            stream=True,
            options={
                "temperature": 0.7,
                "num_predict": 1000,
                "num_ctx": 4096
            }
        )
        
        for chunk in stream:
            if 'message' in chunk and 'content' in chunk['message']:
                token = chunk['message']['content']
                yield f"data: {json.dumps({'token': token, 'done': False})}\n\n"
        
        yield f"data: {json.dumps({'token': '', 'done': True})}\n\n"
        
        logger.info("Streaming chat response completed")
        
    except Exception as e:
        logger.error("Streaming chat request failed", error=str(e), exc_info=True)
        error_data = {
            'error': f"Chat error: {str(e)}",
            'done': True
        }
        yield f"data: {json.dumps(error_data)}\n\n"


async def chat_with_ollama(request: ChatRequest) -> ChatResponse:
    """
    Chat with Ollama model (non-streaming fallback).
    
    Args:
        request: ChatRequest with conversation history
        
    Returns:
        ChatResponse with assistant's reply
    """
    try:
        model = request.model or settings.ollama_model
        
        messages = [{"role": msg.role, "content": msg.content} for msg in request.messages]
        
        logger.info("Processing chat request", 
                   model=model,
                   message_count=len(messages))
        
        response = ollama.chat(
            model=model,
            messages=messages,
            options={
                "temperature": 0.7,
                "num_predict": 1000,
                "num_ctx": 4096
            }
        )
        
        assistant_message = response['message']['content']
        
        logger.info("Chat response generated",
                   response_length=len(assistant_message))
        
        return ChatResponse(
            success=True,
            message=assistant_message
        )
        
    except Exception as e:
        logger.error("Chat request failed", error=str(e), exc_info=True)
        return ChatResponse(
            success=False,
            message="",
            error=f"Chat error: {str(e)}"
        )
