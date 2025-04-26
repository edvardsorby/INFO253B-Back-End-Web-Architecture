from fastapi import APIRouter

from search.db import Database
from search.models import SearchOut
from search.services import retrieve_courses

router = APIRouter(tags=["courses"])


@router.get("/search")
async def search(query: str, db: Database) -> list[SearchOut]:
    return await retrieve_courses(query, db)
