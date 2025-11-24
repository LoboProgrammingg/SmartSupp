"""
Analytics Logger Node
Salva interação no banco para BI e Analytics
"""
from typing import Any
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import uuid4

from src.agents.state import AgentState
from src.domain.models import InteractionLog


async def analytics_logger(state: AgentState, session: AsyncSession) -> AgentState:
    """
    Node: Analytics Logger
    Salva log de interação para BI
    """
    tenant_id = state.get("tenant_id")
    user_profile_id = state.get("user_profile_id")
    session_id = state.get("session_id", str(uuid4()))
    query_text = state.get("query_text") or state.get("user_input")
    recommended_product_ids = state.get("recommended_product_ids", [])
    ranking_data = state.get("ranking_data", {})
    response = state.get("response")

    if not tenant_id:
        state["errors"] = state.get("errors", []) + ["Tenant não definido para logging"]
        state["step"] = "analytics_logging_failed"
        return state

    try:
        log_entry = InteractionLog(
            tenant_id=tenant_id,
            user_profile_id=user_profile_id,
            session_id=session_id,
            query_text=query_text,
            recommended_products=[str(pid) for pid in recommended_product_ids],
            ranking_data=ranking_data,
            created_at=datetime.utcnow(),
        )

        session.add(log_entry)
        await session.commit()

        state["step"] = "analytics_logged"
        return state

    except Exception as e:
        # Log erro mas não falha o fluxo
        state["errors"] = state.get("errors", []) + [f"Analytics logging error: {str(e)}"]
        state["step"] = "analytics_logging_error"
        return state

