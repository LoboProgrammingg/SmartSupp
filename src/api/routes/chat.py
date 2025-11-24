"""
Chat/Recommendation Routes
POST /chat - Endpoint principal para consultas
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.schemas import ChatRequest, ChatResponse
from src.api.dependencies import get_db_session, get_tenant_id_from_header
from src.agents.runner import run_agent

router = APIRouter(prefix="/chat", tags=["chat"])


@router.post("", response_model=ChatResponse, status_code=status.HTTP_200_OK)
async def chat(
    request: ChatRequest,
    tenant_id: int = Depends(get_tenant_id_from_header),
    session: AsyncSession = Depends(get_db_session),
) -> ChatResponse:
    """
    Endpoint principal para consultas e recomendações
    
    Processa o input do usuário através do agente LangGraph completo:
    1. Anamnesis - Coleta dados do usuário
    2. Science - Consulta base científica
    3. Inventory - Consulta estoque do tenant
    4. Matchmaking - Compara e ranqueia produtos
    5. Response - Gera explicação personalizada
    6. Analytics - Salva interação para BI
    """
    try:
        result = await run_agent(
            user_input=request.user_input,
            tenant_id=tenant_id,
            user_profile_id=request.user_profile_id,
            session=session,
            session_id=request.session_id,
        )

        return ChatResponse(
            response=result.get("response", "Erro ao processar requisição"),
            explanation=result.get("explanation"),
            recommended_product_ids=result.get("recommended_product_ids", []),
            ranking_data=result.get("ranking_data"),
            session_id=result.get("session_id", ""),
            step=result.get("step", "unknown"),
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao processar requisição: {str(e)}",
        )

