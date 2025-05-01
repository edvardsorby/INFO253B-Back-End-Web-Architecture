from typing import Annotated

import voyageai
from langchain_core.tools import tool
from pymongo import AsyncMongoClient

from search.db import get_db
from search.models import SearchOut

COURSE_DETAILS_TEMPLATE = """\
Retrieved Course #{rank}:

Course Title:
{department}{course_number}: {full_title}
{instructor}{term_name}

Course Catalog Description:
{catalog_description}

Class Description:
{class_description}

URL:
{url}

Dot product similarity score:
{score}"""


async def retrieve_courses(query: str, db: AsyncMongoClient) -> list[SearchOut]:
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
                    course_number=retrieved_course.course_number,
                    title=(
                        f"{retrieved_course.retrieved_course_title}: {retrieved_course.special_title}"
                        if retrieved_course.special_title
                        else retrieved_course.course_title
                    ),
                    instructor=f"{retrieved_course.instructor} "
                    if retrieved_course.instructor
                    else "",
                    catalog_description=retrieved_course.catalog_description,
                    class_description=retrieved_course.class_description,
                    url=retrieved_course.url,
                    department=retrieved_course.department,
                    term_name=retrieved_course.term_name,
                    score=retrieved_course.score,
                )
                for i, retrieved_course in enumerate(retrieved_courses)
            ]
        )
    }
