import voyageai
from fastapi import APIRouter
from search.db import Database
from search.models import SearchOut

router = APIRouter(tags=["courses"])


@router.get("/search")
async def search(query: str, db: Database) -> list[SearchOut]:
    vo = voyageai.Client()
    query_embed = vo.embed(
        query, model="voyage-3-large", input_type="query"
    ).embeddings[0]

    pipeline = [
        {
            "$vectorSearch": {
                "index": "vector_index",
                "path": "embedding",
                "queryVector": query_embed,
                "numCandidates": 150,
                "limit": 10,
            }
        },
        {
            "$project": {
                "embedding": 0,
                "_id": 0,
                "score": {"$meta": "vectorSearchScore"},
            }
        },
    ]

    db_response = await db.aggregate(pipeline)
    results = []
    async for course in db_response:
        results.append(SearchOut(**course))
    return results
