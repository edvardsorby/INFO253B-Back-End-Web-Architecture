from typing import Annotated

from fastapi import Depends
from pymongo import AsyncMongoClient

from search.config import settings

client: AsyncMongoClient | None = None

database_name = "allcourses"
collection_name = "allcourses_with_embedding"


async def connect_to_mongo():
    global client
    client = AsyncMongoClient(settings.mongo_uri_courses)


async def close_mongo_connection():
    await client.close()


def get_db() -> AsyncMongoClient:
    return client[database_name][collection_name]


Database = Annotated[AsyncMongoClient, Depends(get_db)]
