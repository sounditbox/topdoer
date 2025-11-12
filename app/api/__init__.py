from fastapi import APIRouter

from .incidents import router as incidents_router

__all__ = ["get_api_router"]


def get_api_router() -> APIRouter:
    api_router = APIRouter()
    api_router.include_router(incidents_router)
    return api_router

