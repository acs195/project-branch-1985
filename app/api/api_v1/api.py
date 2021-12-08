"""This module registers all the routes for api_v1"""

from fastapi import APIRouter

from app.api.api_v1.endpoints import branch

api_router = APIRouter()

api_router.include_router(branch.router, prefix="/branch", tags=["branch"])
