"""
LangGraph Orkestratör — Ana agent akış yönetimi.

Akış:
  Ingestion → Clause → Risk → Negotiation → Approval

Her node bir agent'ı temsil eder ve LangGraph state machine'i
üzerinden yönetilir.
"""

from typing import TypedDict


class ContractReviewState(TypedDict):
    """Agent akışının paylaşılan durumu."""

    contract_id: str
    raw_text: str
    clauses: list[dict]
    risk_scores: list[dict]
    revisions: list[dict]
    approval_status: str
    errors: list[str]


# TODO: LangGraph StateGraph tanımı
# from langgraph.graph import StateGraph
#
# workflow = StateGraph(ContractReviewState)
# workflow.add_node("ingestion", ingestion_agent)
# workflow.add_node("clause", clause_agent)
# workflow.add_node("risk", risk_agent)
# workflow.add_node("negotiation", negotiation_agent)
# workflow.add_node("approval", approval_agent)
#
# workflow.add_edge("ingestion", "clause")
# workflow.add_edge("clause", "risk")
# workflow.add_edge("risk", "negotiation")
# workflow.add_edge("negotiation", "approval")
#
# workflow.set_entry_point("ingestion")
# graph = workflow.compile()
