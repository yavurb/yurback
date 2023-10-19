from api.endpoints import assets
from fastapi import APIRouter

from src.api.endpoints import auth, posts, projects

api_router = APIRouter()

api_router.include_router(posts.router, prefix="/posts", tags=["posts"])
api_router.include_router(projects.router, prefix="/projects", tags=["projects"])
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(assets.router, prefix="/assets", tags=["assets"])
