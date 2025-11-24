"""
Agent Utilities
Funções auxiliares para nodes do LangGraph
"""
from typing import Any
from sqlalchemy.ext.asyncio import AsyncSession


def get_session_from_config(config: dict[str, Any] | None) -> AsyncSession | None:
    """Extrai sessão do config do LangGraph"""
    if not config:
        return None
    configurable = config.get("configurable", {})
    return configurable.get("session")


def node_with_session(node_func: Any) -> Any:
    """
    Decorator para nodes que precisam de sessão de banco
    Extrai sessão do config e passa como argumento
    """
    async def wrapper(state: dict[str, Any], config: dict[str, Any] | None = None):
        session = get_session_from_config(config)
        if session:
            return await node_func(state, session)
        return await node_func(state)
    return wrapper

