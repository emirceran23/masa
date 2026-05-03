"""Structured output schema for the Negotiation Agent."""

from pydantic import BaseModel


class NegotiationAgentOutput(BaseModel):
    suggested_text: str
    context_used: str
