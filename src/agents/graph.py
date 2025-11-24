"""
LangGraph Graph Builder
Orquestra todos os nodes do fluxo de recomendação
"""
from typing import Any
from langgraph.graph import StateGraph, END
from sqlalchemy.ext.asyncio import AsyncSession

from src.agents.state import AgentState
from src.agents.nodes.anamnesis_collector import anamnesis_collector
from src.agents.nodes.science_retriever import science_retriever
from src.agents.nodes.comparative_analysis import comparative_analysis
from src.agents.nodes.response_generator import response_generator
from src.agents.nodes.analytics_logger import analytics_logger


def create_graph() -> StateGraph:
    """
    Cria e retorna o grafo LangGraph
    Fluxo: Anamnesis → Science → Analysis → Response → Analytics
    """
    workflow = StateGraph(AgentState)

    # Adicionar nodes
    workflow.add_node("anamnesis_collector", anamnesis_collector)
    workflow.add_node("science_retriever", science_retriever)
    workflow.add_node("comparative_analysis", comparative_analysis)
    workflow.add_node("response_generator", response_generator)
    workflow.add_node("analytics_logger", analytics_logger)

    # Definir fluxo linear
    workflow.set_entry_point("anamnesis_collector")
    workflow.add_edge("anamnesis_collector", "science_retriever")
    workflow.add_edge("science_retriever", "comparative_analysis")
    workflow.add_edge("comparative_analysis", "response_generator")
    workflow.add_edge("response_generator", "analytics_logger")
    workflow.add_edge("analytics_logger", END)

    return workflow.compile()


# Singleton do grafo compilado
_compiled_graph: Any = None


def get_graph() -> StateGraph:
    """Retorna instância singleton do grafo compilado"""
    global _compiled_graph
    if _compiled_graph is None:
        _compiled_graph = create_graph()
    return _compiled_graph

