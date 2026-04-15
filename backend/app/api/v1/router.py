"""API v1 router — aggregates all sub-routers."""

from fastapi import APIRouter

from app.api.v1 import auth, contracts, clauses, playbooks, risks, ws

api_router = APIRouter()

api_router.include_router(auth.router)
api_router.include_router(contracts.router)
api_router.include_router(clauses.router)
api_router.include_router(playbooks.router)
api_router.include_router(risks.router)

# WebSocket routes have their own prefix defined in the ws module
api_router.include_router(ws.router)
