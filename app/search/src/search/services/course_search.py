from typing import Annotated

import voyageai
from langchain_core.tools import tool
from pymongo import AsyncMongoClient

from search.db import get_db
from search.models import SearchOut

COURSE_DETAILS_TEMPLATE = """\
Retrieved Course #{rank}:

Course Title:
{number} {title}

Course Description:
{description}

Dot product similarity score:
{score}"""


async def retrieve_courses(query: str, db: AsyncMongoClient):
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


@tool
async def retrieve_courses_tool(
    query: Annotated[
        str,
        "The query used to retrieve relevant courses from a vector database. This query is used for semantic search",
    ],
):
    """This tool enables you to search a vector database of UC Berkeley courses by providing a natural language query. The database includes all courses in all departments with their titles and descriptions and will retrieve the 10 most relevant courses to a particular query based on semantic similarity to the titles and description."""
    db = get_db()
    retrieved_courses = await retrieve_courses(query, db)

    return {
        "relevant_courses": "\n\n==================\n\n".join(
            [
                COURSE_DETAILS_TEMPLATE.format(
                    rank=i,
                    number=retrieved_course.number,
                    title=retrieved_course.title,
                    description=retrieved_course.description,
                    score=retrieved_course.score,
                )
                for i, retrieved_course in enumerate(retrieved_courses)
            ]
        )
    }
