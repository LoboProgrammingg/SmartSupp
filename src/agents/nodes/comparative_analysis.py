"""
Comparative Analysis Node (Matchmaking)
Cruza UserProfile com Product.nutritional_info e ranqueia marcas
"""
from typing import Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from src.agents.state import AgentState
from src.domain.models import Product
from src.domain.enums import SupplementCategory, DietaryRestriction, MedicalCondition


async def comparative_analysis(state: AgentState, session: AsyncSession) -> AgentState:
    """
    Node: Comparative Analysis (Matchmaking)
    Filtra e ranqueia produtos baseado em:
    - Condições médicas (ex: diabetes = sem maltodextrina)
    - Restrições alimentares (ex: vegan, sem lactose)
    - Custo-benefício (preço por grama de proteína)
    - Disponibilidade em estoque
    """
    tenant_id = state.get("tenant_id")
    category = state.get("recommended_category")
    dietary_restrictions = state.get("dietary_restrictions", [])
    medical_conditions = state.get("medical_conditions", [])
    budget_range = state.get("budget_range")

    if not tenant_id or not category:
        state["errors"] = state.get("errors", []) + ["Tenant ou categoria não definidos"]
        state["step"] = "comparative_analysis_failed"
        return state

    # Buscar produtos disponíveis do tenant
    stmt = (
        select(Product)
        .where(Product.tenant_id == tenant_id)
        .where(Product.category == SupplementCategory(category))
        .where(Product.is_active == True)
        .where(Product.stock_quantity > 0)
    )
    products = (await session.exec(stmt)).all()

    # Filtrar produtos baseado em restrições e condições
    filtered_products = []
    for product in products:
        nutritional_info = product.nutritional_info or {}

        # Verificar contraindicações médicas
        is_valid = True
        reasons = []

        # Diabetes: evitar maltodextrina
        if MedicalCondition.DIABETES.value in medical_conditions:
            if nutritional_info.get("maltodextrin", False):
                is_valid = False
                reasons.append("Contém maltodextrina (contraindicado para diabetes)")

        # Intolerância à lactose
        if DietaryRestriction.LACTOSE_FREE.value in dietary_restrictions:
            if not nutritional_info.get("no_lactose", False):
                is_valid = False
                reasons.append("Contém lactose")

        # Vegan
        if DietaryRestriction.VEGAN.value in dietary_restrictions:
            if not nutritional_info.get("vegan", False):
                is_valid = False
                reasons.append("Não é vegano")

        # Sem glúten
        if DietaryRestriction.GLUTEN_FREE.value in dietary_restrictions:
            if not nutritional_info.get("no_gluten", False):
                is_valid = False
                reasons.append("Contém glúten")

        # Evitar adoçantes artificiais
        if DietaryRestriction.NO_ARTIFICIAL_SWEETENERS.value in dietary_restrictions:
            if nutritional_info.get("artificial_sweeteners", False):
                is_valid = False
                reasons.append("Contém adoçantes artificiais")

        if is_valid:
            filtered_products.append(product)

    # Ranquear produtos por score
    ranked_products = []
    ranking_data: dict[str, dict[str, Any]] = {}

    for product in filtered_products:
        nutritional_info = product.nutritional_info or {}
        protein_g = nutritional_info.get("protein_g", 0.0)

        # Calcular score (0-100)
        score = 0.0
        reasons_positives = []

        # Score de proteína (peso: 40%)
        if protein_g > 0:
            protein_score = min(100, (protein_g / 30.0) * 100)
            score += protein_score * 0.4
            reasons_positives.append(f"Alto teor de proteína ({protein_g}g)")

        # Score de custo-benefício (peso: 30%)
        if protein_g > 0:
            price_per_protein = product.price / protein_g
            cost_benefit_score = max(0, 100 - (price_per_protein * 2))  # Menor preço = maior score
            score += cost_benefit_score * 0.3
            reasons_positives.append(f"Bom custo-benefício (R$ {price_per_protein:.2f}/g proteína)")

        # Score de certificações (peso: 20%)
        certifications = product.certifications or []
        cert_score = len(certifications) * 20  # Max 100 para 5+ certificações
        score += min(100, cert_score) * 0.2
        if certifications:
            reasons_positives.append(f"Certificações: {', '.join(certifications)}")

        # Score de pureza/ingredientes (peso: 10%)
        # Produtos sem aditivos desnecessários ganham pontos
        if not nutritional_info.get("artificial_sweeteners", False):
            score += 10
            reasons_positives.append("Sem adoçantes artificiais")

        if not nutritional_info.get("maltodextrin", False):
            score += 10
            reasons_positives.append("Sem maltodextrina")

        # Normalizar score (0-100)
        score = min(100, max(0, score))

        ranked_products.append({
            "id": product.id,
            "brand_name": product.brand_name,
            "product_name": product.product_name,
            "price": product.price,
            "score": score,
            "reasons": reasons_positives,
        })

        ranking_data[str(product.id)] = {
            "score": score,
            "reasons": reasons_positives,
            "match_score": score / 100.0,
        }

    # Ordenar por score (maior primeiro)
    ranked_products.sort(key=lambda x: x["score"], reverse=True)

    state["available_products"] = [{"id": p.id, "brand_name": p.brand_name, "product_name": p.product_name} for p in products]
    state["filtered_products"] = [{"id": p.id, "brand_name": p.brand_name, "product_name": p.product_name} for p in filtered_products]
    state["ranked_products"] = ranked_products
    state["ranking_data"] = ranking_data
    state["recommended_product_ids"] = [p["id"] for p in ranked_products[:3]]  # Top 3
    state["step"] = "comparative_analysis_complete"

    return state

