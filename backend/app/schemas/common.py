"""Common / shared schemas."""

from uuid import UUID
from pydantic import BaseModel


class MessageResponse(BaseModel):
    message: str


class PaginationParams(BaseModel):
    page: int = 1
    size: int = 20


class PaginatedResponse(BaseModel):
    total: int
    page: int
    size: int
    items: list
