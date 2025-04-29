from fastapi import APIRouter

from search.api.routes import chat, courses

api_router = APIRouter()
api_router.include_router(courses.router, prefix="/courses")
api_router.include_router(chat.router)
