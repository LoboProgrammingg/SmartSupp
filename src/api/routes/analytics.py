"""
Analytics Routes
GET /analytics/brand-performance - Analytics de marcas
"""
from datetime import datetime, timedelta
from typing import Optional
from fastapi import APIRouter, Depends, Query, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select, func

from src.api.schemas import AnalyticsResponse, BrandPerformanceResponse
from src.api.dependencies import get_db_session, get_tenant_id_from_header
from src.domain.models import InteractionLog, Product

router = APIRouter(prefix="/analytics", tags=["analytics"])


@router.get("/brand-performance", response_model=AnalyticsResponse)
async def get_brand_performance(
    days: int = Query(30, ge=1, le=365, description="Período em dias"),
    tenant_id: int = Depends(get_tenant_id_from_header),
    session: AsyncSession = Depends(get_db_session),
) -> AnalyticsResponse:
    """
    Analytics de performance de marcas
    
    Retorna estatísticas de:
    - Quantidade de recomendações por produto
    - Taxa de conversão (seleções / recomendações)
    - Score médio de satisfação (se disponível)
    """
    period_end = datetime.utcnow()
    period_start = period_end - timedelta(days=days)

    # Buscar interações do período
    stmt = (
        select(InteractionLog)
        .where(InteractionLog.tenant_id == tenant_id)
        .where(InteractionLog.created_at >= period_start)
        .where(InteractionLog.created_at <= period_end)
    )
    interactions = (await session.exec(stmt)).all()

    # Agregar dados por produto
    product_stats: dict[int, dict] = {}

    for interaction in interactions:
        recommended_product_ids = [
            int(pid) for pid in interaction.recommended_products if pid.isdigit()
        ]

        for product_id in recommended_product_ids:
            if product_id not in product_stats:
                product_stats[product_id] = {
                    "recommendation_count": 0,
                    "selection_count": 0,
                    "total_satisfaction": 0.0,
                    "satisfaction_count": 0,
                }

            product_stats[product_id]["recommendation_count"] += 1

            if interaction.selected_product_id == product_id:
                product_stats[product_id]["selection_count"] += 1

            if interaction.satisfaction_score:
                product_stats[product_id]["total_satisfaction"] += interaction.satisfaction_score
                product_stats[product_id]["satisfaction_count"] += 1

    # Buscar informações dos produtos
    if product_stats:
        product_ids = list(product_stats.keys())
        stmt = select(Product).where(Product.id.in_(product_ids))  # type: ignore
        products = (await session.exec(stmt)).all()
        product_dict = {p.id: p for p in products}

        brand_performance = []
        for product_id, stats in product_stats.items():
            if product_id in product_dict:
                product = product_dict[product_id]
                avg_satisfaction = None
                if stats["satisfaction_count"] > 0:
                    avg_satisfaction = stats["total_satisfaction"] / stats["satisfaction_count"]

                conversion_rate = 0.0
                if stats["recommendation_count"] > 0:
                    conversion_rate = stats["selection_count"] / stats["recommendation_count"]

                brand_performance.append(
                    BrandPerformanceResponse(
                        brand_name=product.brand_name,
                        product_name=product.product_name,
                        recommendation_count=stats["recommendation_count"],
                        avg_satisfaction=avg_satisfaction,
                        total_selections=stats["selection_count"],
                        conversion_rate=round(conversion_rate, 4),
                    )
                )

        # Ordenar por recommendation_count (maior primeiro)
        brand_performance.sort(key=lambda x: x.recommendation_count, reverse=True)
    else:
        brand_performance = []

    return AnalyticsResponse(
        tenant_id=tenant_id,
        period_start=period_start,
        period_end=period_end,
        total_interactions=len(interactions),
        brand_performance=brand_performance,
    )

