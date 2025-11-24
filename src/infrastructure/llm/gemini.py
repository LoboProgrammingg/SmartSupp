"""
Google Gemini 2.5 Flash Integration
Integração com Vertex AI ou Google AI Studio
"""
from typing import Optional
from langchain_google_vertexai import ChatVertexAI
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.language_models import BaseChatModel

from src.core.config import settings


def get_llm() -> BaseChatModel:
    """
    Retorna instância do LLM (Gemini 2.5 Flash)
    Prioriza Vertex AI, fallback para Google AI Studio
    """
    if settings.GOOGLE_CLOUD_PROJECT and settings.GOOGLE_APPLICATION_CREDENTIALS:
        # Vertex AI (produção)
        return ChatVertexAI(
            model_name=settings.GEMINI_MODEL,
            project=settings.GOOGLE_CLOUD_PROJECT,
            location=settings.VERTEX_AI_LOCATION,
            temperature=0.7,
            max_output_tokens=2048,
        )
    
    # Google AI Studio (desenvolvimento/teste)
    # Requer GOOGLE_API_KEY no .env
    api_key = getattr(settings, "GOOGLE_API_KEY", None)
    if api_key:
        return ChatGoogleGenerativeAI(
            model=settings.GEMINI_MODEL,
            google_api_key=api_key,
            temperature=0.7,
            max_output_tokens=2048,
        )
    
    raise ValueError(
        "Configuração LLM inválida. "
        "Configure GOOGLE_CLOUD_PROJECT + GOOGLE_APPLICATION_CREDENTIALS "
        "ou GOOGLE_API_KEY no .env"
    )

