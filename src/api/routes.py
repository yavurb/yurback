from fastapi import APIRouter

from src.api.endpoints import posts, projects

api_router = APIRouter()

api_router.include_router(posts.router, prefix="/posts", tags=["posts"])
api_router.include_router(projects.router, prefix="/projects", tags=["projects"])
