from fastapi import APIRouter, Depends

from search.auth.dependencies import require_admin
from search.db import Database
from search.models import Course, CourseUpdate, SearchOut
from search.services import retrieve_courses
from search.services.crud import add_course, delete_course, get_course, update_course

router = APIRouter(tags=["courses"])


@router.get("/search")
async def search(query: str, db: Database) -> list[SearchOut]:
    return await retrieve_courses(query, db)

@router.get("/{id}")
async def get(id: str, db: Database, user=Depends(require_admin)):
    return await get_course(id, db)

@router.post("")
async def post(course: Course, db: Database, user=Depends(require_admin)):
    return await add_course(course, db)

@router.put("/{id}")
async def update(id: str, course: CourseUpdate, db: Database, user=Depends(require_admin)):
    return await update_course(id, course, db)

@router.delete("/{id}")
async def delete(id: str, db: Database, user=Depends(require_admin)):
    return await delete_course(id, db)

# Example use:
# Include Authorization header with JWT token in the request
#
# Algorithm: HS256
# Secret: your-secret
# Payload:
# {
#     "sub": "admin_user",
#     "role": "admin"
# }