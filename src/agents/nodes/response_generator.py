"""
Response Generator Node
Gera explicação comparativa usando Gemini 2.5 Flash
Justifica por que Marca X é melhor que Marca Y para aquele usuário específico
"""
from typing import Any
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

from src.agents.state import AgentState
from src.infrastructure.llm.gemini import get_llm


async def response_generator(state: AgentState) -> AgentState:
    """
    Node: Response Generator
    Gera resposta comparativa usando Gemini 2.5 Flash
    """
    ranked_products = state.get("ranked_products", [])
    ranking_data = state.get("ranking_data", {})
    scientific_data = state.get("scientific_data", [])
    medical_conditions = state.get("medical_conditions", [])
    dietary_restrictions = state.get("dietary_restrictions", [])
    goal = state.get("goal")

    if not ranked_products:
        state["response"] = "Desculpe, não encontramos produtos adequados para seu perfil."
        state["step"] = "response_generated_no_products"
        return state

    # Preparar contexto para o LLM
    top_3_products = ranked_products[:3]
    product_details = "\n\n".join([
        f"**{i+1}. {p['brand_name']} - {p['product_name']}**\n"
        f"- Score: {p['score']:.1f}/100\n"
        f"- Preço: R$ {p['price']:.2f}\n"
        f"- Razões: {', '.join(p['reasons'])}"
        for i, p in enumerate(top_3_products)
    ])

    scientific_context = ""
    if scientific_data:
        for data in scientific_data[:2]:  # Top 2 evidências
            scientific_context += f"\n- **{data['supplement_name']}** ({data['source']}): "
            effects = data.get("effects", {})
            scientific_context += ", ".join([f"{k} ({v})" for k, v in list(effects.items())[:3]])
            dosage = data.get("dosage", {})
            if dosage:
                scientific_context += f". Dosagem: {dosage.get('min', '')}-{dosage.get('max', '')} {dosage.get('unit', '')}"

    user_context = ""
    if medical_conditions:
        user_context += f"\n- Condições médicas: {', '.join(medical_conditions)}"
    if dietary_restrictions:
        user_context += f"\n- Restrições alimentares: {', '.join(dietary_restrictions)}"
    if goal:
        user_context += f"\n- Objetivo: {goal}"

    # Prompt template
    prompt = ChatPromptTemplate.from_messages([
        ("system", """Você é um especialista em suplementos esportivos que faz recomendações 
personalizadas baseadas em evidência científica (AIS Group A / Examine.com).

Sua tarefa é explicar de forma clara e objetiva por que determinado produto é melhor 
que outro para o usuário específico, considerando:
- Condições médicas (ex: diabetes = evitar maltodextrina)
- Restrições alimentares (ex: vegan, sem lactose)
- Evidência científica
- Custo-benefício

Seja específico e justifique cada recomendação."""),
        ("user", """Baseado nas seguintes informações, gere uma recomendação personalizada:

**Produtos Ranqueados:**
{product_details}

**Contexto Científico:**
{scientific_context}

**Perfil do Usuário:**
{user_context}

Gere uma resposta que:
1. Recomende o melhor produto (top 1) e explique por quê
2. Compare com os outros produtos se relevante
3. Justifique considerando condições médicas, restrições e evidência científica
4. Seja claro, objetivo e profissional

Resposta:"""),
    ])

    try:
        llm = get_llm()
        chain = prompt | llm | StrOutputParser()

        response = await chain.ainvoke({
            "product_details": product_details,
            "scientific_context": scientific_context,
            "user_context": user_context,
        })

        state["response"] = response
        state["explanation"] = response
        state["step"] = "response_generated"

    except Exception as e:
        # Fallback para resposta simples sem LLM
        top_product = ranked_products[0]
        state["response"] = (
            f"Recomendo {top_product['brand_name']} - {top_product['product_name']} "
            f"(Score: {top_product['score']:.1f}/100). "
            f"Razões: {', '.join(top_product['reasons'][:3])}"
        )
        state["step"] = "response_generated_fallback"
        state["errors"] = state.get("errors", []) + [f"LLM error: {str(e)}"]

    return state

