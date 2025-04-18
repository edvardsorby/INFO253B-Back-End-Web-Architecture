from fastapi import APIRouter
from search.api.routes import courses

api_router = APIRouter()
api_router.include_router(courses.router, prefix="/courses")
