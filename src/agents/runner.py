"""
Agent Runner
Executa o agente LangGraph com contexto de sessão de banco
"""
from typing import Any
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import uuid4

from src.agents.state import AgentState
from src.agents.graph import get_graph


async def run_agent(
    user_input: str,
    tenant_id: int,
    user_profile_id: int | None,
    session: AsyncSession,
    session_id: str | None = None,
) -> dict[str, Any]:
    """
    Executa o agente LangGraph completo
    
    Args:
        user_input: Input do usuário (pergunta/requisição)
        tenant_id: ID do tenant (multitenancy)
        user_profile_id: ID do perfil do usuário (opcional)
        session: Sessão assíncrona do banco
        session_id: ID da sessão (opcional, gera UUID se não fornecido)
    
    Returns:
        Estado final do agente com resposta e dados
    """
    if session_id is None:
        session_id = str(uuid4())

    # Estado inicial
    initial_state: AgentState = {
        "session_id": session_id,
        "tenant_id": tenant_id,
        "user_profile_id": user_profile_id,
        "user_input": user_input,
        "query_text": user_input,
        "biometrics": None,
        "goal": None,
        "dietary_restrictions": None,
        "medical_conditions": None,
        "budget_range": None,
        "scientific_data": None,
        "recommended_category": None,
        "available_products": None,
        "filtered_products": None,
        "ranked_products": None,
        "ranking_data": None,
        "response": None,
        "explanation": None,
        "recommended_product_ids": None,
        "errors": None,
        "step": "initialized",
    }

    graph = get_graph()

    # Executar grafo com contexto de sessão
    # LangGraph suporta passar contexto adicional via config
    config = {"configurable": {"session": session}}

    try:
        final_state = await graph.ainvoke(initial_state, config=config)
        return dict(final_state)
    except Exception as e:
        return {
            **initial_state,
            "response": f"Erro ao processar requisição: {str(e)}",
            "errors": [str(e)],
            "step": "error",
        }

